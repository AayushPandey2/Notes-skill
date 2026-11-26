# Subject Theory Blueprint: Computer Architecture

## Purpose

Teach Computer Architecture through **instruction semantics, datapath/control execution, pipelining/hazards, and memory-hierarchy trade-offs**.

## Core Theory Obligations

1. **ISA & Data Representation:** Instruction formats, addressing modes, two's complement/IEEE-754 bit representations, endianness, and ABI calling conventions.
2. **Datapath, Control & Pipelining:** Single-cycle vs. pipelined execution (qualifying the classic 5-stage `IF/ID/EX/MEM/WB` pipeline as a common **educational model**, not a universal CPU design), structural/data/control hazards, forwarding vs. stalling, branch prediction, and CPI/speedup (Amdahl's law).
3. **Memory Hierarchy & Parallelism:** Temporal/spatial locality, cache geometry (direct-mapped, set-associative, tag/index/offset fields), hit/miss/write policies, virtual-to-physical translation, SIMD/SMT/multicore coherence (MESI).
4. **Beginner Progression, Visuals & Worked Traces:** Motivate hardware structures with a concrete instruction-execution scenario (closing binary arithmetic/logic prerequisites inline), pair datapath/pipeline/cache concepts with verified web-sourced architecture diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) alongside cycle/address tables, and work one concrete numerical trace (e.g., tag/index/offset split or CPI stalls) before an independent exercise.
