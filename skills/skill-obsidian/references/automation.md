# Automation, CLI, URI, search, and templates

Use this reference when an agent can run commands, when a workflow crosses application boundaries, or when a task depends on Obsidian's link and property awareness.

## Choose an execution surface

| Need | Preferred surface |
| --- | --- |
| Link-aware create, move, rename, query, or validation | First-party Obsidian CLI |
| Narrow plaintext edit with no Obsidian-side behavior | Direct filesystem edit |
| Open, create, or search from another application | Obsidian URI |
| Visual rendering or setting confirmation | Obsidian UI |

Do not assume a desktop agent can operate the UI or that a web agent can access local files. Confirm capabilities first.

## Probe and target the CLI

The first-party CLI requires a current Obsidian 1.12 installer; the reviewed documentation specifies installer version 1.12.7 or later. The user must enable **Settings → General → Command line interface** and complete registration. A command requires the desktop app; it launches Obsidian if needed.

Probe before relying on it:

```bash
obsidian help
obsidian version
```

If the command is missing, explain how to enable it or use direct file operations. Do not silently substitute an unrelated third-party `obsidian` package.

Target a vault before the command. Use the vault name or ID:

```bash
obsidian vault="Work Notes" search query="status:open"
```

When filenames may repeat, prefer an exact root-relative `path=` over link-style `file=` resolution:

```bash
obsidian vault="Work Notes" read path="Projects/Atlas/Plan.md"
```

Quote values that contain spaces. Check command-specific parameters with `obsidian help <command>` because the CLI evolves.

## Use link-aware commands

The CLI covers note creation and reading; append and prepend; move and rename; links and unresolved links; properties; search; templates; Bases; history; themes and snippets; and developer inspection. Prefer it when Obsidian-side behavior matters.

For moves and renames, first confirm **Automatically update internal links**. The CLI follows that setting:

```bash
obsidian vault="Work Notes" move path="Drafts/Plan.md" to="Projects/Atlas/Plan.md"
obsidian vault="Work Notes" unresolved
```

Before overwriting or deleting anything:

1. Read the targeted file and verify the exact path.
2. Establish a separate backup or version-control checkpoint.
3. Inspect `obsidian help <command>` for overwrite, trash, or permanent-delete behavior.
4. Preview or test one representative operation.
5. Re-run unresolved-link, property, and content checks afterward.

Use developer commands such as `dev:screenshot`, inspection, or reload only when UI validation is in scope. Do not run arbitrary JavaScript through `eval` unless the task requires it and the code has been reviewed.

## Use Obsidian URI safely

Obsidian URI supports `open`, `new`, `daily`, `unique`, `search`, and `choose-vault` actions. Percent-encode every parameter value, including `/`, `#`, spaces, `&`, and user-provided text.

```text
obsidian://open?vault=Work%20Notes&file=Projects%2FAtlas%2FPlan
obsidian://search?vault=Work%20Notes&query=tag%3Aproject
obsidian://new?vault=Work%20Notes&file=Inbox%2FCapture.md&content=%23%20Capture
```

Use `vault` plus `file` for a vault-relative destination. An absolute URI `path` overrides them and can reveal local filesystem structure, so avoid exposing it unnecessarily. Treat `overwrite`, `append`, callback URLs, and clipboard content as state-changing or sensitive inputs.

## Search before changing structure

Use core Search or `obsidian search` to find names, paths, tags, properties, links, and content before broad edits. Confirm exact current search operators in official Help when composing complex queries. Do not treat a textual match as proof of a resolved internal link; use link-aware CLI commands or Obsidian's unresolved-links view when available.

## Create templates deliberately

The core Templates plugin supports `{{title}}`, `{{date}}`, and `{{time}}`; date and time accept format strings. Other placeholder languages usually belong to community plugins.

```markdown
---
created: "{{date}}"
---

# {{title}}
```

Before generating from a template:

1. Identify the core or community feature that consumes it.
2. Verify that feature's placeholder syntax.
3. Confirm the template folder and new-note destination.
4. Create one representative note and inspect merged properties and links.

## Handle attachments

Inspect **Files and links → Default location for new attachments** and existing relative paths before adding or moving media. Preserve attachment filenames and paths referenced by embeds. Use Obsidian for moves when automatic link updates matter, and check every affected embed afterward.
