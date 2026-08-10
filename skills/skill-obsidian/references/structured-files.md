# Bases and Canvas files

Use this reference to route structured Obsidian artifacts without treating them as ordinary Markdown.

## Obsidian Bases

Bases is a core plugin that creates database-like views from local notes and their properties. A base can be stored in a `.base` file or embedded in a Markdown `base` code block. Its source uses the documented Bases syntax for filters, formulas, properties, summaries, and views.

When working with a base:

1. Confirm the Bases core plugin and required view types are available.
2. Inspect the notes and property types the base is meant to query.
3. Inspect an existing `.base` file before changing its conventions.
4. Preserve unknown keys and formulas; make narrow structural edits.
5. Validate the file with a YAML-aware parser and open each affected view in Obsidian.
6. Route detailed formula, filter, view, or summary work to a dedicated Obsidian Bases skill when one is available.

Do not confuse a `.base` file with note frontmatter. Do not invent community-plugin view types or formula functions.

## Obsidian Canvas

Canvas is a core plugin. Obsidian stores boards as `.canvas` files using the open JSON Canvas format. Canvas nodes can contain text or refer to vault files, attachments, and web pages; edges connect nodes, and groups organize them.

When working with a canvas:

1. Parse the file as JSON, not Markdown.
2. Preserve existing node and edge IDs, positions, dimensions, colors, unknown fields, and ordering unless the requested change requires otherwise.
3. Use unique stable IDs for new nodes and edges.
4. Keep referenced file paths vault-relative and verify the targets exist.
5. Validate against the current JSON Canvas specification and open the board in Obsidian.
6. Route detailed node, edge, group, or layout work to a dedicated JSON Canvas skill when one is available.

Text-only Canvas cards can contain Markdown, but they are not standalone notes and do not appear in backlinks until converted to files.

## Embed structured files

Embed a Canvas from a Markdown note with ordinary Obsidian embed syntax:

```markdown
![[Architecture.canvas]]
```

For Bases, follow the current official instructions for embedding a `.base` file or a `base` code block. Verify syntax against current Help because Bases features and view types continue to evolve.
