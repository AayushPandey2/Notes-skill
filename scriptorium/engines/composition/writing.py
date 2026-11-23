"""Canonical educational composition: plan, tutor, write, and validate one contract.

Inputs are source material and explicit teaching records. Missing educational
content stays an unmet obligation; the writer never invents a lesson to fill it.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any



@dataclass
class Composition:
    concept_id: str
    title: str
    master: str
    source_policy: str
    audience: str
    objectives: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    sections: list[tuple[str, str]] = field(default_factory=list)
    mathematics: list[dict] = field(default_factory=list)
    examples: list[dict] = field(default_factory=list)
    visuals: list[str] = field(default_factory=list)
    chapter: dict[str, Any] = field(default_factory=dict)
    assets: list[dict[str, Any]] = field(default_factory=list)
    inspections: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    assessments: list[dict[str, Any]] = field(default_factory=list)
    obligations: dict[str, str] = field(default_factory=dict)
    trace: list[dict] = field(default_factory=list)
    teaching: dict[str, Any] = field(default_factory=dict)
    bindings: dict[str, str] = field(default_factory=dict)
    mechanism: dict[str, Any] = field(default_factory=dict)
    depth_profile: dict[str, Any] = field(default_factory=dict)
    practical: dict[str, Any] = field(default_factory=dict)
    visual_requirements: list[dict[str, Any]] = field(default_factory=list)
    obligation_details: dict[str, Any] = field(default_factory=dict)

    def record(self, component: str, **details: Any) -> None:
        self.trace.append({"component": component, **details})

    def section(self, heading: str, content: Any) -> None:
        if isinstance(content, (list, tuple)):
            content = "\n\n".join(str(x).strip() for x in content if str(x).strip())
        text = str(content or "").strip()
        if text:
            self.sections.append((heading, text))


def plan_depth(blueprint: Any, facts: list[str]) -> Composition:
    context = blueprint.context
    ext = context.get("teaching_extensions") or {}
    plan = Composition(blueprint.concept_id, blueprint.topic,
                       context.get("selected_master", "M1"),
                       context.get("source_mode", "adaptive"),
                       context.get("audience_depth", "beginner"),
                       objectives=list(ext.get("objectives") or []),
                       prerequisites=[str(b.get("term")) for b in ext.get("prerequisite_bridges", [])
                                      if isinstance(b, dict) and b.get("term")],
                       mathematics=list(ext.get("equations") or []),
                       examples=list(ext.get("worked_problems") or []),
                       visuals=list(ext.get("visual_walkthroughs") or []))
    for name in ("chapter", "assets", "inspections", "evidence", "assessments", "visual_requirements"):
        if name in ext:
            setattr(plan, name, ext[name])
    if plan.assets and len(plan.inspections) != len(plan.assets):
        raise ValueError("Every acquired visual requires an inspection record before writing")
    for asset, inspection in zip(plan.assets, plan.inspections):
        if not inspection.get("inspection_performed") or not asset.get("hash") or inspection.get("content_hash") != asset["hash"]:
            raise ValueError("Image inspection must bind the exact acquired asset hash")
    from .learning import configure
    configure(plan, ext, context)
    plan.record("composition.writing.plan_depth", required=list(plan.obligations),
                source_facts=len(facts), master=plan.master)
    return plan


def teach(plan: Composition, blueprint: Any, facts: list[str]) -> None:
    """Select teaching material in prerequisite order, before formal notation."""
    ext = blueprint.context.get("teaching_extensions") or {}
    spine = blueprint.explanatory_spine
    if plan.teaching:
        from .learning import text, mechanism_text
        for role, heading in (("why", "The Problem and Its Motivation"), ("intuition", "An Intuitive Starting Point")):
            plan.section(heading, text(plan.teaching.get(role)))
        for bridge in ext.get("prerequisite_bridges", []):
            if isinstance(bridge, dict):
                plan.section("Building the Needed Foundations", f"### {bridge.get('term', 'Foundation')}\n\n{bridge.get('explanation', '')}")
        plan.section("Meaning and Components", text(plan.teaching.get("what")))
        plan.section("Inside the Mechanism", [text(plan.teaching.get("how")), mechanism_text(plan.mechanism)])
        plan.record("composition.writing.teach", ordering="problem-to-mechanism", prior_concepts=plan.prerequisites)
        return
    if ext.get("sections"):
        for section in ext["sections"]:
            if not isinstance(section, dict) or not section.get("heading") or not section.get("content"):
                raise ValueError("Authored sections require a heading and substantive content")
            plan.section(section["heading"], section["content"])
        plan.record("composition.writing.teach", ordering="authored-concept-plan")
        return
    if blueprint.context.get("preserve_source_order") and facts:
        plan.section("Source Context & Overview", f"Source material for {plan.title}.")
        plan.section("Sequential Development", facts)
        plan.record("composition.writing.teach", ordering="source")
        return
    if plan.master == "M3":
        plan.section("Core Reference", facts or [blueprint.retrieval.get("summary") or plan.title])
    else:
        plan.section("Why This Matters & Starting Problem",
                     [spine.get("starting_problem", ""), spine.get("obstacle", ""),
                      ext.get("familiar_anchor", "")])
        if blueprint.central_question.get("explicit_in_prose"):
            plan.section("The Guiding Question", blueprint.central_question.get("question"))
        plan.section("Intuitive Picture Before Any Formalism", ext.get("starting_intuition"))
        plan.section("Where the Intuition Stops", ext.get("analogy_limit"))
        bridges = []
        for bridge in ext.get("prerequisite_bridges", []):
            if isinstance(bridge, dict):
                if bridge.get("explanation"):
                    bridges.append(f"### {bridge.get('term', 'Foundation')}\n\n{bridge['explanation']}")
            else:
                bridges.append(str(bridge))
        plan.section("Building the Needed Foundations", bridges)
        plan.section("How the Mechanism Works", facts or
                     [spine.get(k, "") for k in ("necessary_insight", "mechanism", "result")])
        steps = blueprint.mathematical_motivation.get("steps") or []
        plan.section("Stepping Into the Mathematical Idea", [
            f"### Step {i}: {step.get('operation', 'Reasoning').replace('_', ' ').title()}\n\n"
            f"{step.get('goal', '')} {step.get('mathematical_basis', '')}\n\n"
            f"{step.get('result', '')}\n\n{step.get('interpretation', '')} {step.get('next_purpose', '')}"
            for i, step in enumerate(steps, 1)])
    if blueprint.variable_roles:
        rows = ["| Symbol | Meaning | Operational Role | Effect of Change |", "|---|---|---|---|"]
        rows += [f"| `{v['symbol']}` | {v['meaning']} | {v.get('role', '')} | {v.get('effect', '')} |"
                 for v in blueprint.variable_roles]
        plan.section("Roles of Key Quantities", "\n".join(rows))
    plan.record("composition.writing.teach", ordering="prerequisite-before-formalism")


def write(plan: Composition, blueprint: Any) -> str:
    from scriptorium.engines.mathematics import deconstruct_equation, build_worked_solution
    ext = blueprint.context.get("teaching_extensions") or {}
    for raw_equation in plan.mathematics:
        equation = dict(raw_equation)
        if ext.get("require_complete"):
            required = {1, 2, 4, 11, 12}
            if equation.get("symbols"): required.add(3)
            if equation.get("numerical_example"): required.add(6)
            if "mathematical_reasoning" in plan.obligations: required.add(9)
            equation["required_stages"] = sorted(required | set(equation.get("required_stages", [])))
        plan.section("Formal Formulation and Mathematical Breakdown",
                     deconstruct_equation(equation, learner_level=plan.audience)["markdown"])
        plan.record("mathematics.deconstruct_equation", equation=equation.get("equation"))
    for example in plan.examples:
        plan.section("Worked Examples", build_worked_solution(example, learner_level=plan.audience)["markdown"])
        plan.record("mathematics.build_worked_solution")
    for walkthrough in plan.visuals:
        plan.section("Visual Explanation", walkthrough)
    from .learning import render_practical, render_assessments, text
    if plan.practical:
        plan.section("Practical Laboratory", render_practical(plan))
    if plan.teaching:
        plan.section("Applying the Idea", text(plan.teaching.get("apply")))
        plan.section("Choosing This Approach", text(plan.teaching.get("when_use")))
        plan.section("Boundaries and Alternatives", text(plan.teaching.get("when_not_use")))
        plan.section("Reconstructing the Reasoning", text(plan.teaching.get("reinforcement")))
    if plan.assessments:
        plan.section("Check Your Understanding", render_assessments(plan))
    if plan.source_policy == "strict" and blueprint.context.get("preserve_source_order"):
        plan.record("composition.writing.write", sections=len(plan.sections), source_only=True)
        return f"# {plan.title}\n\n" + "\n\n".join(
            f"## {heading}\n\n{text}" for heading, text in plan.sections) + "\n"
    state = blueprint.execution_state
    if state.get("applicable") and state.get("example_trace"):
        columns = list(state["example_trace"][0])
        rows = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
        rows += ["| " + " | ".join(str(row[c]) for c in columns) + " |" for row in state["example_trace"]]
        invariant = state.get("invariant", {})
        plan.section("Step-by-Step State Evolution", [invariant.get("statement", ""), "\n".join(rows)])
    for comparison in ext.get("comparisons", []):
        if isinstance(comparison, dict):
            parts = []
            if comparison.get("causal_explanation"):
                parts.append(str(comparison["causal_explanation"]).strip())
            dim_labels = (
                ("suitability", "Suitability"),
                ("assumptions", "Assumptions"),
                ("mechanism", "Mechanism"),
                ("strengths", "Strengths"),
                ("limitations", "Limitations"),
                ("resources", "Resources"),
                ("reliability", "Reliability"),
                ("interpretability", "Interpretability"),
                ("practical_constraints", "Practical constraints"),
            )
            dim_lines = [f"- **{label}:** {comparison[k]}" for k, label in dim_labels if comparison.get(k)]
            if dim_lines:
                parts.append("\n".join(dim_lines))
            if comparison.get("table"):
                parts.append(str(comparison["table"]).strip())
            plan.section(comparison.get("title", "Comparing Alternatives and Selecting a Method"), parts)
        else:
            plan.section("Comparing Alternatives and Selecting a Method", comparison)
    boundaries = blueprint.boundaries
    caveats = [f"- **Required condition:** {x}" for x in boundaries.get("required_conditions", [])]
    caveats += [f"- **Limitation (when not to use):** {x}" for x in boundaries.get("known_limitations", [])]
    caveats += [f"- **{c['concept_a']} vs. {c['concept_b']}:** {c['distinction']} "
                f"(Example: {c.get('discriminating_example', '')})" for c in blueprint.contrasts]
    caveats += [f"- **Common misconception:** {x}" for x in ext.get("misconceptions", [])]
    if not boundaries.get("minimal_caveats_only") and not any(h == "Applicability Conditions, Misconceptions, and Distinctions" for h, _ in plan.sections):
        plan.section("Applicability Conditions, Misconceptions, and Distinctions", "\n".join(caveats))
    plan.section("Practical Application", ext.get("practical_application"))
    retrieval = blueprint.retrieval
    if retrieval.get("enabled") and not retrieval.get("internal_only") and not any(h == "Reconstructing the Reasoning" for h, _ in plan.sections):
        plan.section("Reconstructing the Reasoning", ["Key cues: " + " → ".join(retrieval.get("cues", [])),
                                                     retrieval.get("summary", "")])
    plan.section("Next Connection", ext.get("transition"))
    plan.record("composition.writing.write", sections=len(plan.sections))
    return f"# {plan.title}\n\n" + "\n\n".join(f"## {heading}\n\n{text}" for heading, text in plan.sections) + "\n"


def validate(plan: Composition, body: str) -> dict:
    from .learning import verify
    report = verify(plan, body)
    plan.record("composition.writing.validate", formula_gate=report["mathematics"]["passed"])
    if not report["mathematics"]["passed"]:
        raise ValueError("Formula teaching gate failed: " + "; ".join(i["description"] for i in report["mathematics"]["issues"]))
    return report


def compose_explanation_note(blueprint: Any, *, source_facts: list[str] | None = None,
                             domain_override: str | None = None,
                             master_topic_override: str | None = None) -> str:
    """Execute the canonical Writer; never fall back to a prior prose generator."""
    from scriptorium.engines.vault import build_obsidian_properties, render_note_with_properties
    kinds = {"M1": "deep-notes", "M2": "study-notes", "M3": "quick-reference",
             "M4": "worked-solutions", "M5": "implementation-guide", "M6": "assessment", "M7": "synthesis-revision"}
    facts = list(source_facts or [])
    plan = plan_depth(blueprint, facts)
    teach(plan, blueprint, facts)
    body = write(plan, blueprint)
    report = validate(plan, body)
    blueprint.context["composition_result"] = {"trace": plan.trace, "validation": report, "contract": asdict(plan)}
    if (blueprint.context.get("teaching_extensions") or {}).get("require_complete") and not report["complete"]:
        pending = [key for key, status in report["obligations"].items() if status == "pending"]
        raise ValueError("Teaching obligations remain pending: " + ", ".join(pending))
    properties = build_obsidian_properties(topic=plan.title, note_type=kinds[plan.master],
                                           domain=domain_override, master_topic=master_topic_override,
                                           concept_ids=[plan.concept_id], source_mode=plan.source_policy)
    return render_note_with_properties(properties, body)


def compose_chapter(
    node: Any,
    plan: Any,
    node_map: dict[str, Any],
    preferences: Any,
    *,
    domain: str,
    master_topic: str,
    source_facts: list[str] | None = None,
    visual_walkthroughs: list[str] | None = None,
    teaching_extensions: dict[str, Any] | None = None,
    created: str | date | None = None,
    execution_report: dict | None = None,
) -> str:
    """Compose a full adaptive child or single note using EIS-01..EIS-07 + M1-M7 + Obsidian Properties."""
    from datetime import date
    from scriptorium.models import parse_note, slugify
    from scriptorium.engines.vault import _master_to_note_type, build_obsidian_properties, render_note_with_properties
    from scriptorium.engines.pedagogy import build_explanation_blueprint

    tpl = node.template_plan or {}
    master = str(tpl.get("master") or preferences.master or "M1")
    variant = tpl.get("variant") if "variant" in tpl else preferences.variant
    note_type = str(tpl.get("note_type") or _master_to_note_type(master, variant))

    parent_node = node_map.get(node.parent_id) if node.parent_id else None
    prereq_titles = [node_map[pid].title if pid in node_map else pid for pid in node.prerequisite_ids]
    related_titles = [node_map[rid].title if rid in node_map else rid for rid in node.related_ids]

    ctx = {
        **(teaching_extensions or {}),
        "transition": (
            (teaching_extensions or {}).get("transition")
            or f"With this foundation on {node.title} established, connect these assumptions to related topics"
            + (f" such as [[{related_titles[0]}]]" if related_titles else "")
            + "."
        ),
    }
    if visual_walkthroughs:
        ctx["visual_walkthroughs"] = list(visual_walkthroughs)

    bp = build_explanation_blueprint(
        node.title,
        concept_id=node.concept_id,
        master=master,
        audience=preferences.depth,
        source_mode=preferences.source_policy,
        preserve_source_order=preferences.preserve_source_order,
        source_facts=source_facts,
        prerequisites=prereq_titles,
        context=ctx,
    )
    composed = compose_explanation_note(
        bp,
        source_facts=source_facts,
        domain_override=domain,
        master_topic_override=master_topic,
    )
    if execution_report is not None:
        execution_report.update(bp.context.get("composition_result", {}))
    parsed = parse_note(composed)
    body = parsed.body.strip()

    # Add non-duplicative Obsidian navigation block
    nav_lines: list[str] = []
    if parent_node:
        nav_lines.append(f"- **Parent:** [[{parent_node.title}]]")
    if prereq_titles:
        nav_lines.append("- **Prerequisites:** " + ", ".join(f"[[{t}]]" for t in prereq_titles))
    if related_titles:
        nav_lines.append("- **Related:** " + ", ".join(f"[[{t}]]" for t in related_titles))
    if node.source_bindings:
        bound = ", ".join(str(b.get("section") or b.get("source") or "") for b in node.source_bindings if b)
        if bound:
            nav_lines.append(f"- **Source Coverage:** {bound}")
    if nav_lines:
        body += "\n\n## Navigation\n" + "\n".join(nav_lines)

    props = build_obsidian_properties(
        topic=node.title,
        note_type=note_type,
        domain=domain,
        master_topic=master_topic,
        content=body,
        parent_topic=parent_node.title if parent_node else None,
        collection_id=plan.collection_id,
        concept_ids=[node.concept_id],
        prerequisites=prereq_titles or None,
        related=related_titles or None,
        source_mode=preferences.source_policy,
        source_refs=[str(b.get("section") or b.get("source")) for b in node.source_bindings if b] or None,
        difficulty=preferences.depth,
        status="active",
        created=created or date.today(),
        template_id=master,
        coverage_status="generated",
    )
    return render_note_with_properties(props, body + "\n")


