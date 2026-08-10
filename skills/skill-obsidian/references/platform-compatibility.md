# Agent Skills platform compatibility

Use this reference when installing, distributing, or describing this skill across agent products. Host capabilities and installation mechanisms change; verify current first-party documentation before promising support.

## Package boundaries

This repository has two useful boundaries:

- The repository root is an OpenAI plugin package with `.codex-plugin/plugin.json`.
- `skills/skill-obsidian/` is the portable Agent Skill directory containing `SKILL.md`, references, scripts, and agent metadata.

Use the smallest boundary the host accepts. Do not copy only `SKILL.md`; its relative references and checker are part of the skill.

## Compatibility matrix

| Host | Package form | Practical boundary |
| --- | --- | --- |
| ChatGPT and ChatGPT Work | OpenAI plugin or supported standalone skill upload | Plugin distribution can make the skill available across supported ChatGPT surfaces; actual file and code access still depends on the session. |
| Codex CLI and IDE | Standalone skill directory or installed plugin | Filesystem and shell work depend on the active sandbox and approvals. |
| ChatGPT desktop | Standalone skill or plugin where supported | Desktop presence does not itself grant Obsidian UI control. |
| Claude Code | Copy the portable skill to the documented personal or project skills directory | Claude Code follows the Agent Skills directory convention; tool permissions still govern access. |
| Claude.ai and Claude Work | Upload or install using the current Skills interface | Skills that execute scripts require the host's code-execution capability. |
| Other Agent Skills hosts | Portable skill directory if supported | Confirm support for references, scripts, dependencies, and progressive disclosure. |

OpenAI currently distinguishes standalone skills from plugin-bundled skills, and surface availability differs between those forms. Consult current OpenAI documentation for the exact ChatGPT, Work, Codex, web, desktop, and mobile matrix before release.

## Installation checks

After installation:

1. Confirm the host discovers `skill-obsidian` and exposes its description.
2. Trigger a note-authoring request and verify the Markdown reference is loaded.
3. Trigger a CSS, CLI, Base, and Canvas request and verify the correct focused reference is selected.
4. If scripts can run, verify PyYAML and run the checker on a temporary valid and invalid note.
5. If scripts cannot run, treat checker execution as unavailable and continue with manual review.
6. Confirm the agent states its real access boundary instead of claiming to have edited or rendered a vault.

Never encode host-specific secrets, absolute vault paths, or credentials into the distributed skill.
