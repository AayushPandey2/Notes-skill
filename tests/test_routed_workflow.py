"""Exercise the built-in router, scaffold, publisher and both validators."""

import json
from pathlib import Path
import re
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import note_layout as layout
import plan_notes as planner
from validate_note import validate_text


def cli(script, *args, code=0):
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts" / f"{script}.py"), *map(str, args)],
        capture_output=True, encoding="utf-8",
    )
    assert result.returncode == code, result.stdout + result.stderr
    return result.stdout


@pytest.mark.parametrize(("request_text", "template", "language"), [
    ("/scribe-dsa cpp https://example.test/two-sum", "dsa", "cpp"),
    ("scribe-dsa python Two Sum", "dsa", "python"),
    ("Solve Two Sum in C++", "dsa", "cpp"),
    ("/scribe-practice CNN", "practice", None),
    ("Create a practice set for my CNN notes", "practice", None),
    ("/scribe-atomic-notes Residual Connection", "atomic", None),
    ("scribe-atomic-notes Residual Connection", "atomic", None),
    ("/scribe-notes Operating Systems", None, None),
    ("Use studynotes template for Operating Systems", "studynotes", None),
    ("https://www.youtube.com/watch?v=example", "summary", None),
    ("Summarize this paper https://arxiv.org/abs/1706.03762", "summary", None),
    ("https://arxiv.org/abs/1706.03762", "paper-breakdown", None),
    ("<https://doi.org/10.5555/12345>", "paper-breakdown", None),
    ("Study CNN using https://arxiv.org/abs/1706.03762 as reference", None, None),
    ("Create a cheat sheet on CNN", "cheat-sheet", None),
    ("Compare Adam vs SGD", "comparison", None),
    ("Use deepstudy-master template for CNN", "deepstudy-master", None),
    ("/scribe-distill CNN", "cheat-sheet", None),
    ("/scribe-compare Adam vs SGD", "comparison", None),
    ("/scribe-deepnotes CNN", None, None),
    ("/scribe-deepnotes https://arxiv.org/abs/1706.03762", "paper-breakdown", None),
    ("/scribe-expand CNN", None, None),
    ("/scribe-ingest CNN https://example.test/docs", None, None),
])
def test_request_precedence(request_text, template, language):
    intent = yaml.safe_load(cli("plan_notes", "inspect", request_text))
    assert (intent["template"], intent["language"]) == (template, language)


def test_command_usage_and_read_only():
    cli("plan_notes", "inspect", "/scribe-dsa invalid", code=2)
    cli("plan_notes", "inspect", "/scribe-practice", code=2)
    cli("plan_notes", "inspect", "/scribe-atomic-notes", code=2)
    cli("plan_notes", "inspect", "/scribe-notes", code=2)
    for command in ("doubt", "quiz"):
        assert planner.inspect_request(f"/scribe-{command} CNN")["mode"] == "existing-notes"


def scaffold(vault, item, *, narrow=False, depends_on=()):
    return cli(
        "scaffold_note", vault, "--template", item["template"], "--math-level", item["math_level"],
        "--id", item["note_id"], "--number", item["id"], "--title", item["title"],
        "--topic", "CNN", "--language", item.get("language", "none"),
        "--created", "2026-01-01", *(["--narrow-practice"] if narrow else []),
        *(["--depends-on", *depends_on] if depends_on else []),
    )


def finish_fixture(draft):
    """Populate structural fixtures with a small addition example."""
    fills = {
        "> <!-- scaffold: Introduce symbols and 1–3 display equations. -->":
            "> Let x be an integer input and y the integer output.\n> $$y = x + 1$$",
        "<!-- scaffold: Define all symbols, domain and assumptions; then show the display equation. -->":
            "Example Pebble uses x = 2 pebbles and returns y = 3 pebbles.\n\n$$y = x + 1$$",
        "<!-- scaffold: Explain scale and sensitivity. -->": "One extra pebble shifts every output by one.",
        "<!-- scaffold: Evaluate zero, ±1, ties and ±∞ under the stated domain. -->":
            "Zero maps to one. Minus one maps to zero. One maps to two. Unbounded inputs stay unbounded.",
        "<!-- scaffold: Give a concrete invalid application. -->": "An absent input has no integer successor.",
        "<!-- scaffold: State target, domain and strategy; number every display-math step. -->":
            "For Pebble, substitute the given input.\n\n1. $$y = 2 + 1 = 3$$",
        "<!-- scaffold: Justify the assumption, guards and implication. -->": "Substitution preserves equality over integers.",
        "<!-- scaffold: Question prompt. -->": "How does one increment affect the count?",
        "<!-- scaffold: Non-spoiling hint. -->": "Identify the input count before tracing.",
        "<!-- scaffold: Approach, final answer, and common trap. -->":
            "Add one to the input.\n>\n> **Final answer:** The count increases by one.",
        "<!-- scaffold: State the change in understanding in 2–3 sentences. -->":
            "I can trace the increment. Its shift stays constant.",
        "<!-- scaffold: State one specific unresolved boundary question. -->": "What happens at the maximum integer?",
        "<!-- scaffold: Name 1–3 granular ideas as existing links or pending text. -->": "Successor (pending note)",
        "<!-- scaffold: Add resolved links and bridge to the next subtopic. -->": "Next I will check overflow.",
    }
    for key, replacement in fills.items():
        draft = draft.replace(key, replacement)
    draft = re.sub(r"^> <!-- scaffold: .+ -->$", "> Trace the increment.", draft, flags=re.M)
    draft = re.sub(r"^<!-- scaffold: .+ -->$", "Each step preserves the integer count.", draft, flags=re.M)
    draft = draft.replace(
        layout.SYMBOL_TABLE[1] + "\n\n",
        layout.SYMBOL_TABLE[1] + "\n| x, y, + | Input, output, addition | Scalar | Integers | +1 per input step |\n\n",
        1,
    ) if layout.SYMBOL_TABLE[0] in draft else draft
    for label, values in (
        ("Smallest non-trivial", "1 | 1 + 1 | 2 | Increment"),
        ("Named running example", "2 | 2 + 1 | 3 | Pebble"),
        ("Perturbed input", "3 | 3 + 1 | 4 | Sensitivity"),
        ("Boundary / degenerate", "0 | 0 + 1 | 1 | Zero input"),
    ):
        draft = draft.replace(f"| {label} | | | | |", f"| {label} | {values} |")
    if "## What is this concept and its governing claim?" in draft:
        draft = draft.replace("Each step preserves the integer count.\n\n", "")
        draft = draft.replace("Let x be an integer input and y the integer output.", "x input; y output.")
        draft = draft.replace("Example Pebble uses x = 2 pebbles and returns y = 3 pebbles.", "Pebble counts integers.")
        draft = draft.replace("One extra pebble shifts every output by one.", "Addition translates.")
        draft = draft.replace("Zero maps to one. Minus one maps to zero. One maps to two. Unbounded inputs stay unbounded.",
                              "Zero, unit, unbounded: same shift.")
        draft = draft.replace("An absent input has no integer successor.", "Undefined for null.")
        draft = draft.replace("For Pebble, substitute the given input.", "Substitute Pebble.")
        draft = draft.replace("Substitution preserves equality over integers.", "Integer equality.")
        draft = draft.replace("I can trace the increment. Its shift stays constant.", "Constant shift.")
        draft = draft.replace("What happens at the maximum integer?", "Overflow?")
        draft = draft.replace("Next I will check overflow.", "Overflow.")
        draft = re.sub(r"^(\| (?:Smallest non-trivial|Named running example|Perturbed input|Boundary / degenerate) \|) .+$",
                       r"\1 0 | +1 | 1 | Shift |", draft, flags=re.M)
    return draft


@pytest.mark.parametrize("route", layout.ROUTES)
@pytest.mark.parametrize("level", (0, 1, 2))
def test_scaffold_and_lint_all_layouts(tmp_path, route, level):
    item = {"id": "01", "note_id": "pebble-01", "title": "Pebble", "template": route,
            "math_level": level, "language": "python" if route == "dsa" else "none"}
    raw = scaffold(tmp_path, item)
    assert raw == scaffold(tmp_path, item)
    assert ("Key Equations" in raw) == (level > 0 and route not in layout.DEEP_ROUTES and route != "practice")
    fm = yaml.safe_load(raw.split("---\n", 2)[1])
    assert list(fm.keys()) == ["id", "aliases", "topic", "tags", "nexttopics"]
    note = tmp_path / "note.md"
    note.write_text(finish_fixture(raw), encoding="utf-8")
    assert "Errors: 0" in cli("validate_note", note)
    assert any("Unauthorized frontmatter key" in msg for _, msg in validate_text(
        note.read_text(encoding="utf-8").replace("topic: CNN\n", "topic: CNN\ntitle: Extra\n", 1),
        route=route, math_level=level,
    ))
    assert any("Missing frontmatter key" in msg for _, msg in validate_text(
        note.read_text(encoding="utf-8").replace("nexttopics: []\n", "", 1),
        route=route, math_level=level,
    ))


def _outline(title, purpose="explain", weight="low", density="cohesive", level=0, **extra):
    return {"title": title, "purpose": purpose, "impl_weight": weight, "density": density,
            "math_level": level, "routing_reason": f"Teach {title} in its own note.", **extra}


def test_cnn_publication_and_interrupted_retry(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    entries = [
        _outline("Convolution Operation & Kernels", "implement", "high", level=2, domain="ml",
                 routing_reason="Derive discrete cross-correlation and compare a manual trace with PyTorch."),
        _outline("History of LeNet to ResNet",
                 routing_reason="Trace architectural changes and their motivation through historical evidence."),
        _outline("PyTorch nn.Conv2d Parameters", "reference", density="callables", level=1,
                 language="python", verification_stack=["Python + PyTorch"], depends_on=["01"],
                 routing_reason="Look up Conv2d parameters and calculate their effect on output shape."),
    ]
    outline = tmp_path / "outline.json"
    outline.write_text(json.dumps(entries), encoding="utf-8")
    command = ("start", vault, "--request", "Study CNN using https://arxiv.org/abs/1512.03385",
               "--topic-folder", "CNN", "--outline", outline)
    plan = yaml.safe_load(cli("plan_notes", *command))
    plan_id = plan["plan_id"]
    assert [(n["template"], n["math_level"], n["output_path"]) for n in plan["plan"]] == [
        ("deepstudy-master", 2, "01 - Convolution Operation & Kernels.md"),
        ("deepstudy-master", 0, "02 - History of LeNet to ResNet.md"),
        ("api-table", 1, "03 - PyTorch nn.Conv2d Parameters.md"),
        ("practice", 2, "Practice Sets/CNN - Practice Test.md"),
    ]
    assert plan["plan"][0]["verification_stack"] == []
    assert not (vault / "CNN").exists()
    cli("scaffold_note", vault, "--syllabus", "--topic", "CNN", "--output", "CNN/00-MOC-cnn.md",
        "--allowed-subtopics", *(n["output_path"] for n in plan["plan"][:-1]))
    saved = {}
    by_id = {item["id"]: item for item in plan["plan"]}
    for item in plan["plan"]:
        draft = tmp_path / f"{item['id']}.md"
        links = [f"[[CNN/{Path(by_id[dep]['output_path']).with_suffix('').as_posix()}]]"
                 for dep in item.get("depends_on", ())]
        content = finish_fixture(scaffold(vault, item, depends_on=links))
        if item["id"] == "02":
            content = content.replace("Each step preserves the integer count.",
                '~~~mermaid\nflowchart TD\nA["Input"] --> B["Features"] --> C["Output"]\n~~~\n'
                'Features are formed from the input. The output consumes those features.', 1)
        if item["id"] == "practice":
            interrupted = yaml.safe_load(cli("plan_notes", *command[:-2]))
            assert interrupted["status"] == {"01": "complete", "02": "complete", "03": "complete", "practice": "pending"}
            content = content.replace("Each step preserves the integer count.", "[[CNN/03 - PyTorch nn.Conv2d Parameters]]", 1)
        draft.write_text(content, encoding="utf-8")
        assert "Errors: 0" in cli("validate_note", draft)
        assert "published" in cli("plan_notes", "publish", vault, plan_id, item["id"], draft)
        path = (vault / item["output_path"]) if item["template"] in {"practice", "atomic"} else (vault / "CNN" / item["output_path"])
        saved[path] = path.read_bytes()
    assert set(yaml.safe_load(cli("plan_notes", "status", vault, plan_id))["status"].values()) == {"complete"}
    assert "already complete" in cli("plan_notes", "publish", vault, plan_id, "01", tmp_path / "01.md")
    assert all(path.read_bytes() == data for path, data in saved.items())
    assert "Errors: 0" in cli("verify_vault_notes", vault, "--files", *saved)
    graph = json.loads(cli("vault_graph", vault, "--topic", "CNN", "--format", "json", "--check-cycles"))
    assert graph["summary"]["broken_link_count"] == 0
    for item in plan["plan"]:
        rel = item["output_path"] if item["template"] in {"practice", "atomic", "cheat-sheet"} else f"CNN/{item['output_path']}"
        assert rel in graph["nodes"]


def test_destinations_and_collision_preflight(tmp_path):
    (tmp_path / "CNN").mkdir()
    practice = planner.build_plan(tmp_path, "/scribe-practice CNN", "CNN", [_outline("CNN")])
    assert [item["output_path"] for item in practice["plan"]] == ["Practice Sets/CNN - Practice.md"]
    assert planner._targets(tmp_path, practice)["01"] == tmp_path / "Practice Sets" / "CNN - Practice.md"
    with pytest.raises(ValueError, match="existing topic"):
        planner.build_plan(tmp_path, "/scribe-practice CNN", "missing", [_outline("CNN")])
    atomic = planner.build_plan(tmp_path, "/scribe-atomic-notes Residual Connection", "CNN", [_outline("Residual Connection")])
    assert [item["output_path"] for item in atomic["plan"]] == ["Atomic Notes/Residual Connection.md"]
    assert planner._targets(tmp_path, atomic)["01"] == tmp_path / "Atomic Notes" / "Residual Connection.md"
    compare = planner.build_plan(tmp_path, "/scribe-compare Adam vs SGD", ".", [_outline("Adam vs SGD")])
    assert compare["plan"][0]["output_path"] == "comparison/adam-vs-sgd.md"
    distill = planner.build_plan(tmp_path, "/scribe-distill CNN", "CNN", [_outline("CNN")])
    assert [item["output_path"] for item in distill["plan"]] == ["Cheatsheets/cnn-CHEAT-SHEET.md"]
    assert planner._targets(tmp_path, distill)["01"] == tmp_path / "Cheatsheets" / "cnn-CHEAT-SHEET.md"
    cnn_sub = planner.build_plan(tmp_path, "Create a cheat sheet on Pooling", "CNN", [_outline("Pooling", "revise")])
    rnn_sub = planner.build_plan(tmp_path, "Create a cheat sheet on Pooling", "RNN", [_outline("Pooling", "revise")])
    assert [item["output_path"] for item in cnn_sub["plan"]] == ["Cheatsheets/cnn-pooling-CHEAT-SHEET.md"]
    assert [item["output_path"] for item in rnn_sub["plan"]] == ["Cheatsheets/rnn-pooling-CHEAT-SHEET.md"]
    nested = planner.build_plan(tmp_path, "/scribe-distill CNN", "ML/CNN", [_outline("CNN")])
    assert planner._targets(tmp_path, nested)["01"] == tmp_path / "ML" / "Cheatsheets" / "cnn-CHEAT-SHEET.md"
    cn_plan = planner.build_plan(
        tmp_path,
        "/scribe-notes Operating Systems",
        "Operating Systems",
        [
            {"title": "Process Scheduling", "purpose": "explain", "impl_weight": "low", "density": "cohesive",
             "routing_reason": "Explain process scheduling in studynotes format."},
            {"title": "CPU Queues Code", "purpose": "implement", "impl_weight": "high", "density": "cohesive",
             "routing_reason": "Trace CPU queue scheduling in studynotes format."},
            {"title": "Scheduling Cheat Sheet", "purpose": "revise", "impl_weight": "low", "density": "cohesive",
             "routing_reason": "Allow auxiliary cheat-sheet."},
        ],
    )
    assert [(n["template"], n["math_level"], n["source_profile"], n["output_path"]) for n in cn_plan["plan"]] == [
        ("studynotes", 0, "fast-web-fetch", "01 - Process Scheduling.md"),
        ("studynotes", 0, "fast-web-fetch", "02 - CPU Queues Code.md"),
        ("cheat-sheet", 0, "vault-notes", "Cheatsheets/operating-systems-scheduling-CHEAT-SHEET.md"),
        ("practice", 0, "planned-notes", "Practice Sets/Operating Systems - Practice Test.md"),
    ]
    for forbidden in layout.DEEP_ROUTES:
        with pytest.raises(ValueError, match="prohibits"):
            planner.build_plan(tmp_path, "/scribe-notes OS", "OS", [_outline("Paging", template=forbidden)])
        with pytest.raises(ValueError, match="prohibits"):
            planner.build_plan(tmp_path, "/scribe-notes OS", "OS", [_outline("Paging")], template=forbidden)
    with pytest.raises(ValueError, match="multiple subtopic notes"):
        planner.build_plan(tmp_path, "/scribe-notes OS", "OS", [_outline("Paging")])
    with pytest.raises(ValueError, match="multiple subtopic notes"):
        planner.build_plan(tmp_path, "/scribe-notes OS", "OS", [_outline("Paging"), _outline("Segmentation")])
    with pytest.raises(ValueError, match="Duplicate"):
        planner.build_plan(tmp_path, "CNN", "CNN", [
            _outline("One", output_path="same.md"), _outline("Two", output_path="SAME.md"),
        ])
    with pytest.raises(ValueError, match="Invalid vault-relative"):
        planner.build_plan(tmp_path, "CNN", "../CNN", [_outline("One")])
    path = tmp_path / "CNN" / "01 - One.md"
    path.write_text("User authored.", encoding="utf-8")
    with pytest.raises(ValueError, match="preserved"):
        planner.start_plan(tmp_path, "CNN", "CNN", [_outline("One")])
    assert path.read_text(encoding="utf-8") == "User authored."


def test_prepare_atomic_links_and_missing_evidence(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    entries = [_outline("Adjacency", "definition", density="micro"),
               _outline("Degree", "definition", density="micro")]
    plan_id, plan = planner.start_plan(vault, "Create atomic notes for graph concepts", ".", entries)
    assert [item["output_path"] for item in plan["plan"]] == ["Atomic Notes/Adjacency.md", "Atomic Notes/Degree.md"]
    for item in plan["plan"]:
        draft = tmp_path / "draft.md"
        text = finish_fixture(scaffold(tmp_path, item))
        if item["id"] == "02":
            text = text.replace("### Metacognitive Reflection & Vault Integration",
                                "![[Adjacency]]\nDegree family (pending note)\n\n### Metacognitive Reflection & Vault Integration", 1)
            assert any("Unresolved wikilink" in message for _, message in validate_text(
                text.replace("Degree family (pending note)", "[[Missing]]"),
                vault=vault, target=vault / item["output_path"],
            ))
        draft.write_text(text, encoding="utf-8")
        assert "published" in planner.publish(vault, plan_id, item["id"], draft)
    for route, evidence in (
        ("summary", "[PARTIAL SUMMARY — TRANSCRIPT/TEXT UNAVAILABLE]\nAuthor: [UNVERIFIED]"),
        ("dsa", "Input limits [ASSUMED / UNVERIFIED]."),
        ("paper-breakdown", "[ABLATION / RESULT ABSENT IN PAPER]"),
    ):
        item = {"template": route, "math_level": 0, "language": "cpp", "id": "01",
                "title": "Fixture", "note_id": "fixture"}
        text = finish_fixture(scaffold(tmp_path, item)).replace("Each step preserves the integer count.", evidence, 1)
        assert not validate_text(text)


def test_publish_standalone_video_with_caption_anchors(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    url = "https://www.youtube.com/watch?v=KuXjwB4LzSA"
    captions = "https://raw.githubusercontent.com/3b1b/captions/main/2022/convolutions/english/captions.srt"
    plan_id, plan = planner.start_plan(vault, url, ".", [_outline("But what is a convolution?")])
    item = plan["plan"][0]
    assert item["template"] == "summary"
    draft = scaffold(vault, item)
    frontmatter, abstract = draft.split("\n# Summary: ", 1)
    assert abstract.startswith(item["title"])
    headings = dict(layout.section_layout("summary", 0))
    footer = finish_fixture(draft).split("### Metacognitive Reflection", 1)[1]
    footer = footer.replace("I can trace the increment. Its shift stays constant.",
                            "I can group dice outcomes by their sum. Bias changes weights without changing the groups.")
    footer = footer.replace("What happens at the maximum integer?", "How does dependence change the weighting?")
    footer = footer.replace("Successor (pending note)", "Joint distribution (pending note)")
    footer = footer.replace("Next I will check overflow.", "Next I will trace the same alignment on polynomial coefficients.")
    authored = f"""# Summary: {item['title']}

{headings[1]}

> [!info] Source Metadata & Accessibility Audit
> **Creator:** Grant Sanderson (3Blue1Brown)
> **Publication date:** 2022-11-18
> **Original URL:** {url}
> **Content access:** Creator-published [English captions]({captions}).
> **Video duration:** [UNVERIFIED]

- Convolution combines entire lists by summing products across aligned pairs.
- Sliding a reversed list groups pairs by their common index sum.
- The same construction applies to probability distributions and polynomial coefficients.

{headings[2]}

### [00:00]({url}&t=0s) Comparing ways to combine lists

The video begins with pairwise addition and multiplication, then introduces convolution as a different operation on sequences.

### [03:58]({url}&t=238s) Bias changes the weights of dice outcomes

For independent dice, each compatible pair contributes the product of the two face probabilities. Add the contributions with the requested sum.

{headings[3]}

| Claim | Timestamp | Check | Caveat |
|---|---|---|---|
| Sum two probabilities by grouping compatible pairs | 03:58 | For two independent fair dice, only the pair of ones yields two, so its probability is one in 36. | Product weights require independence. |

{headings[4]}

Trace the compatible pairs for a sum of three before changing either die's weights.

- Create an atomic note on the joint probability mass function.
- Create a deepstudy-master note on polynomial coefficient convolution.

### Metacognitive Reflection{footer}"""
    file = tmp_path / "video.md"
    file.write_text(frontmatter + "\n" + authored, encoding="utf-8")
    assert "Errors: 0" in cli("validate_note", file)
    assert "published" in cli("plan_notes", "publish", vault, plan_id, item["id"], file)


def test_linter_rejects_malformed_constructs(tmp_path):
    item = {"template": "deepstudy-master", "math_level": 0, "id": "01", "title": "Fixture",
            "note_id": "fixture"}
    text = finish_fixture(scaffold(tmp_path, item))
    for bad, expected in (
        ("$x", "Unclosed inline math"),
        ("$x " + chr(96) + "code" + chr(96) + "$", "Inline code inside math"),
        ("$$\n~~~python\nprint(1)\n~~~\n$$", "Fenced code inside math"),
        ("| A | B |\n|---|---|\n| one | two | three |", "Escape literal pipes"),
        ('~~~mermaid\nflowchart TD\nA[Unquoted] --> B["$x$"]\n~~~', "Malformed Mermaid"),
    ):
        altered = text.replace("Each step preserves the integer count.", bad, 1)
        assert any(expected in message for _, message in validate_text(altered))
    assert any("Duplicate YAML" in message for _, message in validate_text(text.replace("---\n", "---\nid: repeated\n", 1)))
    practice = finish_fixture(scaffold(tmp_path, {**item, "template": "practice"}, narrow=True))
    assert not validate_text(practice)
    assert any("Prefix each callout line" in message for _, message in validate_text(
        practice.replace("Add one to the input.\n>\n", "Add one to the input.\n\n", 1)
    ))
    summary = finish_fixture(scaffold(tmp_path, {**item, "template": "summary"}))
    summary = summary.replace("Each step preserves the integer count.",
                              "[03:42](https://www.youtube.com/watch?v=example&t=2s)", 1)
    assert any("timestamp label must match" in message for _, message in validate_text(summary))
    for route in ("atomic", "cheat-sheet"):
        compact = finish_fixture(scaffold(tmp_path, {**item, "template": route}))
        oversize = compact.replace("### Metacognitive Reflection", "- " + "word " * 400 + "\n\n### Metacognitive Reflection", 1)
        assert any("Body has" in message for _, message in validate_text(oversize))
        if route == "cheat-sheet":
            assert any("bullet exceeds" in message for _, message in validate_text(oversize))


def test_scaffold_loads_one_template(monkeypatch):
    seen = []
    original = Path.read_text

    def track(path, *args, **kwargs):
        seen.append(path.name)
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", track)
    assert planner.inspect_request("Create a cheat sheet on CNN")["template"] == "cheat-sheet"
    assert seen == []
    layout.body_skeleton("cheat-sheet", 0, "01", "CNN", narrow=False)
    assert seen == ["cheat-sheet.md", "footer_widgets.md"]
