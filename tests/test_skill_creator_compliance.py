"""Skill-creator compliance, progressive disclosure, eval schema & trigger verification tests."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scriptorium.engines._token_optimizer import (
    measure_naive_full_context_tokens,
    select_context_bundle,
)
from scriptorium.engines.orchestration import route_request
from scriptorium.triggers import dispatch_trigger

ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def _parse_frontmatter(skill_md: Path) -> tuple[dict, str]:
    content = skill_md.read_text(encoding="utf-8")
    assert content.startswith("---"), f"{skill_md} missing YAML frontmatter"
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", content, re.DOTALL)
    assert m is not None, f"{skill_md} has invalid frontmatter delimiters"
    fm = yaml.safe_load(m.group(1))
    assert isinstance(fm, dict), f"{skill_md} frontmatter must parse as dict"
    return fm, m.group(2)


@pytest.mark.parametrize(
    "skill_dir",
    [
        ROOT,
        ROOT / "skills" / "scribe-notes",
        ROOT / "skills" / "scribe-doubt",
        ROOT / "skills" / "scribe-quiz",
        ROOT / "skills" / "scribe-setfolder",
    ],
)
def test_skill_creator_frontmatter_and_progressive_disclosure(skill_dir: Path):
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.is_file()
    fm, body = _parse_frontmatter(skill_md)

    unexpected = set(fm.keys()) - ALLOWED_FRONTMATTER_KEYS
    assert unexpected == set(), f"{skill_md} has disallowed keys: {unexpected}"
    assert "name" in fm and "description" in fm

    name = str(fm["name"]).strip()
    assert re.match(r"^[a-z0-9-]+$", name), f"Invalid kebab-case name: {name}"
    assert not (name.startswith("-") or name.endswith("-") or "--" in name)
    assert len(name) <= 64

    desc = str(fm["description"]).strip()
    assert desc, f"{skill_md} empty description"
    assert "<" not in desc and ">" not in desc, f"{skill_md} description cannot contain < or >"
    assert len(desc) <= 1024, f"{skill_md} description exceeds 1024 chars ({len(desc)})"
    assert any(cue in desc.lower() for cue in ("use when", "use whenever")), (
        f"{skill_md} description should state concrete trigger conditions"
    )

    line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
    assert line_count <= 120, f"{skill_md} should stay lean via progressive disclosure ({line_count} lines)"
    assert body.strip()


def test_evals_json_and_trigger_eval_schemas_and_routing():
    evals_path = ROOT / "evals" / "evals.json"
    trig_path = ROOT / "evals" / "trigger_eval.json"
    assert evals_path.is_file() and trig_path.is_file()

    evals_data = json.loads(evals_path.read_text(encoding="utf-8"))
    assert evals_data["skill_name"] == "scriptorium"
    assert len(evals_data["evals"]) >= 6
    seen_ids = set()
    for item in evals_data["evals"]:
        assert isinstance(item["id"], int) and item["id"] not in seen_ids
        seen_ids.add(item["id"])
        assert item["prompt"].strip()
        assert item["expected_output"].strip()
        assert isinstance(item.get("files", []), list)
        assert isinstance(item.get("expectations", []), list) and len(item["expectations"]) >= 2

    trig_data = json.loads(trig_path.read_text(encoding="utf-8"))
    for q in trig_data["queries"]:
        if not q["should_trigger"]:
            continue
        if q["expected_command"] == "scribe-notes" and q["expected_master"]:
            if "/scribe-ytnote" in q["query"].lower():
                v_dispatch = dispatch_trigger("VIDEO-01")
                assert v_dispatch["trigger"] == "VIDEO-01"
            else:
                routed = route_request(q["query"], root=ROOT)
                assert routed["master"] == q["expected_master"], (
                    f"Query routed to {routed['master']} instead of {q['expected_master']}: {q['query']}"
                )


def test_selective_context_reduces_tokens_substantially():
    naive = measure_naive_full_context_tokens(ROOT)
    for master, ktypes in (("M1", ["mathematical"]), ("M3", ["conceptual"]), ("M5", ["computational"])):
        bundle = select_context_bundle(master=master, knowledge_types=ktypes, root=ROOT)
        assert bundle["estimated_tokens"] < naive["estimated_tokens"] * 0.25
        assert len(bundle["loaded_files"]) < naive["files_loaded"]
