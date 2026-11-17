#!/usr/bin/env python3
"""Tests for token-optimization features: scaffold_note.py, --fields, and --extract."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import scaffold_note as sn
import vault_index as vi


def test_scaffold_note_creates_valid_7_section_skeleton(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    rc = sn.main(
        [
            str(vault),
            "--output",
            "ml/02-gradient-descent.md",
            "--id",
            "ml-02",
            "--number",
            "02",
            "--title",
            "Gradient Descent",
            "--base-domain",
            "Computer Science",
            "--master-topic",
            "Machine Learning",
            "--topic",
            "Optimization",
            "--tags",
            "ml",
            "optimization",
            "--depends-on",
            "[[01-calculus|Calculus]]",
        ]
    )
    assert rc == 0
    out_file = vault / "ml" / "02-gradient-descent.md"
    assert out_file.is_file()
    text = out_file.read_text(encoding="utf-8")
    assert "# 02. Gradient Descent" in text
    assert "> [!abstract] Key Equations" in text
    for sec in range(1, 8):
        assert f"## {sec}." in text

    # Refuses overwrite without --overwrite
    assert sn.main([str(vault), "--output", "ml/02-gradient-descent.md", "--title", "Gradient Descent", "--topic", "Optimization"]) == 2
    # Rejects traversal
    assert sn.main([str(vault), "--output", "../escape.md", "--title", "Escape", "--topic", "Bad"]) == 2


def test_vault_index_fields_and_extract_sections(tmp_path: Path, capsys) -> None:
    vault = tmp_path / "vault"
    (vault / "ml").mkdir(parents=True)
    note = vault / "ml" / "01-gd.md"
    note.write_text(
        "---\n"
        'id: "ml-01"\n'
        'title: "Gradient Descent"\n'
        'topic: "ML"\n'
        "tags: [ml, optimization]\n"
        "---\n\n"
        "# 01. Gradient Descent\n\n"
        "> [!abstract] Key Equations\n"
        "> $$x_{t+1} = x_t - \\eta \\nabla f(x_t)$$\n\n"
        "## 1. Executive Synthesis\n"
        "First-order iterative optimizer.\n\n"
        "## 3. Deep Theory\n"
        "Uses negative gradient direction.\n\n"
        "## 4. Proof\n"
        "Long derivation omitted during distill.\n"
        "```python\n"
        "## not a heading inside code\n"
        "```\n\n"
        "## 7. Common Traps\n"
        "Learning rate too large diverges.\n",
        encoding="utf-8",
    )

    # --fields returns only requested keys
    rc = vi.main([str(vault), "--topic", "ML", "--fields", "file,title,headings", "--no-cache"])
    assert rc == 0
    captured = capsys.readouterr().out
    rows = json.loads(captured)
    assert len(rows) == 1
    assert set(rows[0].keys()) == {"file", "title", "headings"}

    # --extract --sections abstract,1,7 skips sections 3 and 4
    rc2 = vi.main([str(vault), "--extract", "ml/01-gd.md", "--sections", "abstract,1,7"])
    assert rc2 == 0
    extracted = capsys.readouterr().out
    assert "> [!abstract] Key Equations" in extracted
    assert "## 1. Executive Synthesis" in extracted
    assert "## 7. Common Traps" in extracted
    assert "## 4. Proof" not in extracted
    assert "Long derivation omitted during distill." not in extracted
    assert "## not a heading inside code" not in extracted
