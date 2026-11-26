# Subject Theory Blueprint: Operating Systems & Linux

## Purpose

Explain Operating Systems and Linux cleanly by separating **portable OS mechanisms**, **kernel/system interfaces**, and **Linux/distribution-specific operational commands** rather than mixing conceptual theory with distro trivia.

## Core Theory Obligations

- **Portable OS Concepts & Abstractions:**
  - *Processes & Threads:* Virtualized execution contexts, process isolation vs. thread shared-address space, context switches, PCB/TCB state, user vs. kernel mode.
  - *Memory Management:* Physical vs. virtual address spaces, pages/frames, multi-level page tables, **TLB miss vs. page fault** (a TLB miss only means the translation is uncached—lookup may succeed or fault; page faults include non-resident pages, unmapped addresses, and permission violations), replacement policies, thrashing, allocation.
  - *CPU Scheduling:* Turnaround vs. response vs. throughput, preemption, FCFS/SJF/SRTF/RR/MLFQ, starvation & priority inversion.
  - *Concurrency & Synchronization:* Race conditions, critical sections, mutexes/semaphores/condvars, deadlock conditions & prevention.
  - *Filesystems & I/O:* VFS abstractions, inodes/directories/extents, page cache, crash consistency/journaling, interrupts vs. polling vs. DMA.
- **System Interfaces vs. Linux Operational Commands:** Keep POSIX/kernel interfaces (`fork`, `exec`, `mmap`, `open`, file descriptors, signals) distinct from Linux-specific mechanisms (`cgroups`, `namespaces`, `/proc`, `systemd`) and distribution-specific package/service tools, separating **read-only inspection** commands from **state-changing** administration.
