# Pre-generation routing

**Pass 1: resolve intent and input.** Parse explicit commands, template requests, source links, language, requested depth, and available cheap source metadata.

**Pass 2: classify each planned note.** Use a short topic outline and available vault context to choose a template, math depth, implementation stack, evidence profile, and destination for every output. A broad topic can produce a mixed plan; a narrow request can produce one note.

Evaluate these signals independently:

| Signal | Question | Routing effect |
| --- | --- | --- |
| Input type | Is this an explicit command, selected template, standalone source, or study topic? | Locks or constrains the route |
| Implementation weight | Does mastery require implementing a mechanism, tracing code, or using an API? | Favors DeepStudy-Coding or API-Table |
| Structural density | Is this one cohesive mechanism, an API catalog, or independently useful concepts? | Keeps one deep note, selects API-Table, or proposes bounded Atomic notes |
| Math requirement | Is notation unnecessary, needed for application, or needed to explain why? | Selects math level 0, 1, or 2 |

### 3.2 Apply this precedence

1. **Explicit commands lock the route.** `/scribe-dsa <language> <problem>` selects DSA. `/scribe-practice <topic-or-note>` selects Practice. URLs inside the payload supply source material without overriding that route. Give useful usage for malformed commands.
2. **Explicit template intent comes next.** Honor an explicit supported template when no command has locked the route. If the command and request conflict in a way that prevents a useful result, identify the conflict rather than silently switching modes.
3. **Standalone source ingestion follows.** An article or YouTube link selects Summary. An identifiable research-paper link, including arXiv abstract/PDF links, selects Paper-Breakdown unless the user explicitly requests Summary. A link provided as a reference for a broader topic does not force every generated note into a source-summary route.
4. **Otherwise route by the note's purpose.** Revision selects Cheat-Sheet; a choice between alternatives selects Comparison; lookup selects API-Table; one self-contained idea selects Atomic; implementation-centered understanding selects DeepStudy-Coding; conceptual understanding selects DeepStudy-General.
5. **Use density as a signal, not a rigid threshold.** Around ten distinct API entries suggests API-Table, but a focused parameter reference such as `nn.Conv2d` qualifies with fewer. Split non-API material only when the resulting concepts stand on their own. Do not fragment one mechanism merely because it has several steps.
6. **Resolve math separately.** A conceptual note can require a proof; a coding note can require no math. A paper is not automatically mathematical. Practice questions can have different math requirements within one set.
7. **Resolve language from explicit user intent first**, then subject and established vault convention. Follow the domain matrix below when no stronger preference applies.

### 3.3 Define the math levels

| Level | Use when | Required treatment |
| --- | --- | --- |
| `0` | Notation does not materially improve understanding | Plain-language mechanism, examples, evidence, or logical reasoning; no ornamental math |
| `1` | A formula is needed for correct use | Intuition, assumptions, complete symbol key, formula, worked substitution, and relevant edge cases |
| `2` | Understanding why depends on derivation or proof | Everything in level 1 plus a justified step-by-step derivation, applicable interpretation, counterexample, and domain-aware boundary analysis |

The route controls the **size and placement** of the math treatment. If an Atomic note or Cheat-Sheet needs a long level-2 derivation, keep the compact result and validity conditions there and reference an existing or planned deep-study note for the derivation. Do not violate the compact template's purpose to embed a full textbook chapter.

### 3.4 Use this domain-to-language matrix

| Domain | First-principles or reference stack | Idiomatic or ecosystem stack |
| --- | --- | --- |
| ML / deep learning | Python + NumPy | scikit-learn for classical ML; PyTorch for tensor/autodiff topics |
| DSA | User-selected language; default C++20 for performance-oriented study | Standard facilities in that language; Python 3 as a useful additional reference only when warranted |
| Systems / OS / concurrency | C17 or Rust, selected by the topic and user preference | Appropriate safe abstraction or real OS/library API; Python harness/simulation when useful |
| Databases / data engineering | SQL with an identified PostgreSQL or DuckDB version/dialect | SQL workflow or Python with pandas/polars when that comparison teaches something |
| Web / distributed systems / APIs | TypeScript/Node.js or Go | Idiomatic framework/client/API usage; Python only when useful |
| Pure math / logic | Reproducible derivation, proof, or counterexample | Optional SymPy/NumPy check when it adds evidence |
| Non-code conceptual subjects | Worked evidence or reasoning | No compulsory code implementation |

Do not generate unsafe manual memory management solely to make a first-principles tier look more advanced. Choose the smallest faithful implementation that exposes the actual mechanism. Respect an explicitly requested supported language even when the table suggests another default.

### 3.5 Keep a compact internal generation plan

Adapt this illustrative representation to existing project conventions:

```yaml
title: Convolution Operation & Kernels
template: deepstudy-coding
math_level: 2
language: python
verification_stacks:
  - numpy
  - pytorch
source_profile: official-docs-and-primary-paper
running_example: Small image with one filter
routing_reason: Mastery requires tracing the operation and verifying its output.
output_path: 01 - Convolution Operation & Kernels.md
practice_policy: include-in-topic-set
```

The fields above are planning metadata, not mandatory public frontmatter. Follow the repository's existing metadata contract. Do not expose routing diagnostics throughout the note body.

Check destinations and path uniqueness before writing. Resolve filenames using the existing vault conventions and filesystem rules. Never replace an existing user note merely because a plan entry has the same title.

### 3.6 Support mixed topics

For a CNN study request, a suitable result is:

| Path relative to the topic folder | Route | Math level |
| --- | --- | --- |
| `01 - Convolution Operation & Kernels.md` | DeepStudy-Coding | 2 |
| `02 - History of LeNet to ResNet.md` | DeepStudy-General | 0 |
| `03 - PyTorch nn.Conv2d Parameters.md` | API-Table | 0, or 1 for output-size arithmetic |
| `Practice Set/CNN - Practice Test.md` | Practice | Per question |

Use existing naming style when it differs from these examples. A topic folder does not have to share one route or one math level.
