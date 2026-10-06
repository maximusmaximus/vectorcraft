# VectorCraft for Hermes Agent

This fork of [storytold/vectorcraft](https://github.com/storytold/vectorcraft) adds Hermes Agent skills on top of the upstream MCP server. The Rust MCP server itself already ships in `crates/mcp` and `apps/vectorcraft-cli`.

Public fork: https://github.com/maximusmaximus/vectorcraft

## What you get

- Full stdio MCP server (`vectorcraft-cli mcp`), protocol `2025-06-18` (also accepts `2025-03-26` and `2024-11-05`).
- Remote mode (live app on the control channel) and headless mode (in-process engine).
- Hermes skills that teach the agent how to connect, draw, paint, type, pathfind, and export.

## Build the server

```sh
git clone https://github.com/maximusmaximus/vectorcraft
cd vectorcraft
cargo build --release -p vectorcraft-cli
```

Binary: `target/release/vectorcraft-cli`.

## Register with Hermes

Add this to `~/.hermes/config.yaml` (use the absolute path to the binary):

```yaml
mcp_servers:
  vectorcraft:
    command: "/absolute/path/to/vectorcraft/target/release/vectorcraft-cli"
    args: ["mcp", "--headless"]
    timeout: 180
    tools:
      include:
        - list_commands
        - run_command
        - inspect_document
        - select_tool
        - draw_path
        - draw_shape
        - set_paint
        - add_text
        - pathfinder
        - transform
        - apply_effect
        - create_graph
        - text_wrap
        - screenshot
        - open_file
        - save_file
        - export
        - undo
        - redo
```

Live app instead of headless:

```sh
cargo run --release -p vectorcraft -- --control 7979
```

```yaml
mcp_servers:
  vectorcraft:
    command: "/absolute/path/to/vectorcraft/target/release/vectorcraft-cli"
    args: ["mcp", "--connect", "127.0.0.1:7979"]
    timeout: 180
```

Reload MCP (`/reload-mcp`) or restart Hermes. Tools show up as `mcp_vectorcraft_<tool>`.

## Install the skills

Copy the skill directories into the Hermes skills tree:

```sh
mkdir -p ~/.hermes/skills/creative
cp -R skills/hermes/vectorcraft ~/.hermes/skills/creative/vectorcraft
cp -R skills/hermes/vectorcraft-draw ~/.hermes/skills/creative/vectorcraft-draw
cp -R skills/hermes/vectorcraft-export ~/.hermes/skills/creative/vectorcraft-export
```

Or, if your Hermes build supports path install:

```sh
hermes skills install ./skills/hermes/vectorcraft
hermes skills install ./skills/hermes/vectorcraft-draw
hermes skills install ./skills/hermes/vectorcraft-export
```

Skills:

| Skill | When Hermes should load it |
|---|---|
| `vectorcraft` | Any VectorCraft / MCP session: connect, inspect, command catalogue |
| `vectorcraft-draw` | Drawing, paint, type, Pathfinder, transforms, effects |
| `vectorcraft-export` | Open, save, export SVG/PDF/PNG and visual QA via screenshot |

Protocol details remain in [`docs/mcp.md`](docs/mcp.md) and [`docs/control-protocol.md`](docs/control-protocol.md).

## Brand note

Upstream's brand license (`docs/brand/LICENSE-brand.txt`) says forks and modified versions must remove the ArtCraft name, wordmark, and logos. This fork currently keeps them so it stays a faithful fork of upstream. Strip `docs/brand/` before redistributing a modified build.
