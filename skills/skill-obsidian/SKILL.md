---
name: skill-obsidian
description: Create, validate, organize, automate, and customize Obsidian vaults. Use for Obsidian Markdown, properties, links, embeds, templates, search, CLI and URI workflows, Bases (.base), Canvas (.canvas), CSS snippets, themes, vault migrations, backup-aware bulk edits, or rendering and portability problems. Do not use for generic Markdown work with no Obsidian context.
---

# Obsidian

Produce readable plain-text artifacts that render predictably in Obsidian. Preserve the vault's conventions and distinguish between advice, paste-ready output, and changes actually made.

## Route the task

- Read [markdown-authoring.md](references/markdown-authoring.md) before creating or editing notes, properties, links, embeds, callouts, tables, tasks, math, or Mermaid.
- Read [vault-workflows.md](references/vault-workflows.md) before reorganizing a vault, changing `.obsidian`, creating templates, moving attachments, or performing bulk edits.
- Read [automation.md](references/automation.md) before using the Obsidian CLI, Obsidian URI, Search, or automated link and property operations.
- Read [structured-files.md](references/structured-files.md) before creating or editing Bases (`.base`) or Canvas (`.canvas`) files.
- Read [css-and-interface.md](references/css-and-interface.md) before changing appearance, CSS snippets, themes, callouts, or note-specific styles.
- Read [platform-compatibility.md](references/platform-compatibility.md) when packaging, installing, or explaining support across ChatGPT, Codex, Claude, and other Agent Skills hosts.
- Read [sources.md](references/sources.md) when behavior may have changed, exact compatibility matters, or citations are requested. Prefer linked first-party documentation over remembered behavior.

Load only the references relevant to the task.

## Establish the execution boundary

1. Determine whether the environment can access the vault filesystem, run commands, or operate the Obsidian UI.
2. If filesystem access exists, locate the vault root and inspect only relevant files. Treat the directory containing `.obsidian/` as the root.
3. If command execution exists, probe `obsidian help` before assuming the first-party CLI is installed and enabled.
4. If only supplied content is available, return paste-ready Markdown, CSS, or exact UI steps. Never claim to have changed or rendered the vault.
5. Preserve naming, folders, properties, tags, link style, attachment policy, and CSS conventions unless asked to redesign them.
6. Ask before installing or enabling community plugins. Identify every result that depends on a plugin rather than core Obsidian.

Capabilities determine available actions; product labels do not.

## Author or edit a note

1. Identify the note's purpose and inspect nearby notes for established conventions.
2. Use standard Markdown for structure. Add Obsidian-only syntax only when it improves navigation, reuse, metadata, or presentation.
3. Put YAML properties at the first byte when needed. Preserve unknown keys and types; do not put rendered Markdown in properties.
4. Match the vault's internal-link style. Use ordinary Markdown links for web URLs and where portability is required.
5. Prefer meaningful headings and natural prose over decorative callouts.
6. Make the smallest coherent edit. Do not rewrite an entire note for a local correction.
7. Validate structure, link targets, attachments, and rendered output to the extent the environment allows.

Run the bundled structural/style checker for created or materially rewritten notes. Resolve the script relative to this `SKILL.md`; do not assume the current directory is the skill directory:

```bash
python3 /absolute/path/to/skill-obsidian/scripts/check_markdown_style.py path/to/note.md
```

The checker accepts files or directories and supports `--format json` and `--errors-only`. It requires PyYAML; install dependencies from the adjacent `scripts/requirements.txt` if the host does not provide them. Its findings are review prompts, not proof of Obsidian rendering correctness.

## Apply Markdown formatting discipline

- Separate paragraphs with one blank line.
- Put a blank line after headings and before a list that follows prose.
- Keep simple list items contiguous and indent nested content consistently with spaces.
- Continue every callout body line with `>`; represent an internal blank line as `>`.
- Use fenced code blocks with a language identifier when known. Make an outer fence longer than any fence shown inside it.
- Escape `|` inside wikilinks placed in tables: `[[Note\|Label]]`.
- Avoid raw HTML when Markdown must render inside it; Obsidian does not process Markdown inside HTML elements.
- Do not add frontmatter, tags, aliases, or a duplicate H1 automatically.

## Automate with the smallest reliable surface

1. Prefer the first-party CLI for link-aware vault operations when it is available.
2. Target the vault explicitly and use an exact `path=` when duplicate filenames are possible.
3. Use direct file edits for narrow plaintext changes when CLI support is unavailable or offers no advantage.
4. Use Obsidian URI for cross-application open, create, search, and callback flows; percent-encode user-controlled values.
5. Preview scope and establish a real backup or version-control checkpoint before destructive or bulk changes.
6. Validate with CLI link/property commands, the bundled checker, diff inspection, and representative rendering as available.

## Customize the interface

Choose the smallest mechanism that meets the request:

1. Built-in settings for supported appearance controls.
2. A community theme for broad visual changes when that dependency is acceptable.
3. A narrowly scoped CSS snippet for a focused override.
4. `cssclasses` for note-specific styling.
5. A full theme only for a maintained visual system.

Prefer Obsidian CSS variables over brittle selectors. Support light and dark schemes, keyboard focus, readable contrast, narrow panes, and mobile where relevant. Tell the user how to enable, disable, and recover from a snippet. Never edit bundled `app.css`.

## Change vault structure safely

Before moving, renaming, or bulk-editing notes:

1. Inspect link style, attachment location, excluded files, templates, storage layout, and relevant `.obsidian` settings.
2. Define the exact scope and create a separate backup or version-control checkpoint. Sync and File Recovery are not substitutes for a full backup.
3. Prefer Obsidian or its CLI when automatic link updates matter.
4. Apply one representative change first.
5. Check inbound links, embeds, properties, attachments, and rendered output before expanding.
6. Report files changed, assumptions, validation, and remaining manual steps.

Do not expose secrets from plugin configuration, sync credentials, hidden files, or unrelated notes.

## Diagnose rendering problems

1. Confirm whether the issue occurs in Source mode, Live Preview, Reading view, or more than one.
2. Reduce it to a minimal note or snippet.
3. Check blank lines, indentation, fence length, escaped table pipes, YAML quoting, and balanced links and comments.
4. Disable the relevant snippet, then the theme, then implicated community plugins.
5. Compare with core behavior and current official documentation.
6. Restore components one at a time and record the conflict.

## Deliver the result

- For direct edits, give changed paths and validation results.
- For chat-only work, give complete paste-ready artifacts and exact destination paths.
- For UI instructions, use verified current menu names and note desktop/mobile differences.
- State any theme, plugin, CSS reload, Obsidian restart, or CLI-version requirement.
- Keep citations near sourced claims when citations are requested.
