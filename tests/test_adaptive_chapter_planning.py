"""Observable allocation behavior across domains, not generated wording tests."""
from copy import deepcopy

import pytest

from scriptorium.engines.composition.planning import plan_chapters, validate_chapter_count


def inventory(titles, **overrides):
    return [{"id": f"c{i}", "title": title, "objectives": ["explain the mechanism"], **deepcopy(overrides)}
            for i, title in enumerate(titles)]


@pytest.mark.parametrize("topic,size,count", [
    ("Ancient history", 5, 5),
    ("Circuit analysis", 24, 6),
    ("Algorithms", 36, 8),
    ("Multivariable calculus", 45, 10),
])
def test_adaptive_counts_and_exact_ownership_across_domains(topic, size, count):
    concepts = inventory([f"{topic} concept {i}" for i in range(size)])
    result = plan_chapters(concepts)
    chapters = result["chapters"]
    assert len(chapters) == count
    owned = [cid for chapter in chapters for cid in chapter["concepts"]]
    assert owned == [concept["id"] for concept in concepts]
    assert len(owned) == len(set(owned))
    assert len({chapter["id"] for chapter in chapters}) == count
    assert all(chapter["sections"] and chapter["estimate"]["units"] > 0 for chapter in chapters)
    assert sum(chapter["estimate"]["units"] for chapter in chapters) == pytest.approx(result["rationale"]["total_workload_units"])


def test_depth_changes_allocation_without_topic_specific_rules():
    concepts = inventory([f"Concept {i}" for i in range(14)])
    basic = plan_chapters(concepts)
    for concept in concepts:
        concept.update(depth={"mathematical": 4, "implementation": 4, "research": 4, "visual": 3},
                       examples=[{"id": "worked"}], assessments=[{"id": "check"}])
    demanding = plan_chapters(concepts)
    assert len(basic["chapters"]) == 5
    assert len(demanding["chapters"]) == 10
    assert demanding["rationale"]["scope_review_required"]
    assert demanding["rationale"]["total_workload_units"] > basic["rationale"]["total_workload_units"]


def test_prerequisite_order_overrides_input_and_group_preference():
    concepts = inventory([f"Concept {i}" for i in range(12)])
    for i, concept in enumerate(concepts):
        concept["group"] = "Early" if i % 2 else "Later"
        if i:
            concept["prerequisites"] = [{"id": f"c{i-1}", "classification": "essential"}]
    result = plan_chapters(list(reversed(concepts)))
    order = [cid for chapter in result["chapters"] for cid in chapter["concepts"]]
    assert order == [f"c{i}" for i in range(12)]
    assert result["rationale"]["concept_estimates"]["c11"]["prerequisite_depth"] == 11


def test_ready_concepts_prefer_coherent_groups_and_balance_load():
    concepts = inventory([f"Concept {i}" for i in range(25)])
    for i, concept in enumerate(concepts):
        concept["group"] = f"Group {i % 5}"
    result = plan_chapters(concepts)
    # Five contiguous groups can each occupy a chapter without mixing concepts.
    assert len(result["chapters"]) == 6  # Total burden requires a split of one group.
    assert result["rationale"]["split_groups"]
    assert all(len(chapter["estimate"]["groups"]) <= 2 for chapter in result["chapters"])
    loads = [chapter["estimate"]["units"] for chapter in result["chapters"]]
    assert max(loads) <= 2 * min(loads)


def test_fragments_merge_and_overloaded_groups_split_without_new_concepts():
    concepts = inventory([f"Concept {i}" for i in range(30)])
    for i, concept in enumerate(concepts):
        concept["group"] = "Broad group" if i < 20 else f"Small group {i}"
    result = plan_chapters(concepts)
    assert result["rationale"]["split_groups"]["Broad group"]
    assert result["rationale"]["merged_groups"]
    assert {cid for ch in result["chapters"] for cid in ch["concepts"]} == {concept["id"] for concept in concepts}


def test_external_known_optional_and_missing_prerequisites_remain_explicit():
    concepts = inventory([f"Concept {i}" for i in range(5)])
    concepts[0]["prerequisites"] = ["known", {"id": "optional", "classification": "optional"},
                                    {"id": "gap", "classification": "missing"}]
    result = plan_chapters(concepts, known_prerequisites=["known"])
    records = result["rationale"]["external_prerequisites"]
    assert len(records) == 3
    assert next(record for record in records if record["id"] == "known")["known"]
    assert next(record for record in records if record["id"] == "gap")["classification"] == "missing"


@pytest.mark.parametrize("fault", ["too_small", "duplicate", "empty_id", "title", "objective", "unknown", "cycle", "classification", "malformed"])
def test_invalid_inventories_fail_before_allocation(fault):
    concepts = inventory([f"Concept {i}" for i in range(5)])
    if fault == "too_small": concepts.pop()
    if fault == "duplicate": concepts[1]["id"] = "c0"
    if fault == "empty_id": concepts[0]["id"] = " "
    if fault == "title": concepts[0]["title"] = ""
    if fault == "objective": concepts[0]["objectives"] = [""]
    if fault == "unknown": concepts[0]["prerequisites"] = ["unregistered"]
    if fault == "cycle":
        concepts[0]["prerequisites"] = ["c1"]
        concepts[1]["prerequisites"] = ["c0"]
    if fault == "classification": concepts[0]["prerequisites"] = [{"id": "c1", "classification": "invented"}]
    if fault == "malformed": concepts[0]["prerequisites"] = "c1"
    with pytest.raises(ValueError):
        plan_chapters(concepts)


@pytest.mark.parametrize("count", [4, 11, True, 5.5])
def test_explicit_chapter_bounds(count):
    with pytest.raises(ValueError):
        validate_chapter_count(count)


def test_plan_is_repeatable_preserves_inputs_and_uses_safe_unique_titles():
    concepts = inventory(["CON", "CON", "A/B: geometry", "A/B: geometry", "Limits? More!", "Limits? More!"])
    before = deepcopy(concepts)
    first = plan_chapters(concepts)
    assert first == plan_chapters(concepts)
    assert concepts == before
    titles = [chapter["title"] for chapter in first["chapters"]]
    assert len(set(title.casefold() for title in titles)) == len(titles)
    assert all(not any(char in title for char in '<>:"/\\|?*') for title in titles)


def test_duplicate_dependencies_are_not_counted_twice():
    concepts = inventory([f"Concept {i}" for i in range(5)])
    concepts[1]["prerequisites"] = ["c0", "c0"]
    assert plan_chapters(concepts)["rationale"]["topological_order"][:2] == ["c0", "c1"]


def test_historical_objectives_do_not_receive_mathematical_requirements():
    concepts = inventory(["Trade networks", "Tax institutions", "Imperial authority", "Agrarian change", "Revolt"])
    for concept in concepts:
        concept["objectives"] = ["explain the historical development over time"]
    historical = plan_chapters(concepts)
    assert all(estimate["depth_levels"]["mathematical"] == 0
               for estimate in historical["rationale"]["concept_estimates"].values())
    mathematical = deepcopy(concepts)
    mathematical[0]["objectives"] = ["derive the coordinate transformation"]
    numeric = plan_chapters(mathematical)
    assert numeric["rationale"]["concept_estimates"]["c0"]["depth_levels"]["mathematical"] == 3
    assert numeric["rationale"]["concept_estimates"]["c0"]["units"] > historical["rationale"]["concept_estimates"]["c0"]["units"]


@pytest.mark.parametrize("known", ["one-id", None, [None], [{}]])
def test_malformed_known_prerequisites_have_actionable_failure(known):
    concepts = inventory([f"Concept {i}" for i in range(5)])
    with pytest.raises(ValueError, match="known_prerequisites"):
        plan_chapters(concepts, known_prerequisites=known)
