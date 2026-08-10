# CSS and interface customization

Use this reference for appearance settings, CSS snippets, note-specific styling, callout styling, and theme work.

## Contents

- [Choose the customization layer](#choose-the-customization-layer)
- [Create a CSS snippet](#create-a-css-snippet)
- [Write resilient CSS](#write-resilient-css)
- [Scope styles to notes](#scope-styles-to-notes)
- [Customize callouts](#customize-callouts)
- [Develop a theme](#develop-a-theme)
- [Test and recover](#test-and-recover)

## Choose the customization layer

Use the least complex layer that meets the need:

| Need | Preferred layer |
| --- | --- |
| Font, accent, light/dark mode, readable line length | Built-in Appearance settings |
| Broad prebuilt visual identity | Community theme |
| One focused override | CSS snippet |
| A style for selected notes | CSS snippet plus `cssclasses` |
| Maintained, distributable visual system | Full theme |

Do not recommend a theme or plugin when a supported setting is enough.

## Create a CSS snippet

Store snippets as `.css` files in `<vault>/.obsidian/snippets/`. On desktop, use **Settings → Appearance → CSS snippets → Open snippets folder**, create the file, select **Reload snippets**, and enable it. Obsidian normally detects subsequent saves without a restart.

On mobile or tablet, locate the vault using a file manager, create `.obsidian/snippets/` if needed, add the file, then reload and enable it under **Settings → Appearance → CSS snippets**.

Never edit the application's bundled `app.css`; it is an inspection target, not a customization file.

## Write resilient CSS

Prefer documented Obsidian CSS variables:

```css
body {
  --h1-color: var(--color-accent);
  --file-line-width: 52rem;
}
```

Use `body` for values shared by both schemes and `.theme-dark` or `.theme-light` only when values must differ:

```css
.theme-dark {
  --background-primary: #17181c;
}

.theme-light {
  --background-primary: #fbfbfc;
}
```

Follow these rules:

- Prefer variables over deep selectors tied to transient DOM structure.
- Inspect the current app with Developer Tools when no documented variable exists.
- Keep specificity low, scope selectors narrowly, and avoid `!important` unless cascade inspection proves it necessary.
- Avoid `:has()` unless no simpler selector works; it can be expensive, especially in Canvas.
- Keep fonts, images, and other assets local. Remote assets can fail offline and disclose requests to third parties.
- Include visible keyboard focus states, sufficient contrast, readable text sizing, and reduced-motion behavior where animation is introduced.
- Check editor and Reading view; their DOM structures differ.
- Check both light and dark modes, narrow panes, and mobile when relevant.
- Add a short comment stating purpose and expected scope, not a narrative changelog.

Obsidian's DOM and undocumented selectors may change. State that maintenance risk when a selector cannot use a stable variable or class.

## Scope styles to notes

Add one or more classes through the `cssclasses` property:

```yaml
---
cssclasses:
  - wide-table-note
---
```

Then scope the CSS:

```css
.wide-table-note {
  --file-line-width: 72rem;
}
```

Use a semantic class name that describes purpose rather than a current color or pixel value. Match any established vault convention before adding a new class.

## Customize callouts

Target a custom callout identifier with `data-callout`:

```css
.callout[data-callout="decision"] {
  --callout-color: rgb(46, 160, 67);
  --callout-icon: lucide-git-branch;
}
```

Use it in Markdown:

```markdown
> [!decision] Approved direction
> Record the decision and its consequences.
```

Lucide icon availability changes as Obsidian updates its bundled version. Verify a current icon before relying on it, and ensure an unknown callout still remains legible with the default rendering.

## Develop a theme

A distributable theme lives under `<vault>/.obsidian/themes/<Theme Name>/` and includes `theme.css` plus `manifest.json`. The directory name must exactly match the manifest's `name` value.

Start from Obsidian's official sample theme. Use CSS variables for compatible plugin and theme behavior. Restart Obsidian after changing the manifest; Obsidian picks up ordinary CSS edits after a reload or file save.

Build a full theme only when the user accepts maintenance across Obsidian releases. Keep snippets separate when they represent personal or vault-specific overrides rather than the theme itself.

## Test and recover

For each customization:

1. Save the original snippet or establish a version-control checkpoint.
2. Enable only the new snippet while debugging.
3. Check Source mode, Live Preview, and Reading view as applicable.
4. Check the default theme to distinguish snippet defects from theme conflicts.
5. Check light and dark schemes and keyboard focus.
6. Check narrow panes, zoom, reduced motion, and mobile when relevant.
7. Inspect Canvas performance if selectors can match many nodes.
8. Validate CSS syntax with an appropriate validator.
9. Disable or remove the snippet to confirm the rollback path.

When a style fails, inspect selector matching and computed values before increasing specificity.
