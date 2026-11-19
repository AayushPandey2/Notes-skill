"""Audit local Markdown connectivity and script CLI declarations; no vault mutation.

Implements shared/authoring_rules.md#links-and-placement and routing bindings.
Outputs compact JSON; external URLs and parameterized examples are not fetched.
"""
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

def slug(value):
    return re.sub(r"[^\w -]", "", value).lower().replace(" ", "-")

def audit(root=ROOT):
    errors = []
    checked = 0
    files = [p for p in root.rglob("*") if p.is_file() and not any(
        x in p.parts for x in (".git", "__pycache__", ".pytest_cache"))]
    for path in files:
        if path.suffix not in {".md", ".py"}:
            continue
        text = path.read_text(encoding="utf-8-sig")
        if path.suffix == ".py":
            ast.parse(text, filename=str(path))
            continue
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"(?:https?:|mailto:|plugin:)", target) or any(x in target for x in ("<", ">", "*")):
                continue
            name, _, anchor = unquote(target).partition("#")
            dest = (path.parent / name).resolve() if name else path
            checked += 1
            if not dest.is_file():
                errors.append({"file": str(path.relative_to(root)), "target": target, "fix": "Resolve local target"})
            elif anchor and dest.suffix == ".md":
                headings = re.findall(r"^#+ (.+)$", dest.read_text(encoding="utf-8-sig"), re.M)
                if anchor not in {slug(h) for h in headings}:
                    errors.append({"file": str(path.relative_to(root)), "target": target, "fix": "Resolve heading anchor"})
        for script, arguments in re.findall(r"scripts/([\w]+\.py)([^\n]*)", text):
            dest = root / "scripts" / script
            if not dest.is_file():
                errors.append({"file": str(path.relative_to(root)), "target": script, "fix": "Resolve script path"})
                continue
            if not arguments.startswith(")"):
                arguments = arguments.split("`", 1)[0]
            implementation = dest.read_text(encoding="utf-8")
            for flag in re.findall(r"--[a-z][a-z-]+", arguments):
                if flag not in implementation:
                    errors.append({"file": str(path.relative_to(root)), "target": script + " " + flag, "fix": "Resolve CLI flag"})
    return {"files": len(files), "local_links": checked, "errors": errors}

if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(bool(result["errors"]))
