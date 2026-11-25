# Operating Systems & Linux Investigation Lab Blueprint

Use this lean blueprint for Operating Systems & Linux companion labs (`<note stem> - Experimental Lab.md`). The [shared lab contract](../../procedures/authoring/experimental-lab.md) governs structure, collapsed **A–G** walkthroughs, and static review.

## Required Lab Structure

### Header & Navigation
- Line-1 YAML frontmatter matching the parent note's profile.
- `# <Topic> — Operating Systems Lab`
- `> [!abstract] Parent Note & Companion Pack` linking `[[<Parent Note>]]` and `[[<Parent Note> - Cheatsheet & Interview Q&A]]`.

### Shared System Fixture & Kernel/User Boundary
Define hardware/OS parameters (page size, frame count, CPU burst table, or permissions state) and one concrete fixture.

## Four OS & Linux Tracks (Apply Track-Applicability Gate)

1. **Track 1 — Manual Mechanism Trace:** Trace the OS mechanism by hand (e.g., virtual-to-physical page table/TLB lookup, FCFS/SJF/RR Gantt timeline, inode lookup).
2. **Track 2 — Documented System / CLI Interfaces:** Show standard syscalls or Linux commands, clearly separating **read-only inspection** (`ps`, `vmstat`, `ls -l`) from **state-changing** operations.
3. **Track 3 — Educational Simulation / Program:** Implement a clean bounded simulation or POSIX/systems snippet demonstrating the mechanism.
4. **Track 4 — Failure & Concurrency Diagnosis:** Inspect fault conditions (page fault vs. TLB miss, deadlock/race interleaving, permission failure, OOM) and recovery.

Directly beneath each realization, include `> [!example]- Understand this implementation: OS state, trace, and dry run` covering **A–G**: **A** system parameters & initial state; **B** OS abstraction & invariant; **C** step-by-step transition/execution order; **D** complete concrete trace on the fixture; **E** timing/memory/isolation interpretation; **F** race conditions, thrashing, starvation, privilege errors; **G** core-mechanism reconstruction.

## Verification Status

Label outputs **Hand-calculated** / **Expected** (never **Executed** on the host) and end with **`Source and static review only; not compiled or executed here.`**
