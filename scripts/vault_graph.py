#!/usr/bin/env python3
"""Read-only Obsidian vault graph & DAG topology analyzer for Scriptorium.

Reuses `scripts/vault_index.py` (preserving symlink containment, cache, and
zero-JS guarantees) to analyze:
  - `depends_on` & `next_topic` DAG cycles
  - Topological study order (`topo_order`)
  - Broken / unresolved wikilinks (frontmatter and body)
  - Ambiguous basename targets
  - Orphaned (zero incoming links) and isolated (zero in/out) notes
  - Mermaid flowchart export (`--format mermaid`)

Usage:
  python3 scripts/vault_graph.py "<vault_path>" [--topic "<filter>"] [--format json|mermaid|text]
  python3 scripts/vault_graph.py "<vault_path>" --check-cycles [--strict]
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from vault_index import _filter_notes_by_topic, build_or_load_index, resolve_vault_root


def _strip_wikilink(raw: str) -> str:
    s = raw.strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2].strip()
    if "|" in s:
        s = s.split("|", 1)[0]
    if "#" in s:
        s = s.split("#", 1)[0]
    return s.strip()


def _build_lookup(notes: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Map normalized identifiers (rel path, stem, id, title, aliases) -> list of note file paths."""
    lookup: dict[str, list[str]] = defaultdict(list)

    def _add(key: str | None, file_path: str) -> None:
        if not key:
            return
        k = key.strip().lower()
        if not k:
            return
        if file_path not in lookup[k]:
            lookup[k].append(file_path)

    for n in notes:
        rel = n["file"]
        p = Path(rel)
        rel_no_ext = rel[:-3] if rel.lower().endswith(".md") else rel
        _add(rel, rel)
        _add(rel_no_ext, rel)
        _add(p.stem, rel)
        _add(n.get("id"), rel)
        _add(n.get("title"), rel)
        for alias in n.get("aliases") or []:
            _add(alias, rel)
    return lookup


def _resolve_target(raw_link: str, lookup: dict[str, list[str]]) -> tuple[str | None, list[str]]:
    """Resolve a raw wikilink or target string to a unique note file path.

    Returns (resolved_file_or_None, all_candidate_files).
    """
    target = _strip_wikilink(raw_link)
    if not target:
        return None, []
    candidates = lookup.get(target.lower(), [])
    if len(candidates) == 1:
        return candidates[0], candidates
    if len(candidates) > 1:
        return None, candidates
    return None, []


def _find_cycles(nodes: list[str], adj: dict[str, list[str]]) -> list[list[str]]:
    """Find elementary directed cycles using deterministic DFS (0=unvisited, 1=visiting, 2=done)."""
    state: dict[str, int] = {n: 0 for n in nodes}
    stack: list[str] = []
    cycles: list[list[str]] = []
    seen_sigs: set[tuple[str, ...]] = set()

    def _dfs(u: str) -> None:
        state[u] = 1
        stack.append(u)
        for v in sorted(set(adj.get(u, []))):
            if v not in state:
                continue
            if state[v] == 1:
                idx = stack.index(v)
                cyc = stack[idx:] + [v]
                # Canonicalize cycle signature to avoid duplicates
                core = cyc[:-1]
                min_i = min(range(len(core)), key=lambda i: core[i])
                sig = tuple(core[min_i:] + core[:min_i])
                if sig not in seen_sigs:
                    seen_sigs.add(sig)
                    cycles.append(cyc)
            elif state[v] == 0:
                _dfs(v)
        stack.pop()
        state[u] = 2

    for n in sorted(nodes):
        if state[n] == 0:
            _dfs(n)
    return cycles


def _topological_sort(nodes: list[str], prereq_to_dep: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    """Kahn's topological sort; returns (ordered_nodes, cyclic_or_blocked_nodes)."""
    in_deg: dict[str, int] = {n: 0 for n in nodes}
    for u in nodes:
        for v in set(prereq_to_dep.get(u, [])):
            if v in in_deg:
                in_deg[v] += 1

    q = deque(sorted(n for n, d in in_deg.items() if d == 0))
    order: list[str] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in sorted(set(prereq_to_dep.get(u, []))):
            if v not in in_deg:
                continue
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)

    remaining = sorted(n for n in nodes if n not in set(order))
    return order, remaining


def analyze_vault_graph(
    vault_path: Path,
    topic_filter: str | None = None,
    *,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Analyze the link and dependency topology of a Scriptorium vault (or topic slice)."""
    full = build_or_load_index(vault_path, use_cache=use_cache)
    all_notes = full["notes"]
    scoped_notes = _filter_notes_by_topic(all_notes, topic_filter) if topic_filter else all_notes

    # Lookup resolves against the full vault so cross-topic links aren't falsely flagged broken
    full_lookup = _build_lookup(all_notes)
    scoped_files = {n["file"] for n in scoped_notes}
    notes_by_file = {n["file"]: n for n in scoped_notes}

    # Graph adjacency within scoped notes
    # prereq_to_dep: prereq -> note (learning progression order)
    prereq_to_dep: dict[str, list[str]] = defaultdict(list)
    # dep_edges: note -> prereq (for depends_on cycle detection, equivalent direction)
    next_edges: list[tuple[str, str]] = []
    body_edges: list[tuple[str, str]] = []
    depends_edges: list[tuple[str, str]] = []  # (prereq, note)

    in_links: dict[str, set[str]] = {f: set() for f in scoped_files}
    out_links: dict[str, set[str]] = {f: set() for f in scoped_files}
    broken_links: list[dict[str, str]] = []
    ambiguous_links: list[dict[str, Any]] = []

    for n in scoped_notes:
        src = n["file"]

        # 1. depends_on
        for raw_dep in n.get("depends_on") or []:
            target, cands = _resolve_target(raw_dep, full_lookup)
            if target is None:
                if len(cands) > 1:
                    ambiguous_links.append({"source": src, "field": "depends_on", "target": raw_dep, "candidates": cands})
                else:
                    broken_links.append({"source": src, "field": "depends_on", "target": raw_dep})
                continue
            if target in scoped_files and target != src:
                prereq_to_dep[target].append(src)
                depends_edges.append((target, src))
                out_links[src].add(target)
                in_links[target].add(src)
            elif target != src:
                # Cross-topic dependency still counts as an outgoing link for src
                out_links[src].add(target)

        # 2. next_topic
        raw_next = n.get("next_topic")
        if raw_next:
            target, cands = _resolve_target(raw_next, full_lookup)
            if target is None:
                if len(cands) > 1:
                    ambiguous_links.append({"source": src, "field": "next_topic", "target": raw_next, "candidates": cands})
                else:
                    broken_links.append({"source": src, "field": "next_topic", "target": raw_next})
            elif target in scoped_files and target != src:
                next_edges.append((src, target))
                out_links[src].add(target)
                in_links[target].add(src)
            elif target != src:
                out_links[src].add(target)

        # 3. body wikilinks
        for raw_link in n.get("links") or []:
            target, cands = _resolve_target(raw_link, full_lookup)
            if target is None:
                if len(cands) > 1:
                    ambiguous_links.append({"source": src, "field": "body", "target": raw_link, "candidates": cands})
                else:
                    broken_links.append({"source": src, "field": "body", "target": raw_link})
                continue
            if target in scoped_files and target != src:
                body_edges.append((src, target))
                out_links[src].add(target)
                in_links[target].add(src)
            elif target != src:
                out_links[src].add(target)

    scoped_list = sorted(scoped_files)
    depends_cycles = _find_cycles(scoped_list, prereq_to_dep)

    next_adj: dict[str, list[str]] = defaultdict(list)
    for u, v in next_edges:
        next_adj[u].append(v)
    next_cycles = _find_cycles(scoped_list, next_adj)

    topo_order, blocked_by_cycle = _topological_sort(scoped_list, prereq_to_dep)

    orphans = sorted(f for f in scoped_list if len(in_links[f]) == 0)
    isolated = sorted(f for f in scoped_list if len(in_links[f]) == 0 and len(out_links[f]) == 0)

    return {
        "vault_root": full["vault_root"],
        "topic_filter": topic_filter,
        "summary": {
            "note_count": len(scoped_list),
            "depends_edge_count": len(set(depends_edges)),
            "next_edge_count": len(set(next_edges)),
            "body_edge_count": len(set(body_edges)),
            "depends_cycle_count": len(depends_cycles),
            "next_cycle_count": len(next_cycles),
            "broken_link_count": len(broken_links),
            "ambiguous_link_count": len(ambiguous_links),
            "orphan_count": len(orphans),
            "isolated_count": len(isolated),
        },
        "depends_cycles": depends_cycles,
        "next_cycles": next_cycles,
        "topo_order": topo_order,
        "blocked_by_cycle": blocked_by_cycle,
        "broken_links": broken_links,
        "ambiguous_links": ambiguous_links,
        "orphans": orphans,
        "isolated": isolated,
        "edges": {
            "depends_on": sorted(set(depends_edges)),
            "next_topic": sorted(set(next_edges)),
            "body": sorted(set(body_edges)),
        },
        "nodes": {
            f: {
                "title": notes_by_file[f].get("title") or Path(f).stem,
                "note_type": notes_by_file[f].get("note_type"),
                "in_degree": len(in_links[f]),
                "out_degree": len(out_links[f]),
            }
            for f in scoped_list
        },
    }


def format_mermaid(report: dict[str, Any], *, include_body_links: bool = False) -> str:
    """Render the analyzed graph as a Mermaid flowchart LR diagram."""
    nodes = report["nodes"]
    id_map = {f: f"N{idx}" for idx, f in enumerate(sorted(nodes.keys()), start=1)}

    lines = ["flowchart LR"]
    for f in sorted(nodes.keys()):
        label = str(nodes[f]["title"]).replace('"', "'")
        lines.append(f'  {id_map[f]}["{label}"]')

    seen_edges: set[tuple[str, str, str]] = set()
    for prereq, dep in report["edges"]["depends_on"]:
        if prereq in id_map and dep in id_map:
            key = (prereq, dep, "dep")
            if key not in seen_edges:
                seen_edges.add(key)
                lines.append(f"  {id_map[prereq]} -->|depends| {id_map[dep]}")

    for src, nxt in report["edges"]["next_topic"]:
        if src in id_map and nxt in id_map:
            key = (src, nxt, "next")
            if key not in seen_edges:
                seen_edges.add(key)
                lines.append(f"  {id_map[src]} -.->|next| {id_map[nxt]}")

    if include_body_links:
        for src, dst in report["edges"]["body"]:
            if src in id_map and dst in id_map:
                key = (src, dst, "body")
                if key not in seen_edges:
                    seen_edges.add(key)
                    lines.append(f"  {id_map[src]} -.-> {id_map[dst]}")

    return "\n".join(lines)


def format_text_summary(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        f"Vault Graph Summary (notes={s['note_count']}, depends={s['depends_edge_count']}, next={s['next_edge_count']}, body={s['body_edge_count']})",
        f"  Depends cycles : {s['depends_cycle_count']}",
        f"  Next cycles    : {s['next_cycle_count']}",
        f"  Broken links   : {s['broken_link_count']}",
        f"  Ambiguous links: {s['ambiguous_link_count']}",
        f"  Orphans (in=0) : {s['orphan_count']}",
        f"  Isolated       : {s['isolated_count']}",
    ]
    if report["depends_cycles"]:
        lines.append("Cycles (depends_on):")
        for cyc in report["depends_cycles"]:
            lines.append("  - " + " -> ".join(cyc))
    if report["broken_links"]:
        lines.append("Broken links:")
        for b in report["broken_links"]:
            lines.append(f"  - [{b['field']}] {b['source']} -> {b['target']}")
    if report["isolated"]:
        lines.append("Isolated notes:")
        for iso in report["isolated"]:
            lines.append(f"  - {iso}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze Scriptorium vault link & dependency graph.")
    parser.add_argument("vault_path", nargs="?", help="Path to Obsidian vault.")
    parser.add_argument("--topic", help="Filter analysis to notes matching a topic.")
    parser.add_argument(
        "--format",
        choices=("json", "mermaid", "text"),
        default="json",
        help="Output format (default: json).",
    )
    parser.add_argument(
        "--include-body-links",
        action="store_true",
        help="Include body wikilink edges in Mermaid output.",
    )
    parser.add_argument(
        "--check-cycles",
        action="store_true",
        help="Exit with code 1 if any depends_on cycle is detected.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if cycles or broken links are detected.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Bypass vault index cache.")
    args = parser.parse_args(argv)

    try:
        vault_root = resolve_vault_root(args.vault_path)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = analyze_vault_graph(vault_root, topic_filter=args.topic, use_cache=not args.no_cache)

    if args.format == "json":
        # Keep default JSON compact by omitting verbose full edge list unless needed
        compact = dict(report)
        compact.pop("edges", None)
        print(json.dumps(compact, indent=2))
    elif args.format == "mermaid":
        print(format_mermaid(report, include_body_links=args.include_body_links))
    else:
        print(format_text_summary(report))

    has_cycles = bool(report["depends_cycles"])
    has_broken = bool(report["broken_links"])
    if args.strict and (has_cycles or has_broken):
        return 1
    if args.check_cycles and has_cycles:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
