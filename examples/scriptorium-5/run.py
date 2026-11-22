"""Reproduce real plans and visual artifacts, without certifying unwritten notes."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scriptorium.engines.composition import build_composition
from scriptorium.engines.composition.visuals import render_visuals, validate_svg
from scriptorium.engines.orchestration import route_request
from scriptorium.models import slugify

HERE = Path(__file__).resolve().parent
VAULT = HERE / "vault"


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def inventory(prefix, entries, depth):
    """Example data only: all allocation behavior lives in the production planner."""
    identifiers = [prefix + "." + slugify(row[0]) for row in entries]
    return [{"id": identifiers[i], "title": title, "section": title, "objectives": [goal],
             "group": group, "depth": depth, "capabilities": ["S01"],
             "prerequisites": [identifiers[index] for index in parents]}
            for i, (title, goal, group, parents) in enumerate(entries)]


def specifications():
    math_concepts = inventory("calc", [
        ("Vectors and Euclidean Distance", "Explain vectors and the Euclidean norm", "Geometric Foundations", []),
        ("Limits in Several Variables", "Explain path dependence in multivariable limits", "Geometric Foundations", [0]),
        ("Partial Derivatives", "Derive partial derivatives from one-variable slices", "Local Variation", [1]),
        ("Differentiability", "Explain the linear approximation and its remainder", "Local Variation", [2]),
        ("The Gradient", "Derive the gradient representation of directional derivatives", "Local Variation", [0, 3]),
        ("The Multivariable Chain Rule", "Derive the chain rule using Jacobian composition", "Composing Maps", [3]),
        ("Tangent Planes", "Explain tangent planes through a local affine approximation", "Local Geometry", [4]),
        ("The Hessian", "Derive second-order approximations and the Hessian", "Local Geometry", [2, 4]),
        ("Stationary Points", "Analyze stationary points using Hessian eigenvalues", "Optimization", [7]),
        ("Constrained Extrema", "Derive Lagrange multiplier stationarity conditions", "Optimization", [4, 8]),
        ("Descent Directions", "Explain why a negative gradient is a descent direction", "Optimization", [4]),
        ("Finite Step Stability", "Derive a quadratic descent stability interval", "Optimization", [7, 10]),
        ("Boundary and Singular Cases", "Analyze cases where second-order tests are inconclusive", "Scope and Limitations", [8, 9]),
    ], {"conceptual": 2, "mathematical": 3, "analytical": 2, "visual": 1})
    ai_concepts = inventory("attention", [
        ("Token Sequences", "Explain token indices and sequence boundaries", "Inputs", []),
        ("Embeddings", "Explain learned token embeddings and batch dimensions", "Inputs", [0]),
        ("Positional Information", "Compare absolute and relative positional information", "Inputs", [1]),
        ("Query Key and Value Projections", "Derive projection dimensions for attention heads", "Attention Mechanics", [1]),
        ("Scaled Dot Products", "Derive the matrix of query-key compatibility scores", "Attention Mechanics", [3]),
        ("Masked Normalization", "Explain masking before row-wise softmax", "Attention Mechanics", [4]),
        ("Value Aggregation", "Derive attention output dimensions and weighted sums", "Attention Mechanics", [5]),
        ("Multiple Heads", "Explain head concatenation and output projection", "Transformer Blocks", [6]),
        ("Residual Paths", "Explain residual information paths in a transformer block", "Transformer Blocks", [7]),
        ("Normalization", "Compare pre-normalized and post-normalized residual blocks", "Transformer Blocks", [8]),
        ("Feed Forward Sublayers", "Explain position-wise nonlinear transformations", "Transformer Blocks", [8]),
        ("Causal Decoding", "Explain autoregressive context visibility during decoding", "Execution", [5, 10]),
        ("Key Value Caching", "Implement an explicit key-value cache interface", "Execution", [11]),
        ("Training Labels", "Explain shifted labels and padded-token exclusion", "Training and Verification", [0, 12]),
        ("Gradient Flow", "Analyze gradient ownership through shared projections", "Training and Verification", [9, 13]),
        ("Memory and Runtime", "Analyze attention storage and dense operation counts", "Training and Verification", [4, 12]),
        ("Evidence and Model Limits", "Compare source-reported results with implementation evidence", "Training and Verification", [14, 15]),
    ], {"conceptual": 3, "mathematical": 2, "implementation": 2, "research": 2, "visual": 2})
    engineering = inventory("dc", [
        ("Charge Current and Voltage", "Explain charge flow and potential difference", "Circuit Quantities", []),
        ("Reference Directions", "Explain voltage polarity and passive sign convention", "Circuit Quantities", [0]),
        ("Ideal Resistors", "Explain the resistance model and its valid operating range", "Lumped Models", [1]),
        ("Ideal Sources", "Compare ideal voltage and current source constraints", "Lumped Models", [0, 1]),
        ("Kirchhoff Current Law", "Derive nodal current balance from charge conservation", "Conservation Laws", [0, 1]),
        ("Kirchhoff Voltage Law", "Derive loop voltage balance under lumped-circuit assumptions", "Conservation Laws", [1, 3]),
        ("Series Networks", "Derive series resistance from a common branch current", "Network Reduction", [2, 4, 5]),
        ("Parallel Networks", "Derive parallel resistance from common terminal voltage", "Network Reduction", [2, 4]),
        ("Voltage Division", "Derive the unloaded voltage-divider relation", "Network Reduction", [6]),
        ("Nodal Equations", "Derive and solve a grounded nodal conductance system", "Systematic Analysis", [4, 7]),
        ("Power Balance", "Analyze absorbed and supplied power using declared signs", "Verification", [1, 9]),
        ("Model Boundary Cases", "Analyze open circuits, short circuits and invalid idealizations", "Verification", [3, 10]),
    ], {"conceptual": 2, "mathematical": 2, "visual": 2, "research": 1})
    computer_science = inventory("binary", [
        ("Sorted Search Contract", "Explain ordering and the required search result", "Search Contract", []),
        ("Half Open Intervals", "Explain a half-open search interval", "Search Contract", [0]),
        ("Loop Invariant", "Explain how the active interval retains every candidate", "Correctness", [1]),
        ("Choosing the Midpoint", "Explain overflow-safe midpoint selection", "State Transitions", [1]),
        ("Moving the Lower Bound", "Trace lower-bound changes after a small midpoint value", "State Transitions", [2, 3]),
        ("Moving the Upper Bound", "Trace upper-bound changes after a large midpoint value", "State Transitions", [2, 3]),
        ("Finding a Match", "Trace successful termination on an equal midpoint value", "Termination", [4, 5]),
        ("Empty Search Intervals", "Explain unsuccessful termination and empty input", "Termination", [2, 4, 5]),
        ("Cost and Boundary Tests", "Analyze comparison count and boundary cases", "Verification", [6, 7]),
    ], {"conceptual": 2, "algorithmic": 2, "implementation": 1})
    history = inventory("revolution", [
        ("Late Bourbon Political Order", "Explain the institutions of the late Bourbon monarchy", "Historical Context", []),
        ("Fiscal Crisis and Representation", "Explain the link between fiscal conflict and demands for representation", "Historical Context", [0]),
        ("The Estates General", "Explain the transition from the Estates-General to the National Assembly", "Constitutional Change", [1]),
        ("Assembly and Popular Mobilization", "Explain interactions between institutional change and popular mobilization", "Constitutional Change", [2]),
        ("Constitutional Monarchy", "Explain tensions within the constitutional-monarchy settlement", "Regime Change", [3]),
        ("The Republic", "Explain the transition to a republic without assuming historical inevitability", "Regime Change", [4]),
        ("Historical Evidence and Causation", "Compare competing historical explanations using source scope and chronology", "Interpretation", [0, 5]),
    ], {"conceptual": 2, "research": 1})
    return [
        {"topic": "Multivariable Differential Calculus", "classification": {"subject": "Calculus", "domain": "Mathematics"}, "concepts": math_concepts},
        {"topic": "Transformer Attention Mechanics", "classification": {"subject": "Deep Learning", "domain": "Artificial Intelligence"}, "concepts": ai_concepts},
        {"topic": "DC Resistive Circuit Analysis", "classification": {"subject": "Circuit Theory", "domain": "Engineering"}, "concepts": engineering},
        {"topic": "Binary Search with Half Open Intervals", "classification": {"subject": "Algorithms", "domain": "Computer Science"}, "concepts": computer_science},
        {"topic": "French Revolution Political Transitions", "classification": {"subject": "Modern European History", "domain": "History"}, "concepts": history},
    ]


def executed_search_trace():
    values, target, low, high, states, answer = [1, 4, 7, 10, 13, 16, 19], 13, 0, 7, [], -1
    while low < high:
        midpoint = low + (high-low)//2
        candidate = values[midpoint]
        branch = "found" if candidate == target else "raise low" if candidate < target else "lower high"
        states.append({"low": low, "high_exclusive": high, "midpoint": midpoint, "candidate": candidate, "decision": branch})
        if candidate == target:
            answer = midpoint
            break
        if candidate < target:
            low = midpoint+1
        else:
            high = midpoint
    assert answer == values.index(target) == 4
    assert [(s["low"], s["high_exclusive"], s["midpoint"]) for s in states] == [(0, 7, 3), (4, 7, 5), (4, 5, 4)]
    return {"inputs": values, "target": target, "states": states, "answer_index": answer,
            "classification": "executed deterministic algorithm trace, not model execution"}


def demo_visuals(spec, trace):
    concepts = spec["concepts"]
    def representation(index, name, kind, objective, interpretation, **fields):
        return {"id": name, "concept": concepts[index]["id"], "section": concepts[index]["section"], "kind": kind,
                "objective": objective, "interpretation": interpretation, **fields}
    topic = spec["topic"]
    if topic.startswith("Multivariable"):
        return [
            representation(0, "euclidean-triangle", "geometry", "Inspect a 3-4-5 Euclidean triangle", "Coordinates use the same scale on both axes; this is an exact synthetic geometric construction.",
                           units="dimensionless", nodes=[{"id": "O", "label": "Origin", "x": 0, "y": 0}, {"id": "A", "label": "Horizontal leg", "x": 3, "y": 0}, {"id": "B", "label": "Hypotenuse endpoint", "x": 3, "y": 4}],
                           edges=[{"source": "O", "target": "A"}, {"source": "A", "target": "B"}, {"source": "O", "target": "B"}]),
            representation(11, "quadratic-cross-section", "equation", "Inspect a quadratic objective cross-section", "Only objective values are shown; the slope requires a separate derivative calculation. All points are computed from the stated expression, not measured data.",
                           equation="x*x/2", x_values=[-3, -2, -1, 0, 1, 2, 3], xlabel="scalar x", ylabel="objective x^2 / 2", units="dimensionless"),
        ]
    if topic.startswith("Transformer"):
        return [
            representation(6, "attention-interfaces", "architecture", "Track the shapes of one attention head", "This schematic specifies interfaces; it does not claim a model forward pass was executed.",
                           components=[{"label": "Scaled QK-transpose", "shape": "B,T_q,T_k"}, {"label": "Row-wise softmax", "shape": "B,T_q,T_k"}, {"label": "Multiply by V", "shape": "B,T_q,d_v"}]),
            representation(3, "projection-shapes", "table", "Resolve compatible projection dimensions", "T_q and T_k may differ in cross-attention; the contraction requires matching d_k.",
                           table={"type": "architecture", "objective": "One-head attention interfaces", "interpretation": "Symbols specify dimensions, not observed tensors.", "rows": [
                               {"component": "Score product", "input": "Q: B,T_q,d_k; K: B,T_k,d_k", "output": "B,T_q,T_k", "operation": "Q times transpose(K) / sqrt(d_k)"},
                               {"component": "Weighted values", "input": "A: B,T_q,T_k; V: B,T_k,d_v", "output": "B,T_q,d_v", "operation": "A times V"}]}),
        ]
    if topic.startswith("DC"):
        return [representation(8, "voltage-divider-connectivity", "circuit", "Inspect an unloaded series-divider connectivity graph", "This directed graph records connectivity and the chosen loop direction, not circuit symbols or a circuit simulation. R1=2 kOhm, R2=1 kOhm, Vs=12 V imply Vout=4 V for an ideal unloaded divider.",
                               nodes=[{"id": "supply", "label": "Vs positive: 12 V"}, {"id": "r1", "label": "R1: 2 kOhm"}, {"id": "tap", "label": "Vout: unloaded"}, {"id": "r2", "label": "R2: 1 kOhm"}, {"id": "ground", "label": "Ground and Vs negative"}],
                               edges=[{"source": "supply", "target": "r1"}, {"source": "r1", "target": "tap"}, {"source": "tap", "target": "r2"}, {"source": "r2", "target": "ground"}, {"source": "ground", "target": "supply"}])]
    if topic.startswith("Binary"):
        states = trace["states"]
        return [
            representation(6, "executed-search-states", "algorithm", "Trace an executed search for 13", "The states below were produced by the binary-search implementation in this reproduction script, with high always exclusive.",
                           nodes=[{"id": f"s{i}", "label": f"[{s['low']},{s['high_exclusive']}) mid={s['midpoint']}: {s['decision']}"} for i, s in enumerate(states)],
                           edges=[{"source": f"s{i}", "target": f"s{i+1}"} for i in range(len(states)-1)]),
            representation(6, "search-step-viewer", "interactive", "Step through the executed binary-search trace", "This HTML slider displays observed algorithm states. It executes no user-provided code and is opened as a standalone file.",
                           frames=[{"label": f"Step {i+1}: {s['decision']}", "state": json.dumps({"values": trace["inputs"], "target": trace["target"], **s}, indent=2)} for i, s in enumerate(states)]),
            representation(2, "search-control-flow", "workflow", "Inspect control flow for half-open binary search", "Native Mermaid source is generated and checked against bounded semantic nodes and edges; browser rendering is not asserted.",
                           nodes=[{"id": "interval", "label": "Check low < high"}, {"id": "mid", "label": "Inspect midpoint"}, {"id": "found", "label": "Return matching index"}, {"id": "bounds", "label": "Update a bound"}, {"id": "missing", "label": "Return not found"}],
                           edges=[{"source": "interval", "target": "mid", "label": "nonempty"}, {"source": "interval", "target": "missing", "label": "empty"}, {"source": "mid", "target": "found", "label": "equal"}, {"source": "mid", "target": "bounds", "label": "unequal"}, {"source": "bounds", "target": "interval", "label": "repeat"}]),
        ]
    return [representation(5, "political-transition-chronology", "chronology", "Separate the order of political transitions from a causal explanation", "This selective schematic orders major political forms. An arrow records sequence, not inevitability, a single cause, or a complete account of the French Revolution. Dates and source-level historical interpretations are outside this renderer demonstration.",
                           nodes=[{"id": "monarchy", "label": "Late Bourbon monarchy"}, {"id": "estates", "label": "Estates-General"}, {"id": "assembly", "label": "National Assembly"}, {"id": "constitutional", "label": "Constitutional monarchy"}, {"id": "republic", "label": "Republic"}],
                           edges=[{"source": "monarchy", "target": "estates"}, {"source": "estates", "target": "assembly"}, {"source": "assembly", "target": "constitutional"}, {"source": "constitutional", "target": "republic"}])]


def main():
    started = time.perf_counter()
    trace = executed_search_trace()
    assert math.hypot(3, 4) == 5
    assert 12 * 1000 / (2000+1000) == 4
    save_json(HERE / "executed-search-trace.json", trace)
    receipts, allocations, source_bytes, asset_bytes, cache_hits = {}, [], 0, 0, 0
    for spec in specifications():
        slug = slugify(spec["topic"])
        spec["visuals"] = demo_visuals(spec, trace)
        plan = build_composition(spec)
        # The plans intentionally retain all unfulfilled teaching obligations.
        # Preparing a visual does not certify uncreated instructional chapters.
        save_json(HERE / "plans" / f"{slug}.json", {"delivery_state": "planned", "teaching_collection_complete": False,
                  "input_specification": spec, "canonical_composition_plan": plan})
        drafts = {chapter["id"]: "\n\n".join("## " + section for section in dict.fromkeys(
            visual["section"] for visual in plan["visuals"] if visual["concept"] in chapter["concepts"])) + "\n"
                  for chapter in plan["chapters"]}
        bodies, results = render_visuals(VAULT, plan, drafts)
        failures = {name: result for name, result in results.items() if result["status"] != "verified"}
        assert not failures, failures
        offline = render_visuals(VAULT, plan, bodies, execute=False)[1]
        assert all(result["status"] == "verified" for result in offline.values())
        assert all(results[name]["hash"] == result["hash"] for name, result in offline.items())
        owners = {chapter["id"] for chapter in plan["chapters"] for visual in plan["visuals"] if visual["concept"] in chapter["concepts"]}
        gallery = "# " + spec["topic"] + " — prepared visual demonstration\n\n"
        gallery += "These are actual prepared representations. The associated adaptive chapter plan remains planned; no complete teaching collection or semantic review is claimed.\n\n"
        gallery += "\n\n".join(bodies[chapter["id"]] for chapter in plan["chapters"] if chapter["id"] in owners)
        gallery_path = VAULT / plan["folder"] / "Visual Demo.md"
        gallery_path.parent.mkdir(parents=True, exist_ok=True)
        gallery_path.write_text(gallery.rstrip() + "\n", encoding="utf-8")
        for result in results.values():
            artifact = VAULT / result["path"]
            asset_bytes += artifact.stat().st_size
            cache_hits += bool(result["cached"])
            if artifact.suffix == ".svg":
                assert not validate_svg(artifact.read_text(encoding="utf-8"))
        source_bytes += gallery_path.stat().st_size
        receipts[slug] = {"teaching_collection_complete": False, "renderers": results, "offline_verification": "passed without network acquisition"}
        allocations.append({"topic": spec["topic"], "concept_count": len(spec["concepts"]), "chapter_count": len(plan["chapters"]),
                            "scope_review_required": plan["chapter_rationale"].get("scope_review_required", False),
                            "workload_units": plan["chapter_rationale"]["total_workload_units"], "visuals": len(results),
                            "gallery": gallery_path.relative_to(HERE).as_posix()})
    narrow_request = "Give me a one-sentence quick reference definition of a derivative, without diagrams or implementation"
    narrow = route_request(narrow_request, source_policy="strict")
    assert narrow["master"] == "M3", narrow
    save_json(HERE / "narrow-route.json", {"request": narrow_request, "actual_route": narrow,
              "rendering_calls": 0, "research_retrieval_calls": 0, "notes_authored": 0})
    save_json(HERE / "renderer-receipts.json", receipts)
    measurements = {"measured_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
                    "command": "python examples/scriptorium-5/run.py", "elapsed_seconds": time.perf_counter()-started,
                    "actual_render_calls": len(allocations)*2, "artifacts": sum(row["visuals"] for row in allocations),
                    "acquisition_or_render_cache_hits": cache_hits,
                    "verified_artifact_bytes": asset_bytes, "gallery_utf8_bytes": source_bytes,
                    "allocations": allocations, "network_calls": 0, "teaching_collections_completed": 0,
                    "comparison_baseline": None, "limits": "Single local run; no model-token, speedup, browser, live media or complete-collection performance claim."}
    save_json(HERE / "measurements.json", measurements)
    print(json.dumps(measurements, indent=2))


if __name__ == "__main__":
    main()
