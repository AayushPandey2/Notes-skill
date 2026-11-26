# Computer Architecture Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Model-Specific Activation
Applies to ISAs, datapaths, pipelines, caches, branch predictors, floating-point hardware, and coherence protocols. Select only the tracks matching the requested subsystem—never force CPU pipeline or ISA tracks into a focused cache-associativity lab:

| Topic | Primary Investigation Focus |
|---|---|
| **Cache mapping** | Exact byte-address decomposition (`tag \| index \| offset`), replacement policy, and hit/miss trace (e.g., 16-bit byte address `684` in a 1 KiB direct-mapped cache with 16-byte blocks and 64 lines $\to$ Tag `0` (`000000`), Index `42` (`101010`), Offset `12` (`1100`)) |
| **Pipelining** | Instruction timing, explicit pipeline model, hazards, forwarding paths, and stall cycles |
| **Instruction sets** | Instruction encoding, operand fields, addressing modes, and architectural state |
| **Branch prediction** | Predictor state transitions, accuracy trade-offs, and misprediction penalties |
| **Floating-point hardware** | IEEE 754 bit encoding, rounding modes, subnormals, `NaN`/`Inf`, and exception flags |
| **Multicore coherence** | MESI/MOESI cache states, coherence bus/directory transitions, and memory-model assumptions |

State instruction subset, explicit pipeline model (noting that a classic in-order 5-stage `IF/ID/EX/MEM/WB` pipeline generally prevents WAR/WAW register hazards under single-issue in-order writeback, whereas out-of-order or variable-latency execution introduces them), or cache geometry once up front.

## Practical Realizations
1. **Instruction-Level Trace:** Track operands, registers, program counter (`PC`), and memory/flag writes across a concrete instruction sequence.
2. **Datapath / Pipeline Investigation:** Trace control signals, pipeline stages, applicable data/control hazards (matching the stated pipeline model), forwarding paths, and stall cycles.
3. **Memory-Hierarchy Analysis:** Decode concrete byte addresses into **tag, index, and block-offset** bits and trace cache hits, misses, and eviction/replacement steps.
4. **Performance & Correctness Verification:** Derive CPI, stall overhead, AMAT, or Amdahl speedup under stated assumptions and check boundary cases (e.g., load-use hazard, conflict-miss thrashing).

## Specialized Walkthrough & Verification
Label cycles/hits/AMAT **author-derived / manual_arithmetic / statically_reviewed** (never inventing unallowed origin values, and reflecting only checks actually performed); if simulation code appears end with **`Source and static review only; not compiled or executed here.`**, otherwise **`Manual instruction, pipeline, and cache trace review only (no simulator executed).`**
