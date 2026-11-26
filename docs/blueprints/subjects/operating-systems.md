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
- **Beginner Progression, Visuals & Worked Traces:** Ground kernel abstractions in a concrete running-program scenario (closing hardware/ISA or memory-layout prerequisites inline), pair process states, multi-level page tables/TLBs, and filesystem layouts with verified web-sourced OS diagrams per [representations.md](../../procedures/authoring/representations.md) (never generated/Mermaid/ASCII) alongside trace tables, and walk through one complete trace (e.g., address translation, scheduling timeline, or deadlock check) before an independent diagnostic question.
