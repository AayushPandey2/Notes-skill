#!/usr/bin/env python3
"""Tests for scripts/patch_links.py and scripts/vault_graph.py."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import json
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import patch_links as pl
import vault_graph as vg


def test_patch_frontmatter_preserves_body_and_supports_dry_run(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "ml").mkdir(parents=True)
    note = vault / "ml" / "02-gd.md"
    body = (
        "\n# Gradient Descent\n\n"
        "> [!abstract] Key Equations\n"
        "> $$\\theta_{t+1} = \\theta_t - \\eta \\nabla L(\\theta_t)$$\n\n"
        "See [[01-calculus|Calculus]].\n"
    )
    initial = (
        "---\n"
        'id: "ml-02"\n'
        'title: "Gradient Descent"\n'
        "depends_on:\n"
        '  - "[[01-calculus]]"\n'
        "tags:\n"
        "  - ml\n"
        "---\n"
        + body
    )
    note.write_text(initial, encoding="utf-8")

    # Dry run must not modify disk
    rc_dry = pl.main(
        [
            str(vault),
            "--file",
            "ml/02-gd.md",
            "--add-depends-on",
            "[[00-linalg|Linear Algebra]]",
            "--set-next-topic",
            "[[03-sgd|SGD]]",
            "--append-review-log",
            "2026-11-18 | Score: 4/5 | Weak: step size bound",
            "--dry-run",
        ]
    )
    assert rc_dry == 0
    assert note.read_text(encoding="utf-8") == initial

    # Apply for real
    rc_apply = pl.main(
        [
            str(vault),
            "--file",
            "ml/02-gd.md",
            "--add-depends-on",
            "[[00-linalg|Linear Algebra]]",
            "--set-next-topic",
            "[[03-sgd|SGD]]",
            "--append-review-log",
            "2026-11-18 | Score: 4/5 | Weak: step size bound",
            "--add-alias",
            "GD",
            "--set-status",
            "verified",
        ]
    )
    assert rc_apply == 0

    updated = note.read_text(encoding="utf-8")
    assert updated.endswith(body)
    yaml_part = updated.split("---", 2)[1]
    meta = yaml.safe_load(yaml_part)
    assert meta["depends_on"] == ["[[01-calculus]]", "[[00-linalg|Linear Algebra]]"]
    assert meta["nexttopics"] == ["[[03-sgd|SGD]]"]
    assert meta["review_log"] == ["2026-11-18 | Score: 4/5 | Weak: step size bound"]
    assert meta["aliases"] == ["GD"]
    assert meta["status"] == "verified"
    assert meta["tags"] == ["ml"]


def test_rename_link_skips_code_and_preserves_anchors_and_aliases(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "notes").mkdir(parents=True)
    n1 = vault / "notes" / "a.md"
    n1.write_text(
        "---\n"
        'title: "Alpha"\n'
        'depends_on: ["[[Old Note]]"]\n'
        "---\n\n"
        "Link [[Old Note]], aliased [[Old Note|Custom]], anchored [[Old Note#Section|Sec]].\n"
        "Inline code `[[Old Note]]` and <!-- [[Old Note]] --> must stay untouched.\n\n"
        "```markdown\n"
        "[[Old Note]]\n"
        "```\n",
        encoding="utf-8",
    )

    rc = pl.main([str(vault), "--rename-link", "Old Note", "New Note"])
    assert rc == 0
    text = n1.read_text(encoding="utf-8")
    assert 'depends_on:\n' not in text  # untouched YAML formatting
    assert 'depends_on: ["[[New Note]]"]' in text
    assert "Link [[New Note]], aliased [[New Note|Custom]], anchored [[New Note#Section|Sec]]." in text
    assert "`[[Old Note]]`" in text
    assert "<!-- [[Old Note]] -->" in text
    assert "```markdown\n[[Old Note]]\n```" in text


def test_patch_links_rejects_traversal(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("---\ntitle: Outside\n---\n", encoding="utf-8")

    rc = pl.main([str(vault), "--file", "../outside.md", "--set-status", "bad"])
    assert rc == 2


def test_vault_graph_topo_order_and_mermaid(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "ml").mkdir(parents=True)
    (vault / "ml" / "01-intro.md").write_text(
        '---\nid: "ml-01"\ntitle: "Intro"\ntopic: "ML"\nnext_topic: "[[02-gd]]"\n---\n\n# Intro\n',
        encoding="utf-8",
    )
    (vault / "ml" / "02-gd.md").write_text(
        '---\nid: "ml-02"\ntitle: "Gradient Descent"\ntopic: "ML"\ndepends_on: ["[[01-intro]]"]\nnext_topic: "[[03-sgd]]"\n---\n\n# GD\n\nSee [[01-intro]].\n',
        encoding="utf-8",
    )
    (vault / "ml" / "03-sgd.md").write_text(
        '---\nid: "ml-03"\ntitle: "SGD"\ntopic: "ML"\ndepends_on: ["[[02-gd]]"]\n---\n\n# SGD\n',
        encoding="utf-8",
    )

    report = vg.analyze_vault_graph(vault, topic_filter="ML", use_cache=False)
    assert report["summary"]["note_count"] == 3
    assert report["depends_cycles"] == []
    assert report["broken_links"] == []
    assert report["topo_order"] == ["ml/01-intro.md", "ml/02-gd.md", "ml/03-sgd.md"]

    mermaid = vg.format_mermaid(report)
    assert "flowchart LR" in mermaid
    assert "-->|depends|" in mermaid
    assert "-.->|next|" in mermaid
    assert vg.main([str(vault), "--check-cycles", "--strict", "--no-cache"]) == 0


def test_vault_graph_detects_cycles_broken_links_and_isolated(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "topic").mkdir(parents=True)
    (vault / "topic" / "a.md").write_text(
        '---\ntitle: "A"\ndepends_on: ["[[b]]"]\n---\n\nSee [[missing-note]].\n',
        encoding="utf-8",
    )
    (vault / "topic" / "b.md").write_text(
        '---\ntitle: "B"\ndepends_on: ["[[a]]"]\n---\n\nBody\n',
        encoding="utf-8",
    )
    (vault / "topic" / "lonely.md").write_text(
        '---\ntitle: "Lonely"\n---\n\nNo links.\n',
        encoding="utf-8",
    )

    report = vg.analyze_vault_graph(vault, use_cache=False)
    assert report["summary"]["depends_cycle_count"] == 1
    assert set(report["blocked_by_cycle"]) == {"topic/a.md", "topic/b.md"}
    assert report["broken_links"] == [{"source": "topic/a.md", "field": "body", "target": "missing-note"}]
    assert report["isolated"] == ["topic/lonely.md"]

    assert vg.main([str(vault), "--check-cycles", "--no-cache"]) == 1
    assert vg.main([str(vault), "--strict", "--no-cache"]) == 1

    # Also catch nexttopics cycles via --check-cycles
    nxt_vault = tmp_path / "nxt_vault"
    (nxt_vault / "topic").mkdir(parents=True)
    (nxt_vault / "topic" / "x.md").write_text('---\nid: "x"\naliases: ["X"]\ntopic: "T"\ntags: [t]\nnexttopics: ["[[y]]"]\n---\n', encoding="utf-8")
    (nxt_vault / "topic" / "y.md").write_text('---\nid: "y"\naliases: ["Y"]\ntopic: "T"\ntags: [t]\nnexttopics: ["[[x]]"]\n---\n', encoding="utf-8")
    assert vg.main([str(nxt_vault), "--check-cycles", "--no-cache"]) == 1
