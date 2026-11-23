---
id: "moc-<topic-slug>"
aliases: ["<Topic Title> — Syllabus & Learning Graph", "<Topic Title> Syllabus", "<Topic Title> MOC"]
topic: "<Topic Title>"
tags: ["domain/<domain-slug>", "subject/<subject-slug>", "topic/<topic-slug>"]
nexttopics: ["[[01 - <Subtopic 1>]]"]
---

# <Topic Title> — Syllabus & Learning Graph

<!-- AUTHORING CONTRACT:
- Use [adaptive planning](adaptive-engine.md), [research guidance](../research/research-engine.md), and [authoring rules](../../../shared/authoring_rules.md) before selecting subtopics.
- Write this file FIRST before any `01 - <Title>.md` note is created.
- Nothing outside `allowed_subtopics` may be created during a `/scribe-notes` collection or expansion run.
- Tangential concepts must be handled with a 2-sentence inline recap + [[link]] (if in vault) or plain text—never a new .md file.
-->

## 1. Scope Boundary Contract
<!-- Keep the scope and allowlist. Include out-of-scope entries when they prevent a plausible tangent. Match the saved plan. -->
- **Core Learning Objective:** <!-- 1–2 sentences defining the exact start-to-end boundary of <Topic Title>. -->
- **In-Scope Subtopics (Strict Allowlist):**
  1. `01 - <Subtopic 1>.md` — <!-- 1-line scope -->
  2. `02 - <Subtopic 2>.md` — <!-- 1-line scope -->
- **Explicitly Out-of-Scope (Do-Not-Create Fence):**
  - **<Adjacent Topic 1>:** <!-- Why excluded; link target if it exists, else plain text. -->
  - **<Prerequisite Topic 2>:** <!-- Why excluded; 2-sentence recap rule applies. -->

## 2. Detailed Learning-Flow Graph
<!-- Keep valid dependency edges. Adapt graph layers to the actual topic and confirm the order is acyclic. -->

```mermaid
flowchart TD
    subgraph L1["Layer 1: Foundations & Axioms"]
        N1["01. <Subtopic 1>"]
    end
    subgraph L2["Layer 2: Core Mechanisms & Algorithms"]
        N2["02. <Subtopic 2>"]
    end
    subgraph L3["Layer 3: Formal Theory & Proofs"]
        N3["03. <Subtopic 3>"]
    end
    subgraph L4["Layer 4: Variants & Extensions"]
        N4["04. <Subtopic 4>"]
    end
    subgraph L5["Layer 5: Pathology & Edge Cases"]
        N5["05. <Subtopic 5>"]
    end
    N1 -->|depends| N2
    N2 -->|depends| N3
    N3 -.->|next| N4
    N4 -.->|next| N5
```

- **Topological Mastery Order:** `01` $\to$ `02` $\to$ `03` $\to$ `04` $\to$ `05`

## 3. Subtopic Manifest & Status Matrix
<!-- Keep planned note identities and their real dependencies. Update status from observed publication. -->

| Order | Note | Layer | Prerequisites (`depends_on`) | Next | Status |
|---|---|---|---|---|---|
| 01 | [[01 - <Subtopic 1>\|<Subtopic 1>]] | L1 Foundations | — | [[02 - <Subtopic 2>\|<Subtopic 2>]] | planned |
| 02 | [[02 - <Subtopic 2>\|<Subtopic 2>]] | L2 Core | [[01 - <Subtopic 1>\|<Subtopic 1>]] | — | planned |
