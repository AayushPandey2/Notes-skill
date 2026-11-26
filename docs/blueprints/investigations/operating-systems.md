# Operating Systems & Linux Investigation Profile

Inherits shared structure, YAML, navigation, shared-foundation A–G deduplication, and 3-attribute integrity rules from [experimental-lab.md](../../procedures/authoring/experimental-lab.md).

## Applicability & Shared System Fixture
Applies to OS kernel mechanisms, concurrency, memory/filesystems, and Linux administration. Explicitly separate **portable OS mechanisms**, **Linux-specific behavior** (`/proc`, namespaces, cgroups, `systemd`), and **distribution-specific commands**. Define system parameters (page size, frames, CPU bursts, permissions) once.

## Practical Realizations
1. **Manual Mechanism Trace:** Hand-trace virtual-to-physical translation (TLB lookup vs. page-table walk vs. page/permission fault), CPU scheduling timelines, or inode resolution.
2. **Documented System / CLI Interfaces:** Standard POSIX syscalls or Linux tools, clearly separating **read-only inspection** from **state-changing** commands.
3. **Educational Simulation / Systems Snippet:** Bounded simulation or POSIX snippet demonstrating the mechanism.
4. **Fault & Concurrency Diagnosis:** Inspect thrashing, deadlock/race interleavings, permission denials, or OOM behavior.

## Specialized Walkthrough & Verification
Distinguish portable theory from OS/distro-specific behavior and apply the shared 3-attribute integrity rules from `experimental-lab.md` to all traces (recording actual origin, `manual_arithmetic` or `analytical` method, and verification status actually performed). For non-code labs, end with **`Manual kernel and scheduling trace review only (no commands or code executed).`**
