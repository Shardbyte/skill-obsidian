# Authoritative sources

Use these sources to verify behavior that may have changed. This list records sources reviewed on 2026-08-10. Follow official sub-pages from the landing pages for the current canonical location.

## Markdown foundations

- [Markdown project](https://daringfireball.net/projects/markdown/): original Markdown design goals and project overview.
- [Markdown syntax](https://daringfireball.net/projects/markdown/syntax): original block and span syntax.
- [CommonMark](https://commonmark.org/): specification used by Obsidian.
- [GitHub Flavored Markdown](https://github.github.com/gfm/): tables, task lists, strikethrough, and other GFM behavior used by Obsidian.

## Obsidian notes and metadata

- [Obsidian Help](https://obsidian.md/help/): official help landing page and navigation.
- [Basic formatting syntax](https://help.obsidian.md/syntax): paragraphs, line breaks, headings, links, lists, tasks, code, footnotes, and comments.
- [Advanced formatting syntax](https://help.obsidian.md/advanced-syntax): tables, Mermaid, and MathJax.
- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown): supported Markdown flavors and Obsidian extensions.
- [Internal links](https://help.obsidian.md/links): wikilinks, Markdown internal links, headings, blocks, and aliases.
- [Embed files](https://help.obsidian.md/embeds): note, image, audio, PDF, Canvas, list, and search embeds.
- [Properties](https://help.obsidian.md/properties): property types, YAML storage, reserved properties, and limitations.
- [Callouts](https://help.obsidian.md/callouts): types, titles, folding, nesting, and custom CSS.
- [Tags](https://help.obsidian.md/tags): inline and property tags, nesting, and valid characters.
- [Search](https://help.obsidian.md/plugins/search): core search terms, operators, properties, and embedded queries.
- [Templates](https://help.obsidian.md/plugins/templates): core template folder and supported variables.
- [Attachments](https://help.obsidian.md/attachments): attachment storage, links, default locations, and file handling.

## Automation and structured artifacts

- [Obsidian CLI](https://help.obsidian.md/cli): installation requirements, targeting, commands, scripting, validation, and developer tools.
- [Obsidian URI](https://help.obsidian.md/uri): cross-application actions, parameters, percent-encoding, and callbacks.
- [Bases](https://help.obsidian.md/bases): core database-like views, `.base` files, embedded bases, and view types.
- [Bases syntax](https://help.obsidian.md/bases/syntax): current filters, formulas, properties, summaries, and views.
- [Canvas](https://help.obsidian.md/plugins/canvas): core visual boards and `.canvas` files.
- [JSON Canvas](https://jsoncanvas.org/): open file format used by Obsidian Canvas.

## Storage, backup, and recovery

- [How Obsidian stores data](https://help.obsidian.md/data-storage): local vault storage and configuration data.
- [Back up your Obsidian files](https://help.obsidian.md/backup): independent backups and why synchronization is not backup.
- [File Recovery](https://help.obsidian.md/plugins/file-recovery): device-local snapshots, retention, review, and recovery limitations.

## Interface and extensions

- [CSS snippets](https://help.obsidian.md/snippets): desktop/mobile installation, reload behavior, CSS variables, and `cssclasses`.
- [Themes](https://help.obsidian.md/themes): browsing, installing, updating, and removing themes.
- [Core plugins](https://help.obsidian.md/plugins): officially bundled capabilities.
- [Community plugins](https://help.obsidian.md/community-plugins): installation, enabling, updating, and removal.
- [Settings](https://help.obsidian.md/settings): current application setting names and locations.
- [About styling](https://docs.obsidian.md/Reference/CSS+variables/About+styling): CSS variables for plugins, themes, and snippets.
- [CSS variables](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables): current variable index by component.
- [Build a theme](https://docs.obsidian.md/Themes/App+themes/Build+a+theme): theme structure, manifest behavior, CSS variables, and inspection workflow.
- [Theme guidelines](https://docs.obsidian.md/Themes/App+themes/Theme+guidelines): local assets, accessibility, selectors, and maintainability.
- [Theme review checklist](https://docs.obsidian.md/oo/theme): performance and compatibility checks used for community themes.

## Agent Skills hosts

- [OpenAI: Build with Agent Skills](https://learn.chatgpt.com/docs/build-skills): skill structure, progressive disclosure, standalone skills, plugins, and supported OpenAI surfaces.
- [OpenAI plugins](https://developers.openai.com/plugins): plugin packaging and distribution.
- [Claude Agent Skills overview](https://claude.com/docs/skills/overview): Agent Skills concepts and Claude product support.
- [Claude Code skills](https://code.claude.com/docs/en/skills): personal and project skill installation and behavior.

## Source-use rules

- Prefer Obsidian Help for user-facing behavior and Obsidian Developer Docs for themes, CSS variables, and plugin development.
- Verify current menu paths and compatibility before giving version-sensitive instructions.
- Verify host installation and availability matrices before claiming ChatGPT, Work, Codex, Claude, web, desktop, or mobile support.
- Distinguish original Markdown, CommonMark/GFM, core Obsidian extensions, and community-plugin syntax.
- Paraphrase documentation and link to it; do not copy long passages into generated notes or skill updates.

## Release maintenance

Before a release or material accuracy update:

1. Update the reviewed date at the top of this file.
2. Run the adjacent `scripts/check_source_links.py`; add `--online` when network access is available.
3. Recheck version-sensitive CLI, Bases, Canvas, theme, and host-compatibility claims against first-party pages.
4. Update focused references rather than copying the documentation site into this skill.
5. Run the unit tests, skill validator, plugin validator, and behavioral evaluation cases.
