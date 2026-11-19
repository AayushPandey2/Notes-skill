# Reflection footer

Non-deep routed scaffolds use the following reflection block; deep-study reflection is selected by D15. See [authoring rules](authoring_rules.md#rendering). Fill the reflection in the last section. For compact notes keep each entry brief and within the route's word cap. In practice use the Confusion field as the diagnostic review hook. Obsidian requires Dataview JavaScript queries enabled for the button to execute.

<!-- scaffold:footer -->
### Metacognitive Reflection & Vault Integration

- **What I learned**: <!-- scaffold: State the change in understanding in 2–3 sentences. -->
- **Open Confusion**:
**Confusion** :: <!-- scaffold: State one specific unresolved boundary question. -->
- **Atomize**: <!-- scaffold: Name 1–3 granular ideas as existing links or pending text. -->
- **Connection**: <!-- scaffold: Add resolved links and bridge to the next subtopic. -->

```dataviewjs
const btn = dv.container.createEl("button", { text: "Mark Revisited" });
btn.onclick = async () => {
    const path = dv.current()?.file?.path;
    const file = path && app.vault.getAbstractFileByPath(path);
    if (!file) return;
    const today = window.moment().format("YYYY-MM-DD");
    const content = await app.vault.read(file);
    await app.vault.modify(file, content + "\n**Revisited** :: " + today + "\n");
    new Notice("Revisit logged for " + file.name + " — " + today);
};
```
