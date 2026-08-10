---
name: skill-obsidian
description: Create, edit, organize, validate, and customize Obsidian vaults and Obsidian Flavored Markdown. Use for Obsidian notes and vault structures; Markdown syntax, properties, wikilinks, embeds, callouts, tags, tables, tasks, footnotes, math, and Mermaid; templates and knowledge-management workflows; interface settings, themes, CSS snippets, and per-note cssclasses; or troubleshooting rendering and portability across Obsidian, standard Markdown, and agent environments such as ChatGPT, Codex, and Claude.
---

# Obsidian

Produce readable plain-text artifacts that render predictably in Obsidian. Preserve the user's vault conventions and distinguish between advice, paste-ready output, and changes made on disk.

## Route the task

- Read [markdown-authoring.md](references/markdown-authoring.md) before creating or editing notes, templates, properties, links, embeds, callouts, tables, tasks, math, or Mermaid.
- Read [vault-workflows.md](references/vault-workflows.md) before reorganizing a vault, changing `.obsidian`, creating templates, renaming notes, or performing bulk edits.
- Read [css-and-interface.md](references/css-and-interface.md) before changing appearance, CSS snippets, themes, callouts, or note-specific styles.
- Read [sources.md](references/sources.md) when exact compatibility matters, behavior may have changed, or the user requests citations. Prefer the linked official documentation over remembered behavior.

Load only the references relevant to the current task.

## Establish the execution boundary

1. Determine whether the environment can access the vault filesystem.
2. If it can, locate the vault root and inspect relevant files before editing. Treat the directory containing `.obsidian/` as the vault root.
3. If it cannot, ask for only the files or excerpts needed, then return paste-ready Markdown, CSS, or precise UI steps. Never claim to have changed the vault.
4. Preserve existing naming, folder, property, tag, link, and CSS conventions unless the user asks to redesign them.
5. Ask before installing or enabling community plugins. Explain when a result depends on a plugin rather than core Obsidian.

These rules apply in ChatGPT web/Work/desktop, Codex, Claude, and other agents. Actual tool access, not the product name, determines which changes you can make.

## Author or edit a note

1. Identify the note's purpose, audience, and existing vault conventions.
2. Use standard Markdown for structure. Add Obsidian-only syntax only when it improves navigation, reuse, metadata, or presentation.
3. Put YAML properties at the first byte of the file when properties are needed. Keep values atomic; do not put rendered Markdown in properties.
4. Use wikilinks for vault-internal destinations when the vault uses them. Use Markdown links for web URLs and for portability when requested.
5. Prefer meaningful headings and natural prose over decorative callouts. Use callouts for information with a real semantic role.
6. Preserve unknown properties and deliberate syntax during edits. Do not rewrite an entire note for a small change.
7. Validate structure and inspect the rendered result when Obsidian is available.

Run the bundled checker for files created or materially rewritten:

```bash
python3 scripts/check_markdown.py path/to/note.md
```

Treat checker warnings as review prompts, not proof that Obsidian will reject the note. For vault-wide checks, pass multiple explicit paths or a shell-expanded file list only after confirming scope.

## Apply Markdown formatting discipline

- Separate paragraphs with one blank line.
- Put a blank line after headings and before a list that follows prose.
- Keep list items contiguous; do not add blank lines between simple items.
- Indent nested list content consistently with spaces.
- Continue every callout body line with `>`; represent a blank line inside a callout as `>`.
- Use fenced code blocks with a language identifier when known. Make an outer fence longer than any fence shown inside it.
- Escape `|` inside wikilinks placed in tables: `[[Note\|Label]]`.
- Avoid raw HTML when Markdown must render inside it; Obsidian intentionally does not process Markdown within HTML elements.
- Do not add YAML frontmatter, tags, aliases, or an H1 automatically when they add no value or conflict with vault conventions.

## Customize the interface

Choose the smallest mechanism that satisfies the request:

1. Use built-in settings for fonts, accent color, density, readable line length, and similar supported controls.
2. Use a community theme for broad visual changes when the user accepts that dependency.
3. Use a CSS snippet for a focused local override.
4. Use `cssclasses` to scope a snippet to selected notes.
5. Build or fork a full theme only for a coherent, maintained visual system.

Prefer Obsidian CSS variables over brittle selectors. Support both light and dark schemes, scope changes narrowly, and tell the user how to enable, disable, and recover from a snippet. Never edit Obsidian's bundled `app.css`.

## Change vault structure safely

Before moving, renaming, or bulk-editing notes:

1. Inspect link style, attachment location, excluded files, templates, and relevant `.obsidian` settings.
2. Define the exact file scope and preserve a recoverable copy or version-control checkpoint.
3. Prefer renaming or moving inside Obsidian when automatic link updates matter.
4. Apply a small representative change first.
5. Check links, embeds, properties, and rendered output before expanding the change.
6. Report files changed, assumptions made, validation performed, and any manual Obsidian steps remaining.

Do not expose secrets from plugin configuration, sync credentials, hidden files, or unrelated note content.

## Diagnose rendering problems

Check in this order:

1. Confirm the user is comparing Source mode, Live Preview, and Reading view appropriately.
2. Reduce the issue to a minimal note or snippet.
3. Check blank lines, indentation, fence length, escaped table pipes, YAML quoting, and balanced wikilinks or comments.
4. Temporarily disable the relevant CSS snippet, then the active theme, then implicated community plugins.
5. Compare against core Obsidian behavior and current official documentation.
6. Restore components one at a time and record the exact conflict.

## Deliver the result

- For direct edits, provide the changed paths and validation results.
- For chat-only work, provide complete paste-ready artifacts and exact destination paths.
- For UI instructions, use current menu names when verified and mention desktop/mobile differences.
- State any requirement for a theme, plugin, CSS reload, or Obsidian restart.
- Keep source citations near claims when the user requests sourced guidance.
