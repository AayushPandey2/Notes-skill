# Generative AI, RAG, Agents & MLOps Investigation Lab Blueprint

Use this lean blueprint for Generative AI, RAG, AI Agents, and MLOps companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Applied AI Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared Task, Data & Evaluation Contract
Define input prompt/corpus/stream, representation (tokens, chunks, embeddings, tool schemas, or model versions), deterministic vs. stochastic settings, and evaluation criteria.

## Domain-Tailored Four-Track Matrix (Apply Track-Applicability Gate)

| Subdomain | Track 1 (First Principles) | Track 2 (Core Component) | Track 3 (Framework / Pipeline) | Track 4 (Evaluation, Safety & Monitoring) |
|---|---|---|---|---|
| **Generative AI** | Mathematical trace (attention/softmax/sampling) | From-scratch component (e.g., causal attention, BPE step) | Framework / API decoding & KV-cache usage | Perplexity/evals, hallucination, context/latency limits |
| **RAG** | Manual chunking, similarity & context-assembly trace | Minimal vector retrieval + scoring pipeline | Established RAG framework / hybrid retriever | Recall@k, grounding/faithfulness, chunking & stale-index failures |
| **AI Agents** | Explicit state, observation & tool-call loop trace | Simple tool-calling agent with bounded permissions | Integrated multi-step workflow + memory | Tool-failure handling, prompt-injection boundaries, loop/cost guards |
| **MLOps** | Manual data/model lifecycle & lineage trace | Reproducible training/validation pipeline | Serving, container/registry & versioning config | Data/concept drift detection, rollback & monitoring alerts |

Directly beneath each realization, include `> [!example]- Understand this implementation: mechanics, code, and trace dry run` covering **A–G**: **A** shapes, schemas, configs, boundaries; **B** mathematical/architectural/retrieval/lifecycle mechanism; **C** step-by-step execution order; **D** complete miniature numerical/token/retrieval/state dry run; **E** output quality & latency interpretation; **F** context overflow, ungrounded claims, permission leaks, silent drift; **G** core-system reconstruction.

## Verification Status

Label outputs **Expected** / **Hand-calculated** (never fabricated API responses or **Executed** benchmarks) and end with **`Source and static review only; not compiled or executed here.`**
