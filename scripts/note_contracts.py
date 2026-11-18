"""Shared registry, safe vault paths, and Markdown measurements (no generation)."""
from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def routes() -> dict:
    return json.loads((ROOT / "references/routes.json").read_text(encoding="utf-8"))


def route_name(value: str) -> str:
    key = re.sub(r"[^a-z0-9]", "", value.lower())
    for name, spec in routes().items():
        if key in {re.sub(r"[^a-z0-9]", "", s.lower()) for s in [name, *spec.get("aliases", [])]}:
            return name
    raise ValueError(f"Unsupported template {value!r}. Choose: {', '.join(routes())}")


def resolve_vault(explicit: str | None = None) -> Path:
    value = explicit or os.environ.get("SCRIPTORIUM_VAULT_PATH")
    if not value:
        config = Path.home() / ".scriptorium-config.json"
        if config.is_file():
            value = json.loads(config.read_text(encoding="utf-8")).get("vault_path")
    if not value:
        raise ValueError("Supply a vault path or set SCRIPTORIUM_VAULT_PATH / ~/.scriptorium-config.json")
    root = Path(value).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Vault is not an existing directory: {root}")
    return root


def safe_path(root: Path, relative: str) -> Path:
    """Validate vault-relative paths, including Windows names when run on POSIX."""
    relative = str(relative).replace("\\", "/")
    parts = relative.split("/")
    if not relative or PureWindowsPath(relative).drive or relative.startswith("/"):
        raise ValueError(f"Expected a relative vault path: {relative!r}")
    for part in parts:
        if part in {"", ".", ".."} or part.startswith(".") or part.endswith((".", " ")):
            raise ValueError(f"Unsafe path component: {part!r}")
        if re.search(r'[<>:"|?*\x00-\x1f]', part) or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", part, re.I):
            raise ValueError(f"Invalid filename component: {part!r}")
    root = root.resolve()
    target = root.joinpath(*parts).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Path or symlink escapes the vault")
    return target


def body_text(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:])
    return text


def prose_lines(text: str):
    """Yield line numbers and text outside fenced code, including quoted callouts."""
    fence = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"^(?:\s*> ?)+", "", raw)
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, suffix = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence is None:
            yield n, line


def rendered_word_count(text: str) -> int:
    """Deterministic approximation documented in note_templates.md; includes code/tables."""
    text = body_text(text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"!?(?:\[\[)([^\]]+)\]\]", lambda m: re.split(r"\\?\|", m[1])[-1], text)
    text = re.sub(r"!?\[([^\]]*)\]\([^\n)]*\)", r"\1", text)
    text = re.sub(r"^\s*\[[^\]]+\]:.*$", "", text, flags=re.M)
    text = re.sub(r"https?://[^\s<>]+", "", text)
    rendered = []
    for line in text.splitlines():
        line = re.sub(r"^(?:\s*> ?)+", "", line)
        if re.match(r"^\s*(`{3,}|~{3,})", line) or re.fullmatch(r"[\s|:\-]+", line):
            continue
        line = re.sub(r"^\[![^\]]+\][+-]?\s*", "", line)
        line = re.sub(r"^\s*(?:#{1,6}\s+|[-+*]\s+|\d+\.\s+)", "", line)
        line = line.replace("\\|", " ").replace("|", " ")
        line = re.sub(r"[\$`*_~]", "", line)
        rendered.extend(t for t in line.split() if re.search(r"\w", t))
    return len(rendered)


def resources_for(entry: dict) -> list[str]:
    """Return only the chosen contract and its conditional shared modules."""
    spec = routes()[entry["template"]]
    resources = ["references/note_templates.md", "references/modules/authoring.md"]
    resources.append(entry.get("custom_template") or spec["file"])
    if entry.get("math_level", 0):
        resources.append("references/modules/math.md")
    if spec.get("verification") or entry.get("implementation_weight"):
        resources.append("references/modules/verification.md")
    return resources
