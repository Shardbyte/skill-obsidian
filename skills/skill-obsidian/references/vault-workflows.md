# Vault and agent workflows

Use this reference for vault-wide work, templates, reorganization, or operation from an agent environment.

## Contents

- [Capability-first workflow](#capability-first-workflow)
- [Inspect a vault](#inspect-a-vault)
- [Create notes and templates](#create-notes-and-templates)
- [Rename, move, and reorganize](#rename-move-and-reorganize)
- [Bulk edits](#bulk-edits)
- [Plugins and portability](#plugins-and-portability)
- [Privacy and recovery](#privacy-and-recovery)

## Capability-first workflow

Separate the desired outcome from the available execution surface:

| Environment capability | Appropriate action |
| --- | --- |
| No vault or filesystem access | Return paste-ready artifacts and UI steps. |
| User-provided note excerpts only | Edit only supplied content and identify missing context. |
| Read-only vault access | Audit conventions and propose an exact patch. |
| Writable vault access | Inspect, edit narrowly, validate, and report changed paths. |
| First-party Obsidian CLI access | Prefer link-aware commands for moves, renames, properties, search, and validation. |
| Obsidian UI access | Also verify Live Preview or Reading view and current settings. |

Do not infer filesystem or UI access from labels such as ChatGPT, Codex, Claude, web, desktop, or Work. Inspect the actual tools available in the current session.

## Inspect a vault

Before editing, identify:

- The vault root and `.obsidian/` directory.
- Folder and filename conventions.
- Existing properties, aliases, tags, and date formats.
- Whether internal links use wikilinks or Markdown links.
- The configured attachment and new-note locations.
- Whether the vault is stored in a local, network, cloud-backed, or synchronized folder.
- Template folders and the core/community features they assume.
- Existing CSS snippets, themes, and note `cssclasses`.
- Version-control, sync, or backup behavior.

Limit content inspection to what the task requires. A vault may contain journals, credentials, personal records, or unrelated client material.

## Create notes and templates

Use descriptive filenames and match existing naming rules. Do not assume every note needs an H1 matching its filename; Obsidian already exposes the file title, and vault conventions vary.

For a reusable template:

1. Define which core or community templating feature will consume it.
2. Separate stable properties from values inserted at creation time.
3. Use placeholders supported by that specific feature only.
4. Test one note produced from the template.
5. Verify merged properties, internal links, and filename behavior.

Never present plugin-specific template syntax as native Obsidian syntax.

## Rename, move, and reorganize

Prefer Obsidian's own file operations when **Automatically update internal links** is relevant. External filesystem moves may leave Markdown links, embeds, plugin data, or generated indexes stale.

Use this sequence:

1. Create a separate backup or version-control checkpoint. Do not rely on sync or File Recovery as the only recovery path.
2. Inventory inbound links, embeds, aliases, and plugin references.
3. Rename or move one representative note inside Obsidian or with its first-party CLI.
4. Confirm links and embeds in Reading view.
5. Expand the change in bounded batches.
6. Search for old paths and unresolved destinations.

Do not silently change link style while reorganizing files.

## Bulk edits

For bulk property or text changes:

1. Select files using explicit criteria and show the intended scope.
2. Preserve encoding, line endings, frontmatter keys, and final newlines.
3. Avoid parsing Markdown with a broad regular expression when code blocks, comments, or nested structures matter.
4. Dry-run or preview representative diffs.
5. Write changes atomically where practical.
6. Run structural validation, inspect `git diff` when available, and open sample notes in Obsidian.

Obsidian does not provide native bulk property editing for every case. Scripts or plugins may be appropriate, but require an explicit backup and a narrow scope.

When the first-party CLI is available, use it for link-aware operations and post-change checks. When it is unavailable, direct file edits are acceptable for narrow plaintext work, but external moves can bypass automatic link updates.

## Plugins and portability

Core Obsidian behavior includes standard note editing, internal links, embeds, properties, callouts, tags, templates, and other bundled core plugins. Community plugins execute third-party code and can introduce proprietary syntax or metadata.

Before recommending a community plugin:

- Confirm that core Obsidian cannot reasonably meet the requirement.
- State what the plugin adds and which artifacts depend on it.
- Ask before installing or enabling it.
- Prefer actively maintained plugins and current documentation.
- Keep essential knowledge legible without the plugin when possible.

For portable vaults, favor standard Markdown links, plain lists, conventional YAML, and file-relative assets. Document every intentional Obsidian-only or plugin-only dependency.

## Privacy and recovery

- Do not read or disclose unrelated notes.
- Treat `.obsidian/plugins/*/data.json`, sync settings, and hidden files as potentially sensitive.
- Do not place secrets in properties, comments, templates, CSS, or examples.
- Do not overwrite `.obsidian` wholesale.
- Preserve an easy disable path for snippets, themes, and plugins.
- Inspect Obsidian's storage guidance before moving a vault between local, network, cloud-backed, and synchronized locations.
- Keep at least one independent backup outside the active vault and its synchronization path.
- Treat synchronization as replication, not backup: unwanted edits or deletions can propagate.
- Treat Obsidian File Recovery as device-local recovery help, not a complete backup. Its snapshots do not sync between devices.
- Report which independent backup or version-control checkpoint can revert the change, plus any secondary File Recovery or sync history that may help.
