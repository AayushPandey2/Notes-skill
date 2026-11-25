# Subject Theory Blueprint: Operating Systems & Linux

## Purpose

Explain OS kernels and Linux systems through **abstractions, isolation boundaries, hardware-software interfaces, and resource trade-offs** rather than treating them as command trivia.

## Core Theory Obligations

- **Processes & Threads:** Virtualized execution contexts, process isolation vs. thread shared-address space, context switches, PCB/TCB state, user vs. kernel mode.
- **Memory Management:** Physical vs. virtual address spaces, pages/frames, multi-level page tables, TLB hits/misses vs. page faults, replacement policies, thrashing, allocation & fragmentation.
- **CPU Scheduling:** Turnaround vs. response vs. throughput trade-offs, preemption, FCFS/SJF/SRTF/RR/MLFQ, starvation & priority inversion.
- **Concurrency & Synchronization:** Race conditions, critical sections, mutual exclusion, locks/semaphores/condition variables, deadlock conditions & prevention.
- **Filesystems & I/O:** VFS abstractions, inodes/directories/extents, caching/buffering, crash consistency/journaling, interrupts vs. polling vs. DMA.
- **System Calls & Linux Administration:** Trap/syscall user-kernel boundary, file descriptors, permissions/ownership, signals, services/systemd, and clearly separating **read-only inspection** commands from **state-changing** commands.
