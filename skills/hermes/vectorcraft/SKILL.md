---
name: vectorcraft
description: Drive VectorCraft, an open-source Illustrator-class vector editor, over its stdio MCP server. Use when creating, inspecting, editing, or exporting vector artwork (.vectorcraft, SVG, PDF, PNG) or when the user mentions VectorCraft, vectorcraft-cli, or vector illustration via MCP.
version: 1.0.0
author: Max Infeld
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Creative, Vector, MCP, Illustrator, Design]
    related_skills: [vectorcraft-draw, vectorcraft-export, native-mcp]
---

# VectorCraft MCP

VectorCraft is a clean-room Rust vector editor. Agents drive it through `vectorcraft-cli mcp` (stdio MCP, protocol 2025-06-18). Do not scrape the GUI. Call MCP tools.

## Connect

1. Confirm `mcp_vectorcraft_*` tools are available. If not, tell the user to add the server to `~/.hermes/config.yaml` and reload MCP. Template: `${HERMES_SKILL_DIR}/references/hermes-config.yaml`.
2. Build if needed: `cargo build --release -p vectorcraft-cli` from the repo root. Binary is `target/release/vectorcraft-cli`.
3. Prefer headless (`mcp --headless`) for batch work. Use remote (`mcp --connect 127.0.0.1:7979` while the app runs with `--control 7979`) only when the user wants to watch the canvas.

## Coordinate system

- Document space, y increases downward.
- Origin is the first artboard's top-left.
- A new document is 612 x 792 (US Letter).
- New objects become the selection. Most commands act on the selection or on explicit `ids`.

## Tool order

1. `inspect_document` before editing an existing file, and after any structural change.
2. Dedicated tools when one exists: `draw_path`, `draw_shape`, `set_paint`, `add_text`, `pathfinder`, `transform`, `apply_effect`, `create_graph`, `text_wrap`, `open_file`, `save_file`, `export`, `screenshot`, `undo`, `redo`, `select_tool`.
3. `list_commands` with a filter, then `run_command`, for everything else (swatches, appearance, blends, envelopes, graphs).
4. `screenshot` after visual work. Read the image. If it is wrong, `undo` and retry.
5. Errors return `isError: true` plus a message. Read it and retry. Do not invent command ids.

Paint values accept `"#rrggbb"`, `"none"`, `[r,g,b]` in 0..1, `{"c","m","y","k"}`, `{"gray"}`, or a full paint object.

Headless does not support `inspect_ui`, `type_text`, `open_panel`, or `screenshot` with `window: true`.

Full tool table: `${HERMES_SKILL_DIR}/references/mcp-tools.md`. Upstream protocol: `docs/mcp.md` in the VectorCraft repo.

## Session pattern

```text
open_file or start from the blank document
inspect_document
draw / paint / type / pathfinder
inspect_document
screenshot
export or save_file
```

Related skills: `vectorcraft-draw` for construction, `vectorcraft-export` for files.
