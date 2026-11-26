# Computer Architecture Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared Hardware Fixture
Applies to ISAs, datapaths, pipelines, caches, and hardware performance. Define instruction subset, pipeline model (explicitly qualifying educational 5-stage `IF/ID/EX/MEM/WB` assumptions), or cache geometry (size, block size, associativity, address width) once—never import irrelevant Linux administration commands.

## Practical Realizations
1. **Instruction-Level Trace:** Track operands, registers, program counter (`PC`), flags/memory writes across a concrete instruction sequence.
2. **Datapath / Pipeline Investigation:** Trace control signals, pipeline stages, RAW/WAR/WAW or control hazards, forwarding paths, and stall cycles.
3. **Memory-Hierarchy Analysis:** Decode concrete byte addresses into **tag, index, and block-offset** bits and trace cache hits, misses, and eviction/replacement steps.
4. **Performance & Correctness Verification:** Derive CPI, stall overhead, AMAT, or Amdahl speedup under stated assumptions and check boundary cases (e.g., load-use hazard, conflict miss thrashing).

## Specialized Walkthrough & Verification
Label cycles/hits/AMAT **analytical / manual_arithmetic / statically_reviewed**; if simulation code appears end with **`Source and static review only; not compiled or executed here.`** otherwise **`Manual instruction, pipeline, and cache trace review only (no simulator executed).`**
