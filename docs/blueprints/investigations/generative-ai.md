# Generative AI, RAG, Agents & MLOps Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Evaluation Contract
Applies to Generative AI (LLMs, diffusion, VAEs, multimodal), RAG, AI Agents, and MLOps. Define input representation, deterministic vs. stochastic settings, trust boundaries, and evaluation metrics once. **Never fabricate API responses, model generations, or benchmark scores**—explicitly separate manually computed traces, predicted outputs, and user-supplied API responses.

## Domain-Tailored Practical Realizations (Apply Gate)
| Subdomain | First Principles / Trace | Core Component | Pipeline / API | Evaluation, Safety & Monitoring |
|---|---|---|---|---|
| **Generative AI** | Attention/sampling/denoising math trace | From-scratch module (attention, BPE, diffusion step) | Framework decoding / sampling config | Perplexity/fidelity checks, hallucination & latency bounds |
| **RAG** | Chunking, similarity & context trace | Minimal retriever + reranker pipeline | Hybrid retrieval / framework setup | Recall@k, grounding/citation checks, stale-index failures |
| **AI Agents** | State, observation & tool-call loop trace | Bounded tool-calling loop with schema checks | Multi-step workflow + memory | Tool-failure handling, prompt-injection boundaries, cost/loop guards |
| **MLOps** | Data/model lineage & lifecycle trace | Reproducible train/eval pipeline | Serving, registry & version config | Covariate/concept drift checks, rollback & monitoring alerts |

## Specialized Walkthrough & Verification
Default to **Python** unless another language is requested (never adding unsolicited Rust), distinguish hand-calculated metrics on synthetic inputs from predictions about pipeline behavior, include failure-debugging checks and 1–2 **Independent Exercises** (`> [!hint]-` / `> [!success]-`), and close with **`Source and static review only; not compiled or executed here.`**
