"""Exercise source-study, math routing, and executable evidence through publish."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from decision_matrix import audit_note_against_contract, resolve_decisions
from note_layout import ROUTES, section_layout
from note_verification import Block, verify_runtimes
from validate_note import validate_text


def cli(script, *args, expected=0):
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(ROOT / "scripts" / f"{script}.py"), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result.stdout + result.stderr


def start(vault, request, topic, title, **item_options):
    outline = vault / "outline.json"
    item = {"title": title, "purpose": "explain", "impl_weight": "low", "density": "cohesive",
            "routing_reason": "Teach the selected outcome.", **item_options}
    outline.write_text(json.dumps([item]), encoding="utf-8")
    result = yaml.safe_load(cli("plan_notes", "start", vault, "--request", request, "--topic-folder",
                                ".", "--topic", topic, "--outline", outline))
    return result["plan_id"], result["plan"][0]


def draft_for(vault, item, topic, body):
    scaffold = cli("scaffold_note", "--template", item["template"], "--math-level", item["math_level"],
                   "--topic", topic, "--title", item["title"], "--id", item["note_id"])
    frontmatter = scaffold.split("---", 2)[1]
    draft = vault.parent / f"{vault.name}-draft.md"
    draft.write_text(f"---{frontmatter}---\n\n# {item['title']}\n\n{body}", encoding="utf-8")
    return draft


def test_all_live_template_gates_use_shared_ids_and_source_template_has_five_keys():
    matrix = (ROOT / "shared" / "notes_decision_matrix.md").read_text(encoding="utf-8")
    ids = set(re.findall(r"^## (DM-\d\d)$", matrix, re.M))
    for route in set(ROUTES) - {"deepstudy-coding", "deepstudy-general"}:
        source = (ROOT / "templates" / f"{route}.md").read_text(encoding="utf-8")
        assert "../shared/notes_decision_matrix.md" in source
        for section in re.split(r"^#{2,6} .+\n", source, flags=re.M)[1:]:
            assert route == "deepstudy-master" or ("Gate:" in section or "Decision-matrix IDs:" in section)
            assert set(re.findall(r"\bDM-\d\d\b", section)) <= ids
        if route == "studynotes":
            assert list(yaml.safe_load(source.split("---", 2)[1])) == ["id", "aliases", "topic", "tags", "nexttopics"]
            assert not re.search("teacher|student|class|lecture", source, re.I)


@pytest.mark.parametrize("partial", [False, True])
def test_qualitative_article_and_partial_video_publish(tmp_path, partial):
    source_url = "https://www.youtube.com/watch?v=fixture" if partial else "https://example.org/article/one"
    topic = "History"
    plan, item = start(tmp_path, f"/scribe-notes {source_url}", topic, "Records and witnesses")
    assert item["template"] == "studynotes"
    assert item["domain"] == "social-studies-humanities" and item["math_level"] == 0
    headings = [heading for _, heading in section_layout("studynotes", 0)]
    access = "Only the opening transcript excerpt was available." if partial else "The complete supplied article was available."
    locator = "[00:15](https://www.youtube.com/watch?v=fixture&t=15s)" if partial else "[Opening paragraph](https://example.org/article/one#opening)"
    body = (
        f"{headings[0]}\n\n> [!info] Source & Scope Context\n> {access}\n\n"
        "Identify the distinction between an account and the evidence behind it.\n\n"
        f"{headings[1]}\n\n### 2.1 Who recorded the account?\n\n"
        f"The supplied passage distinguishes witnesses from later accounts. {locator}\n\n"
        f"{headings[-1].replace('## 6.', '## 3.')}\n\n"
        "Which account is closest to the event? Check when its author recorded it.\n"
    )
    draft = draft_for(tmp_path, item, topic, body)
    assert "published" in cli("plan_notes", "publish", tmp_path, plan, item["id"], draft)


def test_forward_pass_honors_explicit_math_and_omits_code(tmp_path):
    topic = "Neural Networks"
    plan, item = start(tmp_path, "/scribe-deepnotes Neural Networks", topic, "Forward pass", math_level=2)
    assert (item["math_level"], item["verification_stack"]) == (2, [])
    assert "clamped_from" not in item
    body = (
        "## Worked prediction\nLet $W$ denote a 1 by 2 row of weights, $x$ a 2 by 1 input, and $b$ a scalar bias.\n\n"
        "$$z = Wx + b$$\n\n"
        "For example, a row of weights (2, 1), input (3, 5), and bias 4 yield 15, a single output value.\n\n"
        "## Deriving the affine output\nThe dot product sums each input multiplied by its weight.\n"
        "Expanding the two coordinates gives $z = w_1 x_1 + w_2 x_2 + b$ by distributivity.\n"
    )
    draft = draft_for(tmp_path, item, topic, body)
    assert "published" in cli("plan_notes", "publish", tmp_path, plan, item["id"], draft)


def with_verification(body, evidence):
    for stack, result in evidence.items():
        body += f"\n### Verification — {stack}\n\nStatus: {result['status']}\n"
        if result["status"] == "executed":
            body += f"Version: {result['version']}\n\n```text\n{result['stdout']}```\n"
    return body


def test_backprop_derivation_uses_one_gradient_check_and_exports(tmp_path):
    topic = "Neural Networks"
    plan, item = start(tmp_path, "/scribe-deepnotes Neural Networks", topic, "Backpropagation derivation",
                       math_level=2, implementation_stack=["python"])
    assert item["domain"] == "ml-theory" and item["math_level"] == 2
    assert item["decision_contract"]["implementation_stack"] == ["python"]
    body = (
        "## Derivation\nLet $x$ denote the real input, $w$ the real weight, and $z$ their product.\n\n"
        "1. Assume $x$ is fixed and define the squared loss.\n\n"
        "$$L = (wx)^2 / 2$$\n\n"
        "2. Use the chain rule because the loss depends on $w$ through $z$.\n\n"
        "$$\\frac{dL}{dw} = zx = wx^2$$\n\n"
        "## Limits\n- With zero input the derivative vanishes at any weight.\n"
        "- With nonzero input and zero weight the derivative vanishes only at that weight.\n\n"
        "## Gradient check\n```python\ndef loss(w, x):\n    return (w * x) ** 2 / 2\n"
        "weight, x = 2.0, 3.0\nstep = 1e-4\n"
        "numeric = (loss(weight + step, x) - loss(weight - step, x)) / (2 * step)\n"
        "assert abs(numeric - weight * x ** 2) < 1e-8\nprint(round(numeric, 6))\n```\n"
    )
    draft = draft_for(tmp_path, item, topic, body)
    preview = json.loads(cli("plan_notes", "verify-runtimes", tmp_path, plan, item["id"], draft))
    assert preview["python"]["stdout"] == "18.0\n"
    draft = draft_for(tmp_path, item, topic, with_verification(body, preview).replace("18.0", "19.0"))
    assert "paste the verbatim python stdout" in cli(
        "plan_notes", "publish", tmp_path, plan, item["id"], draft, expected=2,
    )
    draft = draft_for(tmp_path, item, topic, with_verification(body, preview))
    assert "published" in cli("plan_notes", "publish", tmp_path, plan, item["id"], draft, "--export-code")
    examples = list((tmp_path / "assets" / "neural-networks" / "examples").glob("*.py"))
    assert len(examples) == 1 and "assert abs" in examples[0].read_text(encoding="utf-8")
    assert "already complete" in cli("plan_notes", "publish", tmp_path, plan, item["id"], draft, "--export-code")


def test_domain_stacks_downgrades_and_detached_implementations():
    stacks = {
        "Perceptron": ["python-numpy", "scikit-learn", "pytorch"],
        "Activation Functions": ["python-numpy", "pytorch", "tensorflow-keras"],
        "Dynamic Programming": ["python", "cpp"],
        "Arrays": ["c", "rust"],
        "SQL Joins": ["sql"],
        "Event Loop": ["typescript", "javascript"],
    }
    for topic, stack in stacks.items():
        contract = resolve_decisions(topic, {"title": "Implementations", "math_level": 3}, topic)
        assert contract["implementation_stack"] == stack[:1] and contract["math_level"] == 3
        assert resolve_decisions(topic, {"title": "Mechanism", "math_level": 0}, topic)["implementation_stack"] == []
    assert resolve_decisions("Implement arrays in Rust and Python", {"title": "Implementations"}, "Arrays")[
        "implementation_stack"] == ["rust", "python"]
    for topic, expected in (("Physics", 3), ("Pure Mathematics", 3), ("Arrays", 3), ("Sociology", 3)):
        assert resolve_decisions("", {"title": "Core ideas", "math_level": 3}, topic)["math_level"] == expected
    assert resolve_decisions("", {"title": "Historical Overview", "math_level": 2}, "Physics")["math_level"] == 2
    with pytest.raises(ValueError, match="at most math_level 1"):
        resolve_decisions("", {"template": "summary", "math_level": 2}, "Physics")
    assert resolve_decisions("", {"math_level": 2}, "Arrays", allow_math_override=True)["math_level"] == 2


def test_audit_rejects_stub_math_bloat_and_invalid_python():
    contract = resolve_decisions("", {"title": "Implementations", "math_level": 2}, "MLP")
    draft = "## Implementation\n\n$$z = Wx + b$$\n\n```python\nimport torch\nmodel = torch.nn.Sequential()\n```\n"
    messages = [message for _, message in audit_note_against_contract(draft, contract)]
    assert not any("math_level 0 forbids" in message for message in messages)
    assert any("python-numpy requires" in message for message in messages)
    assert not any("Shared fixture" in message for message in messages)
    metadata = "---\nid: invalid\naliases: [Invalid]\ntopic: MLP\ntags: [mlp]\nnexttopics: []\n---\n"
    invalid = metadata + "# Invalid\n\nBroken Python.\n\n~~~py\ndef missing:\n~~~\n"
    assert any("Invalid Python syntax" in message for _, message in validate_text(invalid, route="deepstudy-master"))


def test_numeric_parity_checks_outputs_from_two_actual_runtimes(monkeypatch):
    python = Block(1, "python", 'print("PARITY: [5]")\n')
    sql = Block(2, "sql", "SELECT 'PARITY: [5.00000001]';\n")
    evidence = verify_runtimes({"python": python, "sql": sql}, [])
    assert all(result["status"] == "executed" for result in evidence.values())
    with pytest.raises(ValueError, match="disagree on the shared fixture"):
        verify_runtimes({"python": python, "sql": Block(2, "sql", "SELECT 'PARITY: [9]';\n")}, [])
    monkeypatch.setattr("note_verification.shutil.which", lambda _: None)
    assert verify_runtimes({"rust": Block(1, "rust", "fn main() {}")}, [])["rust"] == {
        "status": "static verification (not executed — rustc not installed)",
    }
