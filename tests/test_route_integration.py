"""Integration fixtures for the merged command, template and validation paths."""
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import note_contracts as nc
import route_request as rr
import scaffold_note as sn
import verify_vault_notes as vn
import vault_index as vi


@pytest.mark.parametrize("query,kwargs,route,language", [
    ("/scribe-dsa cpp https://example.org/problem", {}, "dsa", "cpp"),
    ("/scribe-dsa python Find the maximum", {}, "dsa", "python"),
    ("/scribe-practice CNN https://example.org/reference", {}, "practice", None),
    ("https://www.youtube.com/watch?v=fixture", {}, "summary", None),
    ("https://arxiv.org/abs/1706.03762", {}, "paper-breakdown", None),
    ("Summarize https://arxiv.org/pdf/1706.03762", {}, "summary", None),
    ("Study CNN with https://arxiv.org/abs/1706.03762", {"purpose": "implementation", "domain": "ml"}, "deepstudy-coding", "python"),
    ("nn.Conv2d parameters", {}, "api-table", None),
    ("A transaction with logging, locking and recovery", {}, "deepstudy-general", None),
    ("A reusable concept", {"purpose": "idea"}, "atomic", None),
    ("Revise concurrency", {}, "cheat-sheet", None),
    ("Compare locking vs snapshots", {}, "comparison", None),
    ("/scribe-distill concurrency", {}, "cheat-sheet", None),
    ("/scribe-compare locking vs snapshots", {}, "comparison", None),
])
def test_request_routing(query, kwargs, route, language):
    plan = rr.plan_request(query, **kwargs)
    assert (plan["template"], plan["language"]) == (route, language)
    selected = [r for r in plan["resources"] if "/templates/" in r]
    assert selected == [nc.routes()[route]["file"]]
    if route == "practice":
        assert plan["practice_policy"] == "none"


@pytest.mark.parametrize("query,kwargs", [
    ("/scribe-dsa rust Find max", {}), ("/scribe-dsa cpp", {}),
    ("/scribe-practice", {}), ("/scribe-dsa cpp Find max", {"template": "summary"}),
    ("A topic", {"template": "unknown"}),
])
def test_invalid_requests_fail_usefully(query, kwargs):
    with pytest.raises(ValueError):
        rr.plan_request(query, **kwargs)


def sample_note(template, level=0):
    """Small artificial structural fixture, not a claim of complete teaching content."""
    text = sn.render_note_skeleton(template=template, math_level=level, note_id=template,
        number="01", title=template, base_domain="Fixtures", master_topic="Integration", topic="Fixture")
    text = re.sub(r"<!-- SCRIPTORIUM_DRAFT.*?-->\n", "", text)
    for h in nc.route_headings(template, level):
        text = text.replace("## " + h + "\n", "## " + h + "\n\nA deliberately small fixture case.\n", 1)
    if template.startswith("deepstudy"):
        questions = "\n".join(f"### Q{i}. Explain case {i}\n\n> [!example]- Reveal answer\n> This is the fixture answer.\n" for i in range(1, 6))
        text = text.replace("## Open Confusion", questions + "\n## Open Confusion")
    if template == "summary":
        text = text.replace("## Breakdown", "- First thesis.\n- Second thesis.\n- Third thesis.\n\n## Breakdown")
    if template == "practice":
        questions = "\n".join(f"### Q{i}. Solve case {i}\n\n> [!hint]- Hint\n> Inspect the given state.\n\n> [!tip]- Solution\n> **Core intuition:** Inspect the state.\n> 1. Read the stated value.\n> **Final answer:** The stated value.\n> **Common trap:** Changing the input.\n" for i in range(1, 11))
        text = text.replace("## Review next", questions + "\n## Review next")
    if level:
        math = "| Symbol | Meaning | Type/domain/shape | Units/range | Effect when changed |\n|---|---|---|---|---|\n| $x$ | Input | Real scalar | Unitless | Increases output |\n\n$$x=x$$\n\nWorked substitution: use the input itself.\n"
        if level == 2:
            math += "\n### Derivation, step by step\n1. Use reflexivity. **Why this step holds:** Equality is reflexive. This proves identity only.\n"
        text += "\n" + math
    return text


@pytest.mark.parametrize("template", list(nc.routes()))
def test_every_route_through_scaffold_and_validator(tmp_path, template):
    spec = nc.routes()[template]
    assert (nc.ROOT / spec["file"]).is_file()
    assert rr.plan_request("fixture", template=template)["template"] == template
    path = tmp_path / (template + ".md")
    assert sn.main([str(tmp_path), "--output", path.name, "--topic", "Fixture", "--title", template, "--template", template]) == 0
    draft = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(draft.split("---")[1])
    assert metadata["note_type"] == template
    assert "UNFINISHED_NOTE" in {c for c, _ in nc.validate_route(draft, template)}
    path.write_text(sample_note(template), encoding="utf-8")
    assert vn.main([str(tmp_path), "--files", path.name]) == 0


@pytest.mark.parametrize("template,level", [("deepstudy-coding", 0), ("deepstudy-general", 1), ("deepstudy-general", 2), ("paper-breakdown", 0)])
def test_math_is_independent_of_route(tmp_path, template, level):
    text = sample_note(template, level)
    assert not nc.validate_route(text, template, level)
    if level:
        assert "MATH_CONTRACT" in {c for c, _ in nc.validate_route(text.replace("| Symbol |", "| Name |"), template, level)}
    if template == "paper-breakdown":
        assert "## Technical Details" in text and "## Math / Technical Details" not in text


def test_compact_limits_include_code_tables_and_link_labels():
    text = "---\ntitle: Hidden metadata\n---\n# Visible\n| Header | Cell |\n|---|---|\n| table words | [[Target|Readable label]] |\n```python\ncode words count\n```\n[Two words](https://example.org/path)"
    assert nc.rendered_word_count(text) == 12
    atomic = sample_note("atomic") + "\n" + "word " * 150
    assert "ATOMIC_WORD_LIMIT" in {c for c, _ in nc.validate_route(atomic, "atomic")}
    sheet = sample_note("cheat-sheet") + "\n```text\n" + "word " * 351 + "\n```"
    assert "CHEATSHEET_WORD_LIMIT" in {c for c, _ in nc.validate_route(sheet, "cheat-sheet")}


def test_practice_keeps_solution_independently_collapsed():
    text = sample_note("practice")
    assert not nc.validate_route(text, "practice")
    assert "PRACTICE_CALLOUTS" in {c for c, _ in nc.validate_route(text.replace("[!tip]-", "[!tip]+", 1), "practice")}


def test_mixed_manifest_custom_precedence_and_scoped_fix(tmp_path):
    untouched = tmp_path / "existing.md"
    untouched.write_bytes(b"Leave this user text $ x $ unchanged.\n")
    note = tmp_path / "new.md"
    text = sample_note("atomic").replace("note_type: atomic\nmath_level: 0\n", "")
    note.write_text(text, encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"outputs": ["new.md"], "notes": {"new.md": {"template": "atomic", "math_level": 0}}}), encoding="utf-8")
    assert vn.main([str(tmp_path), "--manifest", str(manifest), "--fix"]) == 0
    assert untouched.read_bytes() == b"Leave this user text $ x $ unchanged.\n"
    assert vn._resolve_note_schema("new.md", {}, {"outputs": ["new.md"], "template_type": "custom", "notes": {"new.md": {"template": "atomic"}}}) == "custom"
    manifest_entry = {"outputs": ["new.md"], "notes": {"new.md": {"template_type": "custom", "template": "atomic"}}}
    assert vn._resolve_note_schema("new.md", {}, manifest_entry) == "custom"


def test_resources_extract_and_safe_paths(tmp_path):
    plan = rr.plan_request("theorem", purpose="understanding", math_level=2)
    assert "references/modules/math.md" in plan["resources"]
    assert "references/modules/verification.md" not in plan["resources"]
    assert rr.plan_request("/scribe-doubt Fixture question")["resources"] == []
    assert rr.plan_request("/scribe-quiz Fixture")["mode"] == "interactive"
    note = tmp_path / "new.md"
    note.write_text(sample_note("deepstudy-general"), encoding="utf-8")
    extracted = vi.extract_note_sections(tmp_path, "new.md", ["Overview", "Details", "Connection"])
    assert "## Overview" in extracted and "## Open Confusion" not in extracted
    for relative in ["../outside.md", "C:/outside.md", "NUL.md", ".git/config", "nested/../../escape.md"]:
        with pytest.raises(ValueError): nc.safe_path(tmp_path, relative)


def test_mixed_custom_stale_template_blocks_fixes(tmp_path, capsys):
    import hashlib
    template = tmp_path / "Custom.md"
    template.write_text("## Custom\n", encoding="utf-8")
    digest = hashlib.sha256(template.read_bytes()).hexdigest()[:16]
    note = tmp_path / "new.md"
    note.write_text("---\ntitle: Custom\n---\n\nInline $ x $ remains.\n", encoding="utf-8")
    original = note.read_bytes()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"outputs": ["new.md"], "notes": {"new.md": {
        "template_type": "custom", "template_path": "Custom.md", "template_hash": digest}}}), encoding="utf-8")
    template.write_text("## Changed\n", encoding="utf-8")
    assert vn.main([str(tmp_path), "--manifest", str(manifest), "--fix"]) == 1
    assert "STALE_TEMPLATE_PLAN" in capsys.readouterr().out
    assert note.read_bytes() == original


def test_wrapper_paths_and_entry_points():
    root = nc.ROOT
    for wrapper in (root / "skills").glob("*/SKILL.md"):
        content = wrapper.read_text(encoding="utf-8")
        assert yaml.safe_load(content.split("---")[1])["name"] == wrapper.parent.name
        assert (wrapper.parent / "../../SKILL.md").resolve() == root / "SKILL.md"
        section = re.search(r"## Command ([A-I])", content)[1]
        assert f"## Command {section}:" in (root / "references/command_playbooks.md").read_text(encoding="utf-8")
