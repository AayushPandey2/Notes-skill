"""Optional declarations must accept omission and reject incomplete inclusion."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import note_layout
from validate_note import validate_text
from test_routed_workflow import finish_fixture
from scaffold_note import main

def test_optional_declarations(tmp_path, monkeypatch):
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "summary.md").write_text("# Spec\n## 1. Core\n## [OPTIONAL] Why this detail?\n", encoding="utf-8")
    monkeypatch.setattr(note_layout, "ROOT", tmp_path)
    assert note_layout.matches_layout("summary", 0, ["## 1. Core"])
    assert note_layout.matches_layout("summary", 0, ["## 1. Core", "## 2. Why this detail?"])
    assert not note_layout.matches_layout("summary", 0, ["## 1. Unknown"])
    assert not note_layout.matches_layout("summary", 0, ["## 1. Core", "## 2. Why this detail?", "## 3. Why this detail?"])

def test_strict_review_does_not_add_yaml_keys():
    import yaml
    from patch_links import patch_frontmatter_text
    metadata = {"id":"check", "aliases":["Check"], "topic":"Check", "tags":["check"], "nexttopics":[]}
    text = "---\n" + yaml.safe_dump(metadata,sort_keys=False) + "---\nBody\n"
    updated, changed = patch_frontmatter_text(text, append_review_log=["Needs practice"])
    assert changed
    assert yaml.safe_load(updated.split("---")[1]) == metadata
    assert "**Review** :: Needs practice" in updated



def test_declared_optional_module_validates_and_requires_content(tmp_path):
    import argparse
    from scaffold_note import render_routed_note
    args = argparse.Namespace(template="summary", topic="QA", title="QA", number="01",
        base_domain="QA", master_topic="QA", aliases=[], tags=[], next_topic=None,
        depends_on=[], math_level=0, narrow_practice=False, compared_notes=[])
    draft = finish_fixture(render_routed_note(args, "qa"))
    title = note_layout.optional_headings("summary")[0]
    optional = "## 5. " + title + "\n\n**Context:** Conflicting definitions.\n\n**Analysis:** Compare the stated domains.\n\n**Check:** Confirm source conditions.\n\n"
    authored = draft.replace("### Metacognitive Reflection", optional + "### Metacognitive Reflection")
    assert not validate_text(authored, route="summary", math_level=0)
    assert any("nonempty Check" in msg for _,msg in validate_text(authored.replace("**Check:** Confirm source conditions.", ""), route="summary", math_level=0))
