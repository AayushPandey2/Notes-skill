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


def test_scaffold_note_defaults_to_adaptive_deep_study(tmp_path: Path) -> None:
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
    assert "deepstudy-master" in text
    assert "templates/notes_decision_matrix.md" in text
    assert "Key Equations" not in text
    assert "## " not in text

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


def test_verify_vault_notes_accepts_multilang_s5_and_warns_above_3(tmp_path: Path) -> None:
    import verify_vault_notes as vn

    vault = tmp_path / "vault"
    (vault / "dsa" / "topics").mkdir(parents=True)
    note = vault / "dsa" / "topics" / "01-seg.md"
    q_block = "".join(
        f"#### Question {i}\nBody\n\n> [!example]- Answer\n> - Detail\n\n" for i in range(1, 6)
    )
    note.write_text(
        "---\n"
        'id: "dsa-01"\n'
        'aliases: ["Segment Tree"]\n'
        'topic: "Trees"\n'
        "tags: [cs, dsa]\n"
        "nexttopics: []\n"
        "---\n\n"
        "# 01. Segment Tree\n\n"
        "> [!abstract] Key Equations\n"
        "> $$T = O(\\log n)$$\n\n"
        "## 5. Executable Verification (C++20 & Python 3)\n\n"
        "### Implementation 1 — C++20\n```cpp\nint main() { return 0; }\n```\n\n"
        "### Implementation 2 — Python 3\n```python\nassert True\n```\n\n"
        "## 6. Deep Conceptual & Analytical Q&A Mastery Set\n\n"
        + q_block,
        encoding="utf-8",
    )

    findings = vn.validate_file(note, vault, vn.build_vault_index(vault))
    assert not [f for f in findings if f["level"] == "ERROR"]
    assert not [f for f in findings if f["code"] == "TOO_MANY_SECTION_5_IMPLEMENTATIONS"]

    # Adding 2 more implementations (total 4) triggers TOO_MANY_SECTION_5_IMPLEMENTATIONS warning
    note.write_text(
        note.read_text(encoding="utf-8").replace(
            "## 6. Deep Conceptual",
            "### Implementation 3 — Rust\n```rust\nfn main() {}\n```\n\n"
            "### Implementation 4 — Java\n```java\nclass Main {}\n```\n\n"
            "## 6. Deep Conceptual",
        ),
        encoding="utf-8",
    )
    findings_4 = vn.validate_file(note, vault, vn.build_vault_index(vault))
    assert any(f["code"] == "TOO_MANY_SECTION_5_IMPLEMENTATIONS" for f in findings_4)
