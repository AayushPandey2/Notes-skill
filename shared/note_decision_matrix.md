# Note decision index

Resolve these 15 routing decisions; load only the linked detailed branch when needed. This index owns command-level routing; [detailed matrices](notes_decision_matrix.md) retain their stable DM IDs and decision record. Formatting lives only in [authoring rules](authoring_rules.md).

| ID | Decision | Condition ? action | Detail |
|---|---|---|---|
| D01 | Command and route | Deep research ? deepstudy-master; source-faithful study ? studynotes; coding/general filenames are aliases; other explicit formats keep their route. | [DM-01](notes_decision_matrix.md#dm-01) |
| D02 | Scope | One mechanism ? atomic scope; alternatives ? family; breadth ? survey; navigation ? map. | [DM-01](notes_decision_matrix.md#dm-01) |
| D03 | Reader | Missing essential foundation ? explain; familiar ? refresh; advanced ? link conventions. | [DM-02](notes_decision_matrix.md#dm-02) |
| D04 | Outcome and track | Record observable outcome and conceptual/mathematical/algorithmic/systems/applied/hybrid track separately. | [DM-03](notes_decision_matrix.md#dm-03) |
| D05 | Research | Stable supplied support ? no new search; authority/API/conflict ? authoritative/current/deeper source check. | [DM-05](notes_decision_matrix.md#dm-05) |
| D06 | Math inclusion | Defines, predicts, quantifies or changes a decision ? include; otherwise omit. | [DM-06](notes_decision_matrix.md#dm-06) |
| D07 | Math depth | Structural/operational/derivational/proof ? 0/1/2/3 for deep study; other routes use 0/1/2. | [DM-07](notes_decision_matrix.md#dm-07) |
| D08 | Calculus | Forward prediction ? none; update intuition/scalar derivative/chain rule/gradient debugging ? matching depth. | [DM-08](notes_decision_matrix.md#dm-08) |
| D09 | Equation treatment | Define symbols and conditions at first use; expand non-obvious transformations only. | [DM-09](notes_decision_matrix.md#dm-09) |
| D10 | Fixture and topology | Choose small discriminating values; follow actual states, recurrence, components or data flow. | [DM-11](notes_decision_matrix.md#dm-11) |
| D11 | Visual modality | Flow/state/grid/tree/timeline/comparison ? matching visual; spatial/geometry ? ASCII/Unicode diagram (never Mermaid flowchart); direct explanation sufficient ? none. | [DM-13](notes_decision_matrix.md#dm-13) |
| D12 | Code purpose and tool | Non-computing subjects ? `none` (enforced by `scripts/decision_matrix.py`); computing subjects ? select language by observable teaching goal; no purpose ? no code. | [DM-14](notes_decision_matrix.md#dm-14) |
| D13 | Verification | Executable claim ? actual status and relevant checks; numerical check never substitutes for proof. | [DM-18](notes_decision_matrix.md#dm-18) |
| D14 | Optional modules | Include only a declared template module whose activation condition holds; omit heading otherwise. | [DM-19](notes_decision_matrix.md#dm-19) |
| D15 | Final audit | Check outcome, source support, links, residue, numbering and duplication; then validate. | [DM-20](notes_decision_matrix.md#dm-20) |

## Template registry

Canonical deep study: [deepstudy-master.md](../templates/deepstudy-master.md). Structured source study: [studynotes.md](../templates/studynotes.md). Other routes use their exact filename in the template directory. Optional module IDs are declared in template comments; automation reads those declarations rather than maintaining a second registry.
