# Reflection Footer Contract

## Purpose & Activation Trigger

Append a lightweight Dataview reflection and vault-navigation footer at the end of compact/source-study notes (`M2`, `M3`, `M4`, `M5`, `M7`) when vault tracking widgets are enabled (respecting route word caps; deep-study notes select reflection blocks dynamically via [adaptive-engine.md](../references/workflows/notes-creation/adaptive-engine.md)). Omit genuine empty `Confusion` fields cleanly. Requires Obsidian Dataview JS enabled for the button.

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
