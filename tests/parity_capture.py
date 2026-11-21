"""Read-only Python migration inventory and reproducible baseline measurements.

Run with Python while the reference runtime is retained. Writes only the selected
report directory; fixtures and temporary asset writes remain outside the vault.
This is migration tooling, not part of the maintained Scriptorium runtime.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def capture_inventory() -> dict:
    names = subprocess.check_output(["git", "ls-files", "*.py"], cwd=ROOT, text=True).splitlines()
    modules = {name[:-3].replace("/", "."): name for name in names}
    modules.update({name.removesuffix(".__init__"): path for name, path in list(modules.items())
                    if name.endswith(".__init__")})
    entries = []
    for name in names:
        source = (ROOT / name).read_text(encoding="utf-8-sig")
        tree = ast.parse(source)
        module_name = name[:-3].replace("/", ".")
        package = module_name.removesuffix(".__init__") if module_name.endswith(".__init__") else module_name.rpartition(".")[0]
        imports, dependencies, contracts, errors, fs, external = set(), set(), [], set(), [], []
        for node in ast.walk(tree):
            imported = []
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                target = "." * node.level + (node.module or "")
                if node.level:
                    target = importlib.util.resolve_name(target, package)
                imported = [target, *[target + "." + alias.name for alias in node.names]]
            imports.update(imported)
            dependencies.update(modules[item] for item in imported if item in modules)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                contracts.append({"name": node.name, "line": node.lineno,
                    "input_signature": ast.unparse(node.args),
                    "return_annotation": ast.unparse(node.returns) if node.returns else None,
                    "documentation": ast.get_docstring(node),
                    "note": "Missing annotations require behavioral fixture review; signatures alone do not establish parity."})
            if isinstance(node, ast.Raise) and node.exc:
                errors.add(ast.unparse(node.exc))
            if isinstance(node, ast.ExceptHandler):
                errors.add("handles " + (ast.unparse(node.type) if node.type else "all exceptions"))
            if isinstance(node, ast.Call):
                call = ast.unparse(node.func)
                if call.rsplit(".", 1)[-1] in {"read_text", "read_bytes", "write_text", "write_bytes", "open", "mkdir", "unlink", "replace", "rename", "rglob", "glob", "iterdir", "link", "fsync", "NamedTemporaryFile", "TemporaryDirectory"}:
                    fs.append({"line": node.lineno, "call": ast.unparse(node)[:350]})
                if call.startswith(("subprocess.", "socket.", "http.", "urllib.", "ssl.")) or call in {"_run", "_request_once", "fetch_image"}:
                    external.append({"line": node.lineno, "call": ast.unparse(node)[:350]})
        category = "regression_test" if name.startswith("tests/") else "example_or_educational" if name.startswith("examples/") else "runtime"
        tests = [test for test in names if test.startswith("tests/") and any(
            item in (ROOT / test).read_text(encoding="utf-8-sig")
            for item in {module_name, Path(name).stem})]
        entries.append({"python_file": name, "category": category, "lines": len(source.splitlines()),
            "responsibility": (ast.get_docstring(tree) or "Package boundary or compatibility exports").splitlines()[0],
            "imports": sorted(imports), "internal_dependencies": sorted(dependencies - {name}), "callers": [],
            "function_contracts": contracts, "error_contracts": sorted(errors), "filesystem_calls": fs,
            "external_calls": external, "candidate_tests_by_static_reference": tests,
            "migration_status": "pending" if category == "runtime" else "retained_reference",
            "rust_replacement": None, "parity": "unverified", "removal_decision": "retain"})
    by_name = {entry["python_file"]: entry for entry in entries}
    for entry in entries:
        for dep in entry["internal_dependencies"]:
            by_name[dep]["callers"].append(entry["python_file"])
    return {"captured_at": datetime.now(timezone.utc).isoformat(),
        "reference_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "method": "AST signatures, imports, exception handlers and side-effect call sites plus static test references. Dynamic dispatch and semantic equivalence require manual review and parity fixtures.",
        "files": entries, "counts": {"all_python": len(entries),
            "runtime_python": sum(entry["category"] == "runtime" for entry in entries)}}


def measure(call, repeats: int, iterations: int = 1) -> dict:
    # One unmeasured warmup. No network or model requests are issued.
    call()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        for _ in range(iterations):
            call()
        samples.append((time.perf_counter_ns() - start) / iterations / 1_000_000)
    return {"unit": "milliseconds_per_operation", "iterations_per_sample": iterations,
        "samples": samples, "median": statistics.median(samples), "minimum": min(samples)}


def capture_benchmarks(repeats: int) -> dict:
    sys.path.insert(0, str(ROOT))
    from scriptorium.engines.vault import build_obsidian_properties, validate_obsidian_properties
    from scriptorium.models import content_hash, dump_frontmatter, parse_frontmatter
    from scriptorium.engines.composition.visuals import scientific_svg, validate_svg
    from scriptorium.engines._token_optimizer import MultiLevelCache
    import yaml

    props = build_obsidian_properties(topic="Gradient Descent", note_type="deep-notes")
    note = dump_frontmatter(props) + "\n\n# Gradient Descent\n\nA representative validation input.\n"
    manifest = {"schema_version": 1, "notes": [{"path": f"{i}.md", "hash": content_hash(note)} for i in range(100)]}
    raw = note.encode("utf-8") * 1000
    cache = MultiLevelCache()
    cache_key = cache.build_key("L9_validation_result", dependencies={"note_hash": content_hash(note)})
    cache.put(cache_key, {"valid": True})
    config = (ROOT / "references/routing/master-registry.yaml").read_text(encoding="utf-8-sig")
    plots = {"quadratic": [(float(i), float(i * i)) for i in range(-20, 21)]}
    results = {}
    for label, argv in {
        "process_startup_help": ["scripts/scribe.py", "--help"],
        "properties_cli": ["scripts/scribe.py", "properties", "--topic", "Gradient Descent", "--format", "json"],
        "routing_cli": ["scripts/scribe.py", "route", "/scribe-notes Explain gradient descent"],
    }.items():
        results[label] = measure(lambda args=argv: subprocess.run(
            [sys.executable, *args], cwd=ROOT, capture_output=True, check=True), repeats)
    for label, call, count in [
        ("configuration_yaml_parse", lambda: yaml.safe_load(config), 10),
        ("frontmatter_parse", lambda: parse_frontmatter(note), 100),
        ("metadata_validation", lambda: validate_obsidian_properties(note), 100),
        ("asset_sha256", lambda: content_hash(raw), 100),
        ("manifest_serialization", lambda: json.dumps(manifest, sort_keys=True), 100),
        ("memory_cache_lookup", lambda: cache.get(cache_key), 1000),
        ("scientific_svg_render_verify", lambda: validate_svg(scientific_svg(plots, title="Quadratic", xlabel="x", ylabel="x squared")), 100),
    ]:
        results[label] = measure(call, repeats, count)
    with tempfile.TemporaryDirectory(prefix="scriptorium-baseline-") as temp:
        path = Path(temp) / "manifest.json"
        data = json.dumps(manifest, sort_keys=True).encode()
        results["filesystem_manifest_write_read"] = measure(lambda: (path.write_bytes(data), path.read_bytes()), repeats, 100)
    return {"captured_at": datetime.now(timezone.utc).isoformat(), "runtime": sys.version,
        "platform": platform.platform(), "warmups": 1, "repeats": repeats,
        "scope": "Local deterministic Python baseline. Process CLI measurements include interpreter startup and imports. No model, research, network download or end-to-end authorship timing is represented. File measurement is buffered write/read, not atomic durable publication.",
        "results": results, "rust_comparison": "Not yet measured; no speedup claim is supported."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs")
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 3:
        parser.error("Use at least three measured repeats")
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, data in [("rust-migration-inventory.json", capture_inventory()),
                           ("rust-migration-python-baseline.json", capture_benchmarks(args.repeats))]:
        path = args.output / filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
