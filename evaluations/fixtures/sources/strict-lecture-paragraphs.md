# Evaluation Fixture (Source): Strict-Source Two-Paragraph Lecture Excerpt

*Controlled evaluation source fixture for Eval Case 40 (`artifact_plan` source-constraint precedence).*

> **Paragraph 1 (Hashing Overview):** A hash table maps keys from a large universe $U$ into an array of $m$ buckets using a hash function $h: U \to \{0, \dots, m-1\}$. Because $|U| > m$ by the pigeonhole principle, distinct keys can collide ($h(k_1) = h(k_2)$ for $k_1 \neq k_2$). Under separate chaining, each bucket stores a linked list of all keys hashing to that index, making expected lookup time $O(1 + \alpha)$ under uniform hashing where load factor $\alpha = n/m$.

> **Paragraph 2 (Scope Boundary):** Good hash functions aim to distribute keys evenly across buckets regardless of patterns in the input keys. In security-sensitive contexts where adversaries craft colliding keys, randomized seeded hashing prevents worst-case $O(n)$ bucket degeneration. *(End of supplied lecture material; no lab exercises, implementation code, or practice problems are included.)*
