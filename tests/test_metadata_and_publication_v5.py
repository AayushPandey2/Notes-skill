"""Metadata and adaptive-size publication through the existing public pipeline."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from scriptorium.engines.composition import (
    build_composition, five_key_note, publish_composition, to_collection_plan,
    validate_chapter, validate_published_composition, inspect_assets,
)
from scriptorium.engines.vault import (
    ensure_obsidian_properties, generate_tags, normalize_tag, validate_semantic_tags,
)
from scriptorium.engines._collection_intelligence import build_knowledge_collection_plan
from scriptorium.engines._interactive import ResolvedNotePreferences
from scriptorium.models import parse_note
from test_comprehensive_composition import specification, reviews_for, inputs


@pytest.mark.parametrize('count', [5, 6, 8, 10])
def test_publication_accepts_adaptive_counts_with_exact_navigation(tmp_path, count):
    spec = specification()
    for i in range(6, count + 1):
        spec['chapters'].append({'id': f'ch{i}', 'title': f'Chapter {i}', 'concepts': [f'c{i}'], 'sections': [f'Concept {i}']})
        spec['concepts'].append({'id': f'c{i}', 'title': f'Concept {i}', 'objectives': ['explain the mechanism'],
                                 'capabilities': ['S01'], 'prerequisites': [f'c{i-1}']})
        for question in deepcopy(spec['assessments'][:4]):
            question.update(id=f'q{i}.{question["id"]}', chapter=f'ch{i}', objectives=[f'c{i}:objective:0'])
            spec['assessments'].append(question)
    plan = build_composition(spec)
    drafts, evidence, _ = inputs(build_composition(specification()))
    for i in range(6, count + 1):
        drafts[f'ch{i}'] = f'# Chapter {i}\n\n## Concept {i}\n\nA contract fixture explanation reviewed separately.\n'
    from scriptorium.engines.composition.contracts import prepare_drafts
    drafts = {key: body.strip() + '\n' for key, body in prepare_drafts(plan, drafts).items()}
    for concept in plan['concepts'][5:]:
        for obligation in concept['research_obligations']:
            evidence[obligation['id']] = deepcopy(next(iter(evidence.values())))
    reviews = reviews_for(plan, drafts)
    report = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert report['complete'], report['errors']
    assert len(report['written_paths']) == count + 1
    assert validate_published_composition(tmp_path, plan)['valid']
    for i, chapter in enumerate(plan['chapters']):
        note = parse_note((tmp_path / chapter['path']).read_text(encoding='utf-8'))
        assert set(note.metadata) == {'id', 'aliases', 'topic', 'tags', 'nexttopics'}
        assert validate_semantic_tags(note.metadata['tags']) == []
        assert note.metadata['nexttopics'] == ([f'[[{Path(plan["chapters"][i+1]["path"]).stem}]]'] if i + 1 < count else [])
    repeat = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews)
    assert repeat['complete'] and not repeat['written_paths']


@pytest.mark.parametrize('count', [4, 11])
def test_out_of_profile_counts_are_rejected(count):
    spec = specification()
    spec['chapters'] = [deepcopy(spec['chapters'][0]) for _ in range(count)]
    with pytest.raises(ValueError, match='5–10'):
        build_composition(spec)


@pytest.mark.parametrize('objectives', [[' '], {'a': 'explain'}, [42], []])
def test_explicit_plans_fail_cleanly_for_malformed_objectives(objectives):
    spec = specification()
    spec['concepts'][0]['objectives'] = objectives
    with pytest.raises(ValueError, match='objectives'):
        build_composition(spec)


def test_semantic_tags_are_normalized_and_deduplicate_synonyms():
    tags = generate_tags(topic='ML', domain='AI', master_topic='Computer Science', note_type='deep-notes',
                         secondary_concepts=['machine_learning', 'Neural Networks', 'neural-networks'])
    assert 'topic/machine-learning' in tags
    assert 'subject/computer-science' in tags
    assert 'domain/artificial-intelligence' in tags
    assert len(tags) == len(set(tags))
    assert normalize_tag('#concept/C++') == 'concept/c-plus-plus'
    assert validate_semantic_tags(tags) == []
    assert validate_semantic_tags(['type/full-notes'])
    assert validate_semantic_tags(tags + ['topic/ML'])


def test_content_ownership_and_explicit_classification_drive_chapter_tags():
    spec = specification()
    spec['topic'] = 'Contractual Remedies'
    spec['classification'] = {'subject': 'Contract Law', 'domain': 'Law'}
    spec['concepts'][0]['title'] = 'Expectation Damages'
    plan = build_composition(spec)
    text = five_key_note(plan, 'ch1', 'Chapter 1', '# Authored body\n', None)
    tags = parse_note(text).metadata['tags']
    assert 'topic/expectation-damages' in tags and 'subject/contract-law' in tags and 'domain/law' in tags
    assert not any('gradient' in tag or 'artificial' in tag for tag in tags)
    assert validate_chapter(text) == []


def test_existing_user_metadata_survives_taxonomy_upgrade():
    original = '---\ntopic: Binary Search\ntags: [personal/favorite]\ncustom: preserve\naliases: [Bisection]\n---\n# Binary Search\n\nKeep this explanation.\n'
    updated = ensure_obsidian_properties(original)
    metadata = parse_note(updated).metadata
    assert metadata['custom'] == 'preserve' and metadata['aliases'] == ['Bisection']
    assert 'personal/favorite' in metadata['tags'] and validate_semantic_tags(metadata['tags']) == []
    assert 'Keep this explanation.' in updated


def test_unknown_classification_stays_plannable_but_cannot_publish_as_precise():
    spec = specification()
    spec['topic'] = 'Zorblax Symbolics'
    plan = build_composition(spec)
    text = five_key_note(plan, 'ch1', 'Chapter 1', '# Chapter\n', None)
    assert any('generic-only' in error for error in validate_chapter(text))
    spec['classification'] = {'domain': 42, 'subject': 'Valid Subject'}
    with pytest.raises(ValueError, match='nonempty strings'):
        build_composition(spec)


def test_kcp_notation_uses_composition_instead_of_unrelated_domain_defaults(tmp_path):
    spec = specification()
    spec['notation'] = {'r': 'residual vector', 'R': 'resistance', 'Ω': 'ohm', 'α': 'temperature coefficient'}
    plan = build_composition(spec)
    prefs = ResolvedNotePreferences('understand', 'M1', None, 'comprehensive', {}, 'hierarchical_collection', [], 'strict')
    kcp = build_knowledge_collection_plan(tmp_path, to_collection_plan(plan), prefs)
    entries = kcp.terminology_registry['entries']
    assert len(entries) == 4
    assert {entry['preferred_symbol'] for entry in entries.values()} == set(spec['notation'])
    assert not any(entry['preferred_term'] == 'loss_function' for entry in entries.values())


def test_cli_can_plan_from_concept_inventory_without_explicit_chapters(tmp_path):
    spec = specification()
    del spec['chapters']
    # Question owners refer to an author-supplied plan; re-plan these after allocation.
    spec['assessments'] = []
    path = tmp_path / 'spec.json'
    path.write_text(json.dumps(spec), encoding='utf-8')
    run = subprocess.run([sys.executable, 'scripts/scribe.py', 'notes', 'compose', '--spec', str(path)],
                         capture_output=True, text=True, encoding='utf-8')
    assert run.returncode == 0, run.stdout + run.stderr
    result = json.loads(run.stdout)
    assert len(result['chapters']) == 5
    assert result['chapter_rationale']


def test_undeclared_remote_markdown_image_cannot_bypass_publication(tmp_path):
    plan = build_composition(specification())
    drafts, evidence, _ = inputs(plan)
    drafts['ch1'] += '\n![a source figure](https://example.test/figure.png)\n'
    report = publish_composition(tmp_path, plan, drafts, evidence=evidence, reviews=reviews_for(plan, drafts))
    assert not report['complete'] and any('unverified remote image' in error for error in report['errors'])
    assert not list(tmp_path.rglob('*.md'))


@pytest.mark.parametrize('image', [
    '![a [nested] caption](https://example.test/a.png)',
    r'![a \] caption](https://example.test/a.png)',
    '![caption][figure]\n\n[figure]: https://example.test/a.png',
])
def test_complex_markdown_labels_and_reference_images_cannot_bypass_acquisition(tmp_path, image):
    plan = build_composition(specification())
    text = five_key_note(plan, 'ch1', 'Chapter 1', '# Chapter\n\n' + image + '\n', None)
    errors, _ = inspect_assets(tmp_path, {plan['chapters'][0]['path']: text}, {})
    assert any('unverified remote image' in error for error in errors)


def test_title_placement_remains_supported_without_fenced_or_duplicate_headings():
    from scriptorium.engines.composition.contracts import insert_at_section
    assert 'inserted' in insert_at_section('# Placement\n\nBody\n', 'Placement', 'inserted')
    assert '## Placement\n\ninserted' in insert_at_section('# Placement\n\n## Placement\n', 'Placement', 'inserted')
    with pytest.raises(ValueError, match='ambiguous'):
        insert_at_section('# Title\n\n## Placement\n\n## Placement\n', 'Placement', 'inserted')


def test_standard_local_images_are_checked_and_fenced_examples_ignored(tmp_path):
    plan = build_composition(specification())
    text = five_key_note(plan, 'ch1', 'Chapter 1', '# Chapter\n\n![figure](../assets/missing.png)\n', None)
    errors, _ = inspect_assets(tmp_path, {plan['chapters'][0]['path']: text}, {})
    assert any('missing Markdown image' in error for error in errors)
    code = five_key_note(plan, 'ch1', 'Chapter 1', '# Chapter\n\n```markdown\n![example](https://example.test/a.png)\n```\n', None)
    assert inspect_assets(tmp_path, {plan['chapters'][0]['path']: code}, {}) == ([], {})


def test_narrow_scaffold_generation_does_not_claim_semantic_verification(tmp_path):
    from scriptorium import OrchestrationEngine, VaultEngine
    orchestration = OrchestrationEngine()
    session = orchestration.start_notes_session('quick binary search reminder')
    session = orchestration.respond_to_session(session, 'use your recommendations')['state']
    result = VaultEngine().generate_collection(tmp_path, session.collection_plan, session.resolved_preferences)
    assert result['complete']  # Backward-compatible field means the files were written.
    assert result['verified'] is False and result['content_state'] == 'generated'
    assert result['manifest']['verified'] is False
    for relative in result['written_paths']:
        assert parse_note((tmp_path / relative).read_text(encoding='utf-8')).metadata['coverage_status'] == 'generated'
