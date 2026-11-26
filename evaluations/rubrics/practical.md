# Evaluation Rubric: Practical & Lab Quality (Evaluation-Only)

*Load only during evaluation or when explicitly requested as an evaluation rubric—do not load during normal note authoring. Apply only criteria relevant to the intended artifact and resolved `artifact_plan` (for instance, strict-source notes with no supported lab are evaluated on proper omission, not missing tracks).*

| Dimension | Pass Standard (Cite Supporting Passage) | Automatic Fail Trigger |
|---|---|---|
| **Artifact Cardinality** | Emits the resolved artifacts under the master policy, explicit requests and source restrictions | Unrequested companion, duplicate implementation lab, unsolicited Rust implementation, or unrequested language stack |
| **Track Purpose & Deduplication** | Selected tracks provide distinct educational value; shared worked example/model explained once without cross-track copy-paste | Identical setup repeated across tracks, or PyTorch `.zero_grad()`/`.eval()` forced into JAX |
| **Walkthrough & Static Correctness** | Lab A–G responsibilities are evident. Focused implementation guides provide the necessary setup, trace and failure checks under their format. | Missing consequential reasoning, incorrect operators or types, or unaddressed boundary failures |
| **Three-Attribute Integrity** | Clearly distinguishes origin, method and actual verification. Uses the applicable static or analytical disclosure from the lab contract. | Presents a prediction as observed evidence or claims local execution |
| **Safety Boundaries** | Honors `security-education.md` (isolated/defensive) and `physical-lab-safety.md` (safe low-voltage/non-hazardous) | Targets real systems, evades safety guardrails, or fabricates wet-lab/bench measurements |
