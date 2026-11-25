# Subject Theory Blueprint: Generative AI, RAG, Agents & MLOps

## Purpose

Provide dedicated theory obligations for modern LLM/generative systems, retrieval pipelines, tool-using agents, and production ML lifecycles rather than folding them into classical supervised ML.

## Subdomain Theory Obligations

- **Generative AI & LLMs:** Subword tokenization (BPE/byte-level effects on arithmetic/multilingual text), token & positional embeddings, causal self-attention & KV caching, pretraining vs. instruction/preference tuning, decoding strategies (greedy, temperature, top-k/top-p), context-window trade-offs, hallucination vs. calibration, and evaluation limits.
- **Retrieval-Augmented Generation (RAG):** Document parsing & chunking boundaries, dense vs. sparse/hybrid indexing, embedding similarity vs. reranking, context assembly & lost-in-the-middle effects, citation grounding, and separating retrieval failure from generation failure.
- **AI Agents:** State loops (observe → plan → act), tool schemas & parameter validation, permission/trust boundaries, short- vs. long-term memory, prompt injection & confused-deputy risks, stopping criteria, latency/cost bounds, and failure recovery.
- **MLOps:** End-to-end data/feature/model lineage, experiment tracking & reproducibility, artifact versioning, serving patterns (batch vs. online, latency/throughput), shadow/canary rollouts, data/concept drift monitoring, and rollback criteria.
