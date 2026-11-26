# Subject Theory Blueprint: Generative AI, RAG, Agents & MLOps

## Purpose

Provide dedicated theory obligations for modern generative models (autoregressive, diffusion, VAEs, multimodal), retrieval pipelines, tool-using agents, and production ML lifecycles rather than folding them into classical supervised ML.

## Subdomain Theory Obligations

- **Generative Model Families:** Cover **autoregressive LLMs** (subword tokenization/BPE effects, positional embeddings, causal attention & KV caching, decoding strategies), **diffusion models** (forward noising vs. learned reverse denoising, score/noise prediction, guidance & sampling steps), **VAEs** (encoder/decoder, latent bottleneck, ELBO reconstruction + KL trade-off), and **multimodal architectures**—evaluating each modality honestly (perplexity/likelihood vs. sample fidelity/diversity vs. task benchmarks, hallucination vs. calibration).
- **Retrieval-Augmented Generation (RAG):** Document parsing & chunking boundaries, dense vs. sparse/hybrid indexing, embedding similarity vs. cross-encoder reranking, context assembly & lost-in-the-middle effects, citation grounding, and separating retrieval failure from generation failure.
- **AI Agents:** State loops (observe $\to$ plan $\to$ act), tool schemas & parameter validation, permission/trust boundaries, short- vs. long-term memory, prompt injection & confused-deputy risks, stopping criteria, latency/cost bounds, and failure recovery.
- **MLOps:** End-to-end data/feature/model lineage, experiment tracking & reproducibility, artifact versioning, serving patterns (batch vs. online, latency/throughput), shadow/canary rollouts, data/concept drift monitoring, and rollback criteria.
- **Beginner Progression, Visuals & Practice:** Build intuition from a concrete single-step example (next-token distribution, one denoising step, or one retrieved chunk) while closing probability/transformer prerequisites inline, pair multi-stage architectures and pipelines with verified web-sourced diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII), and walk through one concrete failure/debugging trace before an independent design prompt.
