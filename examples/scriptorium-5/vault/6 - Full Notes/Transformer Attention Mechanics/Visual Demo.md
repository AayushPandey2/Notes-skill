# Transformer Attention Mechanics — prepared visual demonstration

These are actual prepared representations. The associated adaptive chapter plan remains planned; no complete teaching collection or semantic review is claimed.

## Query Key and Value Projections

One-head attention interfaces

| component | input | output | operation |
| --- | --- | --- | --- |
| Score product | Q: B,T_q,d_k; K: B,T_k,d_k | B,T_q,T_k | Q times transpose(K) / sqrt(d_k) |
| Weighted values | A: B,T_q,T_k; V: B,T_k,d_v | B,T_q,d_v | A times V |

Symbols specify dimensions, not observed tensors.

T_q and T_k may differ in cross-attention; the contraction requires matching d_k.



## Value Aggregation

![[assets/scriptorium/79b4e954dc8b729c3e3316af3767a6b1fdf8e5e958a5e7a314ebb2e21e0e07b8.svg]]

This schematic specifies interfaces; it does not claim a model forward pass was executed.
