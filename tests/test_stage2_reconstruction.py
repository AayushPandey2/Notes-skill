"""Stage 2 reconstruction integration & regression tests for Scriptorium 6.0 core engines."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import plan_notes
from scriptorium.engines.composition import (
    build_composition,
    bvia,
    compile_context,
    five_key_note,
    lavia,
    prepare_composition,
    publish_composition,
    validate_chapter,
    validate_published_composition,
)
from scriptorium.engines._interactive import ResolvedNotePreferences
from scriptorium.engines.orchestration import OrchestrationEngine, lint_instruction_authority, route_request
from scriptorium.engines.pedagogy import PedagogyEngine
from scriptorium.engines.research import ResearchEngine
from scriptorium.models import content_hash, heading_slug, parse_note


def _transformer_spec(
    *,
    web_image_first: bool = True,
    organize_by_collection: bool = True,
    embed_style: str = "wikilink",
    learner_level: str = "beginner",
    enforce_bvia_walkthrough: bool = False,
) -> dict:
    chapters = [
        {"id": "ch1", "title": "Tokenization and Embeddings", "concepts": ["tf.c1"], "sections": ["Input Representations"]},
        {"id": "ch2", "title": "Positional Encoding", "concepts": ["tf.c2"], "sections": ["Sinusoidal Encoding"]},
        {"id": "ch3", "title": "Scaled Dot-Product Attention", "concepts": ["tf.c3"], "sections": ["Attention Mechanism"]},
        {"id": "ch4", "title": "Multi-Head Attention", "concepts": ["tf.c4"], "sections": ["Parallel Subspaces"]},
        {"id": "ch5", "title": "Encoder-Decoder Stack", "concepts": ["tf.c5"], "sections": ["Full Architecture"]},
    ]
    concepts = [
        {
            "id": "tf.c1",
            "title": "Token Embeddings",
            "section": "Input Representations",
            "objectives": ["explain how discrete tokens map to continuous vectors"],
            "capabilities": ["S01"],
            "prerequisites": [],
        },
        {
            "id": "tf.c2",
            "title": "Sinusoidal Positional Encoding",
            "section": "Sinusoidal Encoding",
            "objectives": ["explain sinusoidal position signals", "visualize positional scaling behavior"],
            "capabilities": ["S01", "S12"],
            "depth": {"visual": 2},
            "visual_review": {
                "objective": "Show smooth positional scaling across token indices",
                "difficulty": "Position curves are easier to grasp graphically than from raw sums",
                "representation": "scientific curve",
                "placement": "Sinusoidal Encoding",
                "validation": "equation and axes",
            },
            "prerequisites": ["tf.c1"],
        },
        {
            "id": "tf.c3",
            "title": "Scaled Dot-Product Attention",
            "section": "Attention Mechanism",
            "objectives": ["explain query-key-value attention weights"],
            "capabilities": ["S01"],
            "prerequisites": ["tf.c2"],
        },
        {
            "id": "tf.c4",
            "title": "Multi-Head Attention",
            "section": "Parallel Subspaces",
            "objectives": ["explain multi-head projection and concatenation"],
            "capabilities": ["S01"],
            "prerequisites": ["tf.c3"],
        },
        {
            "id": "tf.c5",
            "title": "Transformer Encoder-Decoder Stack",
            "section": "Full Architecture",
            "objectives": ["explain end-to-end encoder-decoder block composition", "visualize encoder-decoder block shapes"],
            "capabilities": ["S01", "S12"],
            "depth": {"visual": 2},
            "visual_review": {
                "objective": "Show end-to-end encoder-decoder tensor interfaces",
                "difficulty": "Multi-block residual shapes are clarified by an architecture schematic",
                "representation": "architecture diagram",
                "placement": "Full Architecture",
                "validation": "component labels and tensor shapes",
            },
            "prerequisites": ["tf.c4"],
        },
    ]
    concepts_by_id = {c["id"]: c for c in concepts}
    assessments = []
    for i, ch in enumerate(chapters, 1):
        cid = ch["concepts"][0]
        obj_ids = [f"{cid}:objective:{k}" for k in range(len(concepts_by_id[cid]["objectives"]))]
        for j, (kind, q, sol) in enumerate(
            [
                ("conceptual", f"What core role does {ch['title']} play in a Transformer?", f"{ch['title']} transforms representations cleanly across token positions."),
                ("numerical", f"For d_model=64 and h=8 heads, what is d_k in chapter {i}?", "d_k = 64 / 8 = 8 per attention head."),
                ("diagnosis", f"What fails if scaling or residual connections are omitted in {ch['title']}?", "Gradients saturate or degrade across deep stacks."),
                ("comparison", f"How does {ch['title']} compare to recurrent sequence processing?", "It processes all sequence positions in parallel rather than sequentially."),
            ]
        ):
            assessments.append(
                {
                    "id": f"tf.q{i}.{j}",
                    "chapter": ch["id"],
                    "objectives": [obj_ids[j % len(obj_ids)]],
                    "type": kind,
                    "question": q,
                    "hint": "Trace the tensor shapes and scaling factors carefully.",
                    "solution": sol,
                }
            )
    visuals = [
        {
            "id": "tf-pos-curve",
            "concept": "tf.c2",
            "section": "Sinusoidal Encoding",
            "kind": "source_figure",
            "coverage_category": "mathematical_behavior",
            "progression_level": 2,
            "objective": "Show sinusoidal positional encoding curve",
            "url": "https://commons.wikimedia.org/wiki/File:Sinusoidal_positional_encoding.png",
            "source": "https://commons.wikimedia.org/",
            "rights": "CC-BY-4.0",
            "alt": "Sinusoidal positional encoding curve",
            "relevance": "Illustrates smooth positional frequencies.",
            "asset_policy": "offline_only",
            "local_fallback": "fixture_pos.png",
            "explain": "Examine how frequency varies across dimensions in the sinusoidal positional curve.",
            "decode_components": ["Horizontal axis traces position index while curve height shows periodic scaling."],
            "connect": "These continuous position signals feed directly into downstream attention dot products.",
        },
        {
            "id": "tf-arch-blocks",
            "concept": "tf.c5",
            "section": "Full Architecture",
            "kind": "source_figure",
            "coverage_category": "overall_structure",
            "progression_level": 1,
            "objective": "Show end-to-end Transformer encoder-decoder block interfaces",
            "url": "https://commons.wikimedia.org/wiki/File:Transformer_architecture.png",
            "source": "https://commons.wikimedia.org/",
            "rights": "CC-BY-4.0",
            "alt": "Transformer encoder-decoder architecture block diagram",
            "relevance": "Maps encoder and decoder stacks using external architecture figure.",
            "asset_policy": "offline_only",
            "local_fallback": "fixture_arch.png",
            "explain": "Examine the full Transformer encoder-decoder block pipeline before inspecting individual layers.",
            "decode_components": ["Left column represents encoder self-attention blocks and right column represents masked decoder blocks."],
            "connect": "Notice how queries Q, keys K, and values V cross from encoder output into decoder cross-attention.",
            "abbreviations": ["Q", "K", "V"],
        },
    ]
    return {
        "topic": "Transformer Architecture",
        "source_policy": "strict",
        "classification": {"domain": "Artificial Intelligence", "subject": "Deep Learning"},
        "notation": {
            "Q": "Query matrix",
            "K": "Key matrix",
            "V": "Value matrix",
            "d_model": "Hidden model dimension",
        },
        "chapters": chapters,
        "concepts": concepts,
        "assessments": assessments,
        "visuals": visuals,
        "web_image_first": web_image_first,
        "organize_by_collection": organize_by_collection,
        "embed_style": embed_style,
        "learner_level": learner_level,
        "enforce_bvia_walkthrough": enforce_bvia_walkthrough,
    }


def _reviews_for(plan: dict, drafts: dict[str, str]) -> dict:
    def receipt(chapter_ids):
        return {
            "verifier": "stage2 pytest reviewer",
            "method": "artifact-bound content review",
            "result": "pass",
            "limitations": "Isolated synthetic test fixture.",
            "evidence": [
                {"chapter": cid, "hash": content_hash(drafts[cid]), "excerpt": drafts[cid].splitlines()[0]}
                for cid in chapter_ids
            ],
        }

    return {
        **{r: receipt(drafts) for r in plan["review_required"]},
        "obligations": {o["id"]: receipt([o["owner"]]) for o in plan["obligations"]},
    }


def _evidence_for(plan: dict) -> dict:
    return {
        o["id"]: {
            "verified": True,
            "source": "Attention Is All You Need (supplied fixture)",
            "location": "Section 3",
            "origin": "supplied",
            "claim": "Transformer layers preserve model dimension d_model across residual sublayers.",
            "classification": "definition",
            "version": "arXiv:1706.03762v7",
            "verification_method": "supplied fixture check",
            "limits": "test fixture only",
        }
        for c in plan["concepts"]
        for o in c["research_obligations"]
    }


def _transformer_drafts() -> dict[str, str]:
    return {
        "ch1": (
            "# Tokenization and Embeddings\n\n"
            "## Input Representations\n\n"
            "Token embeddings map discrete vocabulary indices into dense vectors of dimension $d_{model}$ "
            "so downstream attention projections operate in a continuous Euclidean space.\n"
        ),
        "ch2": (
            "# Positional Encoding\n\n"
            "## Sinusoidal Encoding\n\n"
            "Because self-attention is permutation-equivariant, sinusoidal positional encodings inject "
            "smooth order signals into every token embedding before the first attention block.\n"
        ),
        "ch3": (
            "# Scaled Dot-Product Attention\n\n"
            "## Attention Mechanism\n\n"
            "Attention computes scaled inner products between queries $Q$ and keys $K$, normalizes them "
            "with softmax, and aggregates values $V$ without recurrence.\n"
        ),
        "ch4": (
            "# Multi-Head Attention\n\n"
            "## Parallel Subspaces\n\n"
            "Multi-head attention splits $Q$, $K$, and $V$ into parallel lower-dimensional subspaces "
            "so different heads specialize in syntactic and semantic relationships simultaneously.\n"
        ),
        "ch5": (
            "# Encoder-Decoder Stack\n\n"
            "## Full Architecture\n\n"
            "To understand how a Transformer processes sequences end to end, follow how embeddings enter "
            "the encoder stack and feed cross-attention queries Q, keys K, and values V in the decoder stack.\n"
        ),
    }


def _write_png_fixture(path: Path, width: int = 400, height: int = 220) -> None:
    import binascii, struct, zlib
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = (b"\x00" + b"\x10\x40\x80" * width) * height
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def test_full_transformer_pipeline_lavia_bvia_and_vault_native_layout(tmp_path: Path):
    _write_png_fixture(tmp_path / "fixture_pos.png")
    _write_png_fixture(tmp_path / "fixture_arch.png")
    spec = _transformer_spec(enforce_bvia_walkthrough=True)
    plan = build_composition(spec)

    # Propagated LAVIA / BVIA fields and visual coverage attached
    assert plan["web_image_first"] is True
    assert plan["organize_by_collection"] is True
    assert plan["collection_slug"] == "transformer-architecture"
    assert plan["embed_style"] == "wikilink"
    assert plan["learner_level"] == "beginner"
    assert plan["visual_coverage"]["total_planned_visuals"] == 2
    assert plan["progressive_visual_order"] == ["tf-arch-blocks", "tf-pos-curve"]

    # Vault-native <vault>/Transformer Architecture/ layout (zero "6 - Full Notes")
    assert plan["folder"] == "Transformer Architecture"
    assert plan["moc_path"] == "Transformer Architecture/00 - Map of Contents.md"
    assert all(ch["path"].startswith("Transformer Architecture/") for ch in plan["chapters"])
    assert "6 - Full Notes" not in plan["folder"]
    assert "6 - Full Notes" not in plan["moc_path"]

    # Prepare composition & check LAVIA manifest persistence
    prepared_drafts, renderers = prepare_composition(tmp_path, plan, _transformer_drafts())
    assert len(renderers) == 2
    assert all(r["status"] == "verified" for r in renderers.values()), renderers
    manifest_file = tmp_path / "assets/scriptorium/transformer-architecture/manifest.json"
    assert manifest_file.is_file()
    persisted_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert persisted_manifest["collection_slug"] == "transformer-architecture"
    assert persisted_manifest["summary"]["verified"] == 2

    # BVIA Explain -> Show -> Decode -> Connect check passes on prepared chapter bodies
    for visual in plan["visuals"]:
        owner = next(ch["id"] for ch in plan["chapters"] if visual["concept"] in ch["concepts"])
        bvia_check = bvia.validate_explain_show_decode_connect(
            prepared_drafts[owner],
            visual,
            terminology_registry=plan["notation"],
        )
        assert bvia_check["passed"] is True, bvia_check

    # Publish composition and validate published collection
    evidence = _evidence_for(plan)
    reviews = _reviews_for(plan, prepared_drafts)
    pub = publish_composition(tmp_path, plan, prepared_drafts, evidence=evidence, reviews=reviews)
    assert pub["complete"] is True, pub["errors"]
    assert pub["manifest"]["summary"]["verified"] == 2
    assert len(pub["written_paths"]) == 6
    assert (tmp_path / "Transformer Architecture/00 - Map of Contents.md").is_file()
    assert not (tmp_path / "6 - Full Notes").exists()

    # MOC must NOT leak raw internal IDs like tf.c1 (covered)
    moc_text = (tmp_path / plan["moc_path"]).read_text(encoding="utf-8")
    assert "tf.c1 (covered)" not in moc_text
    assert "Token Embeddings" in moc_text

    val = validate_published_composition(tmp_path, plan)
    assert val["valid"] is True, val["errors"]
    assert val["manifest"]["summary"]["verified"] == 2

    # Targeted visual repair via CLI --repair-visuals after deleting an asset
    broken_rel = renderers["tf-pos-curve"]["path"]
    (tmp_path / broken_rel).unlink()
    broken_val = validate_published_composition(tmp_path, plan)
    assert broken_val["valid"] is False

    spec_file = tmp_path / "spec.json"
    spec_file.write_text(json.dumps(spec), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/scribe.py"),
            "notes",
            "compose",
            "--spec",
            str(spec_file),
            "--vault",
            str(tmp_path),
            "--repair-visuals",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    repaired_payload = json.loads(proc.stdout)
    assert repaired_payload["repaired_ids"] == ["tf-pos-curve"]
    assert (tmp_path / broken_rel).is_file()
    assert validate_published_composition(tmp_path, plan)["valid"] is True


def test_publish_rejects_leaked_remote_image_and_missing_local_embed_in_lavia_mode(tmp_path: Path):
    spec = _transformer_spec()
    plan = build_composition(spec)
    prepared_drafts, _ = prepare_composition(tmp_path, plan, _transformer_drafts())
    # Inject leaked remote image URL
    leaked = dict(prepared_drafts)
    leaked["ch1"] = leaked["ch1"] + "\n![leaked remote](https://cdn.example.invalid/diagram.png)\n"
    res = publish_composition(
        tmp_path,
        plan,
        leaked,
        evidence=_evidence_for(plan),
        reviews=_reviews_for(plan, leaked),
    )
    assert res["complete"] is False
    assert any("remote image" in e for e in res["errors"]), res["errors"]


def test_compile_context_maps_scientific_empirical_and_computational_subtemplates():
    spec = _transformer_spec()
    spec["concepts"][0]["capabilities"] = ["S07"]
    spec["concepts"][1]["capabilities"] = ["S16"]
    spec["concepts"][2]["capabilities"] = ["S06"]
    spec["concepts"][3]["capabilities"] = ["S05"]
    plan = build_composition(spec)

    ctx_s07 = compile_context(plan, ["tf.c1"])
    assert any(f.endswith("subtemplates/scientific.md") for f in ctx_s07["loaded_files"]), ctx_s07["loaded_files"]

    ctx_s16 = compile_context(plan, ["tf.c2"])
    assert any(f.endswith("subtemplates/scientific.md") for f in ctx_s16["loaded_files"]), ctx_s16["loaded_files"]

    ctx_s06 = compile_context(plan, ["tf.c3"])
    assert any(f.endswith("subtemplates/empirical.md") for f in ctx_s06["loaded_files"]), ctx_s06["loaded_files"]

    ctx_s05 = compile_context(plan, ["tf.c4"])
    assert any(f.endswith("subtemplates/computational.md") for f in ctx_s05["loaded_files"]), ctx_s05["loaded_files"]


def test_research_engine_and_pedagogy_engine_facade_smoke(tmp_path: Path):
    # ResearchEngine facade methods (all 6)
    re_engine = ResearchEngine(cache_dir=tmp_path / "rcache")
    inst_plan = {
        "topic": "Gradient Descent",
        "concepts": [
            {
                "id": "gd",
                "title": "Gradient Descent",
                "knowledge_types": ["mathematical"],
                "depths": {"math": 3, "code": 1, "visual": 1, "theory": 2, "practice": 1, "assessment": 1},
            }
        ],
    }
    rplan = re_engine.plan("Gradient Descent", inst_plan)
    assert rplan["topic"] == "Gradient Descent"
    assert rplan["research_questions"]

    raw_reg = {
        "sources": [
            {
                "source_id": "SRC-1",
                "title": "Convex Optimization",
                "source_type": "academic_textbook",
                "canonical_url": "https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf",
                "access_status": "full",
                "content_verified": True,
            }
        ],
        "claims": [
            {
                "claim_id": "CLM-1",
                "concept_id": "gd",
                "statement": "Gradient descent converges for L-smooth convex functions with step size <= 1/L.",
                "source_ids": ["SRC-1"],
                "verification_status": "verified",
            }
        ],
    }
    norm_reg = re_engine.normalize_registry(raw_reg, research_plan=rplan)
    assert norm_reg["sources"]

    audit = re_engine.audit_citations("# Gradient Descent\n\nBody without broken citations.\n", norm_reg)
    assert isinstance(audit, list)

    pkg = re_engine.package(rplan, norm_reg)
    assert isinstance(pkg, dict) and "concepts" in pkg and "coverage_summary" in pkg

    candidates = [
        {
            "title": "Convex Optimization Textbook",
            "resource_type": "academic_textbook",
            "author_or_institution": "Boyd & Vandenberghe",
            "canonical_url": "https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf",
            "verified": True,
            "cost": "free",
            "learner_levels": ["beginner", "intermediate"],
            "progression_stage": "conceptual_foundation",
            "why_useful": "Rigorous first-principles convex optimization reference.",
        }
    ]
    curated_list = re_engine.curate_resources(candidates)
    curated_with_topic = re_engine.curate_resources("Gradient Descent", candidates)
    assert curated_list["recommended"]
    assert curated_with_topic["recommended"]

    tf_plan = build_composition(_transformer_spec())
    ev_status = re_engine.composition_evidence_status(tf_plan, _evidence_for(tf_plan))
    assert ev_status["sufficient"] is True

    # PedagogyEngine facade methods
    ped = PedagogyEngine()
    comp = ped.plan_composition(_transformer_spec())
    assert comp["topic"] == "Transformer Architecture"
    tbl = ped.render_table(
        {
            "type": "definition",
            "objective": "Define core terms",
            "interpretation": "Each term corresponds to a Transformer component.",
            "rows": [{"term": "Attention", "meaning": "Weighted value aggregation"}],
        }
    )
    assert "| Attention | Weighted value aggregation |" in tbl
    vis_sel = ped.select_visual(
        {"kind": "equation", "objective": "Plot curve", "search_queries": ["quadratic curve diagram"], "concept": "c1", "section": "Core"},
        available={"external"},
    )
    assert vis_sel["renderer"] == "external"

    raw_inst_plan = {
        "topic": "Gradient Descent",
        "audience": "beginner",
        "overall_objective": "Understand gradient descent from first principles.",
        "source_policy": "independent",
        "concepts": [
            {
                "id": "gd",
                "title": "Gradient Descent",
                "types": ["mathematical"],
                "objectives": ["explain", "derive"],
                "depth": {"math": 4, "theory": 4},
                "prerequisites": [],
                "reason": "Core optimization method.",
            }
        ],
    }
    norm_p = ped.normalize_plan(raw_inst_plan)
    assert norm_p["concepts"][0]["id"] == "gd"
    contract = ped.resolve_contract("Explain gradient descent", "Gradient Descent", raw_inst_plan)
    assert "composed_outline" in contract
    ped_plan = ped.build_pedagogical_plan(norm_p)
    assert "concepts" in ped_plan
    assert isinstance(ped.detect_gaps("# Gradient Descent\n\nWe update $x_{t+1} = x_t - \\alpha \\nabla f(x_t)$.\n"), dict)
    assert isinstance(ped.control_density("# Gradient Descent\n\nShort crisp paragraph.\n"), dict)
    assert isinstance(ped.optimize_examples([{"title": "Ex 1", "concept": "gd", "type": "numeric", "body": "x=2"}]), dict)

    auth_note = "---\ntopic: Gradient Descent\ntags: [domain/mathematics, subject/optimization, topic/gradient-descent, type/deep-notes]\nmaster_topic: Optimization\ndomain: Mathematics\nnote_type: deep-notes\n---\n# Gradient Descent\n\n## Core Update\n\nThe gradient update is $x_{t+1} = x_t - \\alpha \\nabla f(x_t)$.\n"
    comp_res = ped.compress(auth_note)
    assert "compressed_body" in comp_res
    assert isinstance(ped.validate_compression(auth_note, comp_res["compressed_body"]), dict)

    bp = ped.build_explanation_blueprint("Gradient Descent")
    ex_note = ped.compose_explanation(bp)
    assert isinstance(ped.validate_explanation(ex_note, bp), list)
    trace_check = ped.verify_trace(
        [{"step": 0, "theta": 2.0, "gradient": 4.0, "loss": 4.0, "next_theta": 1.6}],
        value_checks={"gradient": "2.0 * theta", "loss": "theta ** 2"},
        recurrence_checks={"next_theta": "theta - alpha * gradient"},
        constants={"alpha": 0.1},
    )
    assert isinstance(trace_check, dict)

    prefs = ResolvedNotePreferences(
        "Deep mastery",
        "M1",
        None,
        "comprehensive",
        {},
        "hierarchical_collection",
        [],
        "adaptive",
    )
    col_plan = ped.plan_collection("Transformer Architecture", prefs)
    assert "Transformer" in col_plan.title
    assert col_plan.nodes
    assert isinstance(ped.format_collection_preview(col_plan), str)
    mod_plan = ped.modify_collection_plan(col_plan, "keep as is")
    assert mod_plan is not None
    assert isinstance(ped.allocate_depth(col_plan, prefs), dict)
    assert isinstance(ped.evaluate_granularity(col_plan, prefs), dict)
    child_id = col_plan.nodes[1].concept_id if len(col_plan.nodes) > 1 else col_plan.nodes[0].concept_id
    assert ped.split_note_in_plan(col_plan, child_id, ["Part A", "Part B"]) is not None
    assert isinstance(ped.generate_learning_paths(col_plan, prefs), dict)
    assert isinstance(ped.plan_synthesis_notes(col_plan, prefs), list)
    assert isinstance(ped.apply_progressive_disclosure(auth_note), dict)
    outcomes = ped.define_learning_outcomes(col_plan.nodes[0], prefs)
    assert isinstance(outcomes, list)
    assert isinstance(ped.build_collection_assessment(col_plan, prefs, {col_plan.nodes[0].concept_id: outcomes}), dict)


def test_routing_negation_and_from_scratch_distinction():
    # plan_notes.inspect_request must strip negations before override matching
    inspected = plan_notes.inspect_request("/scribe-notes don't make a cheat sheet; explain PCA deeply")
    assert inspected["master"] == "M1", inspected
    assert inspected["template"] != "cheat-sheet", inspected
    assert inspected["lock"] != "explicit" or inspected["master"] == "M1"

    # "teach/explain <X> from scratch" -> M1; "implement/build/code <X> from scratch" -> M5
    assert route_request("teach me backpropagation from scratch")["master"] == "M1"
    assert route_request("explain transformers from scratch")["master"] == "M1"
    assert route_request("implement backpropagation from scratch")["master"] == "M5"
    assert route_request("build a tokenizer from scratch")["master"] == "M5"
    assert route_request("code k-means from scratch")["master"] == "M5"


def test_validate_chapter_rejects_tab_in_latex_duplicate_headings_and_leaked_ids():
    plan = build_composition(_transformer_spec())

    # 1. Raw TAB inside inline or display LaTeX math span
    tab_note = five_key_note(
        plan,
        "ch1",
        "Tokenization",
        "# Tokenization\n\n## Input Representations\n\nFormula $a + \text{b}$ has a raw tab.\n",
        None,
    )
    errs_tab = validate_chapter(tab_note)
    assert any("TAB" in e for e in errs_tab), errs_tab

    # 2. Duplicate immediate # Title / ## Title headings
    dup_note = five_key_note(
        plan,
        "ch1",
        "Tokenization",
        "# Input Representations\n\n## Input Representations\n\nExplanation text.\n",
        None,
    )
    errs_dup = validate_chapter(dup_note)
    assert any("duplicate immediate H1/H2" in e for e in errs_dup), errs_dup

    # 3. Leaked internal concept/prerequisite ID like tf.c1 (covered)
    leak_note = five_key_note(
        plan,
        "ch2",
        "Positional Encoding",
        "# Positional Encoding\n\n## Sinusoidal Encoding\n\nPrerequisite: tf.c1 (covered).\n",
        None,
    )
    errs_leak = validate_chapter(leak_note)
    assert any("leaked internal" in e for e in errs_leak), errs_leak

    # Clean chapter passes all three checks
    clean_note = five_key_note(
        plan,
        "ch1",
        "Tokenization",
        "# Tokenization\n\n## Input Representations\n\nClean formula $a + \\text{b}$ without leaks.\n",
        None,
    )
    assert validate_chapter(clean_note) == []


def test_heading_slug_and_lint_instruction_authority_contracts_and_bare_scripts(tmp_path: Path):
    assert heading_slug("1. Scaled Dot-Product `Attention` (Q, K, V)") == "1-scaled-dot-product-attention-q-k-v"

    # Build a minimal repo layout in tmp_path to verify lint_instruction_authority catches
    # bare retired script names and references/contracts/ leaks cleanly.
    import shutil
    shutil.copytree(ROOT / "references", tmp_path / "references")
    shutil.copytree(ROOT / "shared", tmp_path / "shared")
    shutil.copytree(ROOT / "skills", tmp_path / "skills")
    for fname in ("SKILL.md", "router.md", "README.md"):
        shutil.copy2(ROOT / fname, tmp_path / fname)

    contract_doc = tmp_path / "references/contracts/test-leak.md"
    contract_doc.write_text(
        "Use instructional_plan.py and note_verification.py with templates/deepstudy-master.md.\n",
        encoding="utf-8",
    )
    res = lint_instruction_authority(tmp_path)
    assert res["valid"] is False
    details = {(i["file"], i["detail"]) for i in res["issues"]}
    assert ("references/contracts/test-leak.md", "instructional_plan.py") in details
    assert ("references/contracts/test-leak.md", "note_verification.py") in details
    assert ("references/contracts/test-leak.md", "templates/deepstudy-master.md") in details
