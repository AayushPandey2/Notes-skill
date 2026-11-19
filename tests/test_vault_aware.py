#!/usr/bin/env python3
"""Regression tests for content-aware and vault-aware Scriptorium indexing & validation."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import vault_index as vi
import verify_vault_notes as vn


def test_configured_core_and_templater_discovery_and_dynamic_detection(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / ".obsidian" / "plugins" / "templater-obsidian").mkdir(parents=True)
    (vault / "Templates").mkdir(parents=True)
    (vault / "Templater").mkdir(parents=True)

    (vault / ".obsidian" / "templates.json").write_text(json.dumps({"folder": "Templates"}), encoding="utf-8")
    (vault / ".obsidian" / "plugins" / "templater-obsidian" / "data.json").write_text(
        json.dumps({"templates_folder": "Templater", "folder_templates": [{"folder": "ML", "template": "Templater/ML Note.md"}]}),
        encoding="utf-8",
    )
    (vault / "Templates" / "Study Note.md").write_text(
        '---\ntitle: "{{title}}"\ntags: [study]\n---\n\n# {{title}}\n\n## Core Idea\n\n## Summary\n',
        encoding="utf-8",
    )
    (vault / "Templater" / "ML Note.md").write_text(
        '---\ntitle: "<% tp.file.title %>"\n---\n\n# <% tp.file.title %>\n\n## Intuition\n',
        encoding="utf-8",
    )

    res = vi.build_or_load_index(vault, use_cache=False)
    by_path = {t["path"]: t for t in res["templates"]}
    assert "Templates/Study Note.md" in by_path
    assert by_path["Templates/Study Note.md"]["discovery_source"] == "core_templates_config"
    assert "{{title}}" in by_path["Templates/Study Note.md"]["dynamic_syntax"]["core_placeholders"]
    assert "Templater/ML Note.md" in by_path
    assert by_path["Templater/ML Note.md"]["dynamic_syntax"]["unsupported_templater"]


def test_tag_extraction_false_positives_and_collision_detection(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "notes").mkdir(parents=True)

    (vault / "notes" / "a.md").write_text(
        '---\n'
        'title: "Alpha"\n'
        'tags: "neural_network, ai/deep-learning"\n'
        '---\n\n'
        '# Heading #not-a-heading-tag\n\n'
        'Valid inline #neural-networks and #unicode-café.\n'
        'False positives: `#code_tag` [link](https://example.com/#frag) https://example.org/#urlfrag <!-- #comment_tag --> \\#escaped_tag #12345.\n'
        '```python\n# #fenced_tag\n```\n',
        encoding="utf-8",
    )
    (vault / "notes" / "b.md").write_text(
        '---\ntitle: "Beta"\ntags:\n  - "neural-network"\n---\n\nBody #ai/deep-learning\n',
        encoding="utf-8",
    )

    res = vi.build_or_load_index(vault, use_cache=False)
    tag_map = {t["tag"]: t for t in res["tag_registry"]}
    assert "neural_network" in tag_map
    assert "neural-networks" in tag_map
    assert "neural-network" in tag_map
    assert "ai/deep-learning" in tag_map
    assert tag_map["ai/deep-learning"]["parent_hierarchy"] == "ai"
    assert "unicode-café" in tag_map
    for bad in ("not-a-heading-tag", "code_tag", "frag", "urlfrag", "comment_tag", "escaped_tag", "12345", "fenced_tag"):
        assert bad not in tag_map

    # Collision group detects neural_network / neural-network / neural-networks without mutating tags
    coll_variants = {v for c in res["tag_collisions"] for v in c["variants"]}
    assert {"neural_network", "neural-network", "neural-networks"}.issubset(coll_variants)


def test_cache_invalidation_on_add_edit_delete_and_config_change(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    cache_dir = tmp_path / "cache"
    (vault / ".obsidian").mkdir(parents=True)
    (vault / "topic").mkdir(parents=True)
    n1 = vault / "topic" / "01-intro.md"
    n1.write_text('---\nid: "t1"\ntitle: "Intro"\ntopic: "ML"\ntags: ["ml"]\n---\n\n## Intro\n', encoding="utf-8")

    r1 = vi.build_or_load_index(vault, use_cache=True, cache_dir=cache_dir)
    assert r1["cache_hit"] is False
    r2 = vi.build_or_load_index(vault, use_cache=True, cache_dir=cache_dir)
    assert r2["cache_hit"] is True

    # Add file -> cache invalidated
    n2 = vault / "topic" / "02-next.md"
    n2.write_text('---\nid: "t2"\ntitle: "Next"\ntopic: "ML"\ntags: ["ml"]\n---\n\n## Next\n', encoding="utf-8")
    r3 = vi.build_or_load_index(vault, use_cache=True, cache_dir=cache_dir)
    assert r3["cache_hit"] is False
    assert len(r3["notes"]) == 2

    # Config change -> cache invalidated
    (vault / ".obsidian" / "templates.json").write_text('{"folder": "Templates"}', encoding="utf-8")
    r4 = vi.build_or_load_index(vault, use_cache=True, cache_dir=cache_dir)
    assert r4["cache_hit"] is False

    # Delete file -> cache reflects deletion
    n2.unlink()
    r5 = vi.build_or_load_index(vault, use_cache=True, cache_dir=cache_dir)
    assert r5["cache_hit"] is False
    assert len(r5["notes"]) == 1


def test_custom_template_scoped_validation_preserves_unrelated_notes_and_blocks_stale_plan(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "Templates").mkdir(parents=True)
    (vault / "ml").mkdir(parents=True)

    tpl = vault / "Templates" / "Custom.md"
    tpl_text = '---\ntitle: ""\ntags: []\n---\n\n# Title\n\n## Overview\n'
    tpl.write_text(tpl_text, encoding="utf-8")
    tpl_hash = hashlib.sha256(tpl_text.encode("utf-8")).hexdigest()[:16]

    # Pre-existing unrelated note with intentional legacy quirks that must NOT be modified by scoped --fix
    unrelated = vault / "ml" / "unrelated.md"
    unrelated_bytes = b'---\ntitle: "01-Unrelated"\n---\n\n# Unrelated\n\nInline $ x $ untouched.\n^anchor-1\n'
    unrelated.write_bytes(unrelated_bytes)

    # Custom-template note using <details> and literal YAML LaTeX (allowed for custom templates!)
    custom_note = vault / "ml" / "custom-note.md"
    custom_note.write_text(
        '---\n'
        'title: "Custom Study"\n'
        'formula: "\\\\theta"\n'
        'tags:\n'
        '  - "neural_network"\n'
        '---\n\n'
        '# Custom Study\n\n'
        'Inline $ y $ and link [[unrelated#^anchor-1]].\n\n'
        '<details><summary>Toggle</summary>Allowed in custom template.</details>\n',
        encoding="utf-8",
    )

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "operation_id": "op-1",
                "template_path": "Templates/Custom.md",
                "template_hash": tpl_hash,
                "template_type": "custom",
                "template_frontmatter_keys": ["title", "tags"],
                "outputs": ["ml/custom-note.md"],
                "pre_generation_tags": ["neural-network"],
            }
        ),
        encoding="utf-8",
    )

    # Scoped --fix fixes $ y $ -> $y$, warns NEAR_DUPLICATE_TAG, allows <details> & custom YAML, leaves unrelated byte-identical
    p = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--manifest", str(manifest), "--fix"],
        capture_output=True, text=True, check=False,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    assert "NEAR_DUPLICATE_TAG" in p.stdout
    assert "FORBIDDEN_SECTION_6_STRUCTURE" not in p.stdout
    assert "MISSING_KEY_EQUATIONS_CALLOUT" not in p.stdout
    assert "$y$" in custom_note.read_text(encoding="utf-8")
    assert unrelated.read_bytes() == unrelated_bytes

    # Repeat --fix is idempotent
    p2 = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--manifest", str(manifest), "--fix"],
        capture_output=True, text=True, check=False,
    )
    assert p2.returncode == 0
    assert "Repairs: 0" in p2.stdout

    # Mutating template invalidates manifest -> STALE_TEMPLATE_PLAN
    tpl.write_text(tpl_text + "\n## Extra\n", encoding="utf-8")
    p_stale = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--manifest", str(manifest)],
        capture_output=True, text=True, check=False,
    )
    assert p_stale.returncode == 1
    assert "STALE_TEMPLATE_PLAN" in p_stale.stdout


def test_unresolved_template_syntax_and_path_traversal_rejection(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    bad = vault / "bad.md"
    bad.write_text("---\ntitle: X\n---\n\nHello <% tp.date.now() %> and [[missing#^bad-blk]].\n", encoding="utf-8")

    p = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--files", "bad.md"],
        capture_output=True, text=True, check=False,
    )
    assert p.returncode == 1
    assert "UNRESOLVED_TEMPLATE_SYNTAX" in p.stdout
    assert "UNRESOLVED_WIKILINK" in p.stdout

    # Path traversal rejected
    p_trav = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "verify_vault_notes.py"), str(vault), "--files", "../outside.md"],
        capture_output=True, text=True, check=False,
    )
    assert p_trav.returncode == 2


def test_auto_detect_obsidian_creates_notes_and_saves_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    vault = tmp_path / "MyVault"
    (vault / ".obsidian").mkdir(parents=True)
    sub = vault / "workspace"
    sub.mkdir()
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.delenv("SCRIPTORIUM_VAULT_PATH", raising=False)
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.chdir(sub)

    resolved = vi.resolve_vault_root()
    assert resolved == Path(os.path.realpath(vault))
    assert (vault / "Notes").is_dir()
    cfg = json.loads((fake_home / ".scriptorium-config.json").read_text(encoding="utf-8"))
    assert Path(cfg["vault_path"]) == resolved
    assert cfg["notes_folder"] == "Notes"
    assert Path(cfg["notes_path"]) == resolved / "Notes"
    assert vi.resolve_notes_folder(resolved) == "Notes"

    custom = vault / "Study" / "AI"
    saved = vi.set_notes_folder(custom)
    assert Path(saved["vault_path"]) == resolved
    assert saved["notes_folder"] == "Study/AI"
    assert vi.resolve_notes_folder(resolved) == "Study/AI"


def test_discover_detects_topic_workflow_notes_vs_deepnotes(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "OS").mkdir(parents=True)
    (vault / "Transformers").mkdir(parents=True)
    (vault / "Mixed").mkdir(parents=True)

    (vault / "OS" / "01 - Paging.md").write_text(
        '---\nid: "01-paging"\ntopic: "OS"\ntags: [study-notes]\nnexttopics: []\n---\n\n'
        '# Paging\n\n## 1. Overview, Source Context & Learning Goals\n',
        encoding="utf-8",
    )
    (vault / "Transformers" / "01 - Attention.md").write_text(
        '---\nid: "01-attention"\ntopic: "Transformers"\ntags: [deepstudy-master]\nnexttopics: []\n---\n\n'
        '# Attention\n',
        encoding="utf-8",
    )
    (vault / "Mixed" / "01 - A.md").write_text(
        '---\nid: "01-a"\ntopic: "Mixed"\ntags: [study-notes]\nnexttopics: []\n---\n',
        encoding="utf-8",
    )
    (vault / "Mixed" / "02 - B.md").write_text(
        '---\nid: "02-b"\ntopic: "Mixed"\ntags: [deepstudy-master]\nnexttopics: []\n---\n',
        encoding="utf-8",
    )

    p_notes = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "vault_index.py"), str(vault), "--discover", "--topic", "OS", "--no-cache"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_notes.stdout)["detected_workflow"] == "notes"

    p_deep = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "vault_index.py"), str(vault), "--discover", "--topic", "Transformers", "--no-cache"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_deep.stdout)["detected_workflow"] == "deepnotes"

    p_mixed = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "vault_index.py"), str(vault), "--discover", "--topic", "Mixed", "--no-cache"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_mixed.stdout)["detected_workflow"] == "mixed"

    p_none = subprocess.run(
        [sys.executable, "-B", str(SCRIPTS_DIR / "vault_index.py"), str(vault), "--discover", "--topic", "NonExistent", "--no-cache"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(p_none.stdout)["detected_workflow"] is None
