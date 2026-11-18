#!/usr/bin/env python3
"""Tests for 00-MOC syllabus boundary enforcement & scaffolding."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import scaffold_note as sn
import verify_vault_notes as vn


def test_syllabus_scaffolding_and_scope_boundary_enforcement(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    topic_dir = vault / "logistic-regression"
    topic_dir.mkdir(parents=True)

    # 1. Scaffold 00-MOC-logistic-regression.md
    rc = sn.main(
        [
            str(vault),
            "--syllabus",
            "--output",
            "logistic-regression/00-MOC-logistic-regression.md",
            "--topic",
            "Logistic Regression",
            "--base-domain",
            "Computer Science",
            "--master-topic",
            "Machine Learning",
            "--allowed-subtopics",
            "01-sigmoid.md",
            "--excluded-topics",
            "Neural Networks (separate topic)",
        ]
    )
    assert rc == 0
    moc = topic_dir / "00-MOC-logistic-regression.md"
    assert moc.is_file()

    # 2. Allowed note passes without OUT_OF_SCOPE_NOTE_CREATED
    allowed_note = topic_dir / "01-sigmoid.md"
    allowed_note.write_text(
        "---\n"
        'id: "lr-01"\n'
        'title: "Sigmoid Function"\n'
        'aliases: ["Sigmoid Function"]\n'
        'topic: "Logistic Regression"\n'
        "tags: [ml, logistic-regression]\n"
        "---\n\n"
        "# 01. Sigmoid Function\n\nBody.\n",
        encoding="utf-8",
    )

    # 3. Unapproved tangent note triggers OUT_OF_SCOPE_NOTE_CREATED
    tangent_note = topic_dir / "02-neural-networks-tangent.md"
    tangent_note.write_text(
        "---\n"
        'id: "lr-02"\n'
        'title: "Neural Networks Tangent"\n'
        'aliases: ["Neural Networks Tangent"]\n'
        'topic: "Logistic Regression"\n'
        "tags: [ml, logistic-regression]\n"
        "---\n\n"
        "# 02. Neural Networks Tangent\n\nTangent.\n",
        encoding="utf-8",
    )

    vidx = vn.build_vault_index(vault)
    moc_findings = vn.validate_file(moc, vault, vidx)
    assert not [f for f in moc_findings if f["level"] == "ERROR"]

    allowed_findings = vn.validate_file(allowed_note, vault, vidx)
    assert not [f for f in allowed_findings if f["code"] == "OUT_OF_SCOPE_NOTE_CREATED"]

    tangent_findings = vn.validate_file(tangent_note, vault, vidx)
    assert any(
        f["level"] == "ERROR" and f["code"] == "OUT_OF_SCOPE_NOTE_CREATED"
        for f in tangent_findings
    )
