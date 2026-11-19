"""Extract runnable note examples and verify their published evidence."""

from __future__ import annotations

import ast
import json
import math
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
PYTHON = {"python", "py", "python3"}
FENCE_LANGS = {"cpp": {"cpp", "c++"}, "javascript": {"js", "javascript"},
               "typescript": {"ts", "typescript"}, "csharp": {"c#", "csharp"}}
PYTHON_PACKAGES = {
    "python-numpy": ("numpy",),
    "scikit-learn": ("sklearn",),
    "pytorch": ("torch",),
    "tensorflow-keras": ("tensorflow", "keras"),
}
STACK_PATTERNS = {
    "python-numpy": (
        r"(?:import|from)\s+numpy\b",
        r"\b(?:array|asarray|arange|zeros|ones|linspace)\s*\(",
        r"\b(?:dot|matmul|sum|mean|min|max|argmax|exp|tanh|maximum|reshape|einsum)\s*\(|\s(?:@|\*|\+|/|-)\s",
        r"\b(?:assert|print\s*\()",
    ),
    "scikit-learn": (r"(?:import|from)\s+sklearn\b", r"\.fit\s*\(", r"\.(?:predict\w*|score)\s*\(|\b(?:accuracy_score|mean_squared_error|classification_report|f1_score)\s*\("),
    "pytorch": (
        r"(?:import|from)\s+torch\b",
        r"\btensor\s*\(",
        r"\.backward\s*\(|\b(?:model|layer|network|net|mlp|linear|forward|relu|sigmoid|softmax|matmul|tanh)\s*\(\s*\w+\s*[,)]",
    ),
    "tensorflow-keras": (
        r"(?:import|from)\s+(?:tensorflow|keras)\b",
        r"\b(?:constant|convert_to_tensor|tensor|array)\s*\(",
        r"\.(?:fit|predict|evaluate|train_on_batch|gradient)\s*\(|\b(?:model|layer|network|net|dense|relu|sigmoid|softmax|matmul|tanh)\s*\(\s*\w+\s*[,)]",
    ),
    "c": (r"\b(?:int|void)\s+main\s*\([^)]*\)\s*\{", r"\b(?:printf|puts|assert)\s*\("),
    "cpp": (r"\bint\s+main\s*\([^)]*\)\s*\{", r"\b(?:cout|printf|assert)\b"),
    "rust": (r"\bfn\s+main\s*\([^)]*\)\s*\{|#\[test\]\s*fn\s+\w+", r"\b(?:println|assert\w*)!"),
    "sql": (r"\bCREATE\s+TABLE\b", r"\bSELECT\b", r"\bEXPLAIN\b"),
    "javascript": (r"\b(?:console\.log|assert\w*)\s*\(",),
    "typescript": (r"\b(?:console\.log|assert\w*)\s*\(",),
    "python": (r"\b(?:assert|print\s*\()",),
    "java": (r"\bstatic\s+void\s+main\s*\(", r"\b(?:println|assert)\b"),
    "go": (r"\bfunc\s+main\s*\(", r"\b(?:Println|Printf|panic)\s*\("),
    "csharp": (r"\bConsole\.Write(?:Line)?\s*\(",),
    "kotlin": (r"\bfun\s+main\s*\(", r"\b(?:println|check|assert)\s*\("),
}
EXTENSIONS = {"c": ".c", "cpp": ".cpp", "rust": ".rs", "sql": ".sql", "javascript": ".js",
              "typescript": ".ts", "java": ".java", "go": ".go", "csharp": ".cs", "kotlin": ".kt"}
TOOLS = {"c": ("gcc",), "cpp": ("g++",), "rust": ("rustc",), "javascript": ("node",),
         "typescript": ("node", "tsc"), "java": ("java",), "go": ("go",),
         "csharp": ("dotnet",), "kotlin": ("kotlinc", "java")}


@dataclass(frozen=True)
class Block:
    line: int
    lang: str
    code: str


def quoted_line(line: str, *, limit: int | None = None) -> tuple[int, str]:
    depth = 0
    while (limit is None or depth < limit) and (match := re.match(r"^\s*>\s?", line)):
        line = line[match.end():]
        depth += 1
    return depth, line


def split_blocks(text: str) -> tuple[list[Block], list[str]]:
    """Collect closed fences and mask them from prose while retaining line numbers."""
    blocks = []
    prose = []
    opening = None
    in_comment = False
    for number, original in enumerate(text.splitlines(), 1):
        depth, line = quoted_line(original, limit=opening[3] if opening else None)
        marker = FENCE.match(line)
        if opening:
            start, lang, delimiter, quote_depth = opening
            prose.append("")
            if (marker and not marker[2].strip() and depth == quote_depth
                    and marker[1][0] == delimiter[0] and len(marker[1]) >= len(delimiter)):
                blocks.append(Block(start, lang, "\n".join(contents) + ("\n" if contents else "")))
                opening = None
            else:
                contents.append(line)
        elif marker and not in_comment:
            info = marker[2].strip().lower().split(maxsplit=1)
            opening = (number, info[0] if info else "", marker[1], depth)
            contents = []
            prose.append("")
        else:
            rest = original
            visible = []
            while rest:
                if in_comment:
                    _, found, rest = rest.partition("-->")
                    if not found:
                        break
                    in_comment = False
                else:
                    before, found, rest = rest.partition("<!--")
                    visible.append(before)
                    in_comment = bool(found)
            prose.append("".join(visible))
    return blocks, prose


def check_python(blocks: list[Block]) -> list[tuple[int, str]]:
    findings = []
    for block in blocks:
        if block.lang in PYTHON:
            try:
                ast.parse(block.code)
            except SyntaxError as exc:
                findings.append((block.line + (exc.lineno or 1), f"Invalid Python syntax: {exc.msg}."))
    return findings


def _matches_stack(block: Block, stack: str) -> bool:
    langs = PYTHON if stack == "python" or stack in PYTHON_PACKAGES else FENCE_LANGS.get(stack, {stack})
    if block.lang not in langs:
        return False
    code = block.code
    if block.lang in PYTHON:
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and ast.get_docstring(node):
                    node.body = node.body[1:]
                if isinstance(node, ast.Constant) and isinstance(node.value, (str, bytes)):
                    node.value = ""
            code = ast.unparse(tree)
        except SyntaxError:
            return False
        if stack == "python" and any(re.search(rf"\b(?:import|from)\s+{module}\b", code)
                                     for modules in PYTHON_PACKAGES.values() for module in modules):
            return False
    else:
        code = re.sub(r"/\*[\s\S]*?\*/|(?m://[^\n]*|^\s*--[^\n]*)", "", code)
    return sum(bool(line.strip()) for line in code.splitlines()) >= 6 and all(
        re.search(pattern, code, re.I) for pattern in STACK_PATTERNS.get(stack, ())
    )


def required_examples(blocks: list[Block], stack: list[str]) -> tuple[dict[str, Block], list[tuple[int, str]]]:
    examples = {}
    findings = []
    for name in stack:
        matches = [block for block in blocks if _matches_stack(block, name)]
        if len(matches) != 1 or matches[0] in examples.values():
            line = matches[0].line if matches else 1
            findings.append((line, f"DM-17: {name} requires one distinct runnable block with at least six substantive lines and an exercised result."))
        else:
            examples[name] = matches[0]
    return examples, findings


def _run(command: list[str], cwd: Path, *, include_stderr: bool = False) -> str:
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace", timeout=45)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"{Path(command[0]).name} could not finish verification: {exc}") from exc
    if result.returncode:
        raise ValueError(f"{Path(command[0]).name} exited with {result.returncode}: {(result.stderr or result.stdout)[-2000:]}")
    return result.stdout + result.stderr if include_stderr else result.stdout


def _execute(block: Block, stack: str, cwd: Path) -> dict:
    packages = PYTHON_PACKAGES.get(stack, ())
    if packages:
        probe = ("import importlib.util, json; "
                 f"print(json.dumps([p for p in {packages!r} if importlib.util.find_spec(p)]))")
        available = json.loads(_run([sys.executable, "-X", "utf8", "-I", "-c", probe], cwd))
        if not available:
            return {"status": f"static verification (not executed — {packages[0]} not installed)"}
    tools = [shutil.which(name) for name in TOOLS.get(stack, ())]
    if None in tools:
        missing = TOOLS[stack][tools.index(None)]
        return {"status": f"static verification (not executed — {missing} not installed)"}

    source = cwd / ("Example" + EXTENSIONS.get(stack, ".py"))
    source.write_text(block.code, encoding="utf-8")
    if block.lang in PYTHON:
        module = next((p for p in packages if re.search(rf"\b(?:from|import)\s+{p}\b", block.code)), None)
        if module and module not in available:
            return {"status": f"static verification (not executed — {module} not installed)"}
        version = _run([sys.executable, "-X", "utf8", "-I", "-c",
                        f"import {module}; print({module}.__version__)" if module else
                        "import platform; print(platform.python_version())"], cwd).strip()
        command = [sys.executable, "-X", "utf8", "-I", str(source)]
    elif stack == "sql":
        # Execute in a separate process so SQL errors and timeouts use the same gate.
        query = ("import sqlite3, sys; from pathlib import Path; "
                 "db = sqlite3.connect(':memory:'); pending = ''; "
                 "db.set_authorizer(lambda op, *_: sqlite3.SQLITE_DENY if op in "
                 "(sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH) else sqlite3.SQLITE_OK)\n"
                 "for char in Path(sys.argv[1]).read_text(encoding='utf-8'):\n"
                 "    pending += char\n"
                 "    if char == ';' and sqlite3.complete_statement(pending):\n"
                 "        for row in db.execute(pending): print(*row, sep='\\t')\n"
                 "        pending = ''\n"
                 "if pending.strip():\n"
                 "    for row in db.execute(pending): print(*row, sep='\\t')\n")
        version = sqlite3.sqlite_version
        command = [sys.executable, "-X", "utf8", "-I", "-c", query, str(source)]
    else:
        tool = tools[0]
        executable = cwd / ("example.exe" if sys.platform == "win32" else "example")
        version = _run([tool, "--version"], cwd).splitlines()[0] if stack not in {"go", "kotlin"} else ""
        if stack in {"c", "cpp", "rust"}:
            flags = {"c": ["-std=c17"], "cpp": ["-std=c++20"], "rust": ["--test"] if "#[test]" in block.code else []}
            _run([tool, *flags[stack], str(source), "-o", str(executable)], cwd)
            command = [str(executable)]
        elif stack == "typescript":
            version += " / TypeScript " + _run([tools[1], "--version"], cwd).strip().removeprefix("Version ")
            _run([tools[1], "--target", "es2020", "--module", "commonjs", str(source)], cwd)
            command = [tool, str(source.with_suffix(".js"))]
        elif stack == "go":
            version = _run([tool, "version"], cwd).strip()
            command = [tool, "run", str(source)]
        elif stack == "kotlin":
            version = _run([tool, "-version"], cwd, include_stderr=True).strip()
            jar = cwd / "example.jar"
            _run([tool, str(source), "-include-runtime", "-d", str(jar)], cwd)
            command = [tools[1], "-jar", str(jar)]
        elif stack == "csharp":
            command = [tool, "run", "--file", str(source)]
        else:
            command = [tool, str(source)]
    return {"status": "executed", "version": version, "stdout": _run(command, cwd)}


def verify_runtimes(examples: dict[str, Block], prose: list[str]) -> dict[str, dict]:
    evidence = {}
    for stack, block in examples.items():
        with tempfile.TemporaryDirectory(prefix="scriptorium-example-") as directory:
            try:
                evidence[stack] = _execute(block, stack, Path(directory))
            except ValueError as exc:
                raise ValueError(f"{stack} example at line {block.line}: {exc}") from exc
    outputs = [result["stdout"] for result in evidence.values() if result["status"] == "executed"]
    workflow_only = any(re.match(
        r"^(?:\*\*)?Parity(?:\*\*)?:(?:\*\*)?\s*workflow-only\s+\S", line, re.I
    ) for line in prose)
    if len(outputs) >= 2 and (not workflow_only or any(re.search(r"^PARITY:", stdout, re.M) for stdout in outputs)):
        values = []
        for stdout in outputs:
            rows = re.findall(r"^PARITY:\s*(.+)$", stdout, re.M)
            try:
                row = json.loads(rows[0]) if len(rows) == 1 else None
                if not isinstance(row, list) or not row or not all(type(v) in {int, float} and math.isfinite(v) for v in row):
                    raise ValueError()
            except (ValueError, OverflowError) as exc:
                raise ValueError("DM-18: each executed stack must print one PARITY: JSON array of finite numbers.") from exc
            values.append(row)
        if any(len(row) != len(values[0]) or any(
            not math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-8)
            for actual, expected in zip(row, values[0])
        ) for row in values[1:]):
            raise ValueError("DM-18: executed stacks disagree on the shared fixture (rel_tol=1e-6, abs_tol=1e-8).")
    return evidence


def check_evidence(evidence: dict[str, dict], blocks: list[Block], prose: list[str]) -> None:
    for stack, result in evidence.items():
        heading = re.compile(rf"^### (?:\d+\.\d+ )?Verification — {re.escape(stack)}$")
        headings = [n for n, line in enumerate(prose, 1) if heading.fullmatch(line)]
        if len(headings) != 1:
            raise ValueError(f"DM-18: add one '### Verification — {stack}' section.")
        start = headings[0]
        end = next((n for n, line in enumerate(prose, 1) if n > start and re.match(r"^#{1,3} ", line)), len(prose) + 1)
        section = [line.strip() for line in prose[start:end - 1]]
        if [line for line in section if line.startswith("Status:")] != [f"Status: {result['status']}"]:
            raise ValueError(f"DM-18: {stack} requires Status: {result['status']}.")
        versions = [line for line in section if line.startswith("Version:")]
        output = [block.code for block in blocks if start < block.line < end and block.lang in {"text", "plaintext"}]
        if result["status"] == "executed":
            expected_versions = [f"Version: {result['version']}"] if result["version"] else []
            if versions != expected_versions:
                raise ValueError(f"DM-18: record only the observed version for {stack}: {result['version']}.")
            if output != [result["stdout"].removesuffix("\n") + ("\n" if result["stdout"] else "")]:
                raise ValueError(f"DM-18: paste the verbatim {stack} stdout in one text fence.")
        elif versions or output:
            raise ValueError(f"DM-18: {stack} is static-only. Remove the version and observed output.")
