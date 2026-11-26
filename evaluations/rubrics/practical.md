# Evaluation Rubric: Practical & Lab Quality (Evaluation-Only)

*Load only during evaluation or when explicitly requested as an evaluation rubric—do not load during normal note authoring.*

| Dimension | Pass Standard (Cite Supporting Passage) | Automatic Fail Trigger |
|---|---|---|
| **Artifact Cardinality** | Emits exact files specified by `master-registry.yaml` `artifact_policy` and explicit user overrides | Unrequested companion labs on `M3`/`M4`/`M6`/`M7`/`M5`/single-file requests, or unwanted 4-language stacks |
| **Track Purpose & Deduplication** | Selected tracks provide distinct educational value; shared fixture/model explained once without cross-track copy-paste | Identical setup repeated across tracks, or PyTorch `.zero_grad()`/`.eval()` forced into JAX |
| **Walkthrough & Static Correctness** | A–G walkthrough explains inputs, invariants/laws, execution order, complete trace, interpretation, failure modes, and reconstruction; operators/types/APIs are statically sound | Missing A–G insight, wrong `*`/`@`/`**`/`^` operators, or unaddressed boundary failures |
| **Three-Attribute Integrity** | Clearly distinguishes *Origin*, *Method*, and *Verification*; includes `Source and static review only; not compiled or executed here.` | Presents predicted outputs or synthetic calculations as **Observed** or **Executed** |
| **Safety Boundaries** | Honors `security-education.md` (isolated/defensive) and `physical-lab-safety.md` (safe low-voltage/non-hazardous) | Targets real systems, evades safety guardrails, or fabricates wet-lab/bench measurements |
