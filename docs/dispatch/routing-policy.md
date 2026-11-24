# Routing policy

Load when a request names multiple products or its intended format is unclear. The [master registry](master-registry.yaml) maps the seven products to real files; it does not install commands or run software.

1. Respect the user's explicit command and source limits. A source-only request uses `R-S0` and never browses outside supplied material. `R-S1` permits targeted external verification only when the user permits source-first verification. An output choice never loosens a source restriction.
2. Honor an explicit requested product such as “formula sheet” or “worked solutions.” Ignore a negated product phrase such as “don't make a cheat sheet.” Otherwise choose the dominant learning objective via [router.md](../../router.md).
3. A bare topic defaults to M1. Supplied lectures or chapters requested in order use M2. A paper analysis or comparison uses M7. A video request uses M2 unless the user requests a different product.
4. Keep a small summary inside the primary note when it supports that note. For two independently requested artifacts, route each separately and share the same verified facts and notation.

The installed public skill folders are `/scribe-notes`, `/scribe-ytnotes`, `/scribe-doubt`, `/scribe-quiz`, and `/scribe-setfolder`. Old note-command names may be explained as migrated requests; do not claim they are installed commands. If a selected template is missing, state that gap rather than inventing a registry entry.
