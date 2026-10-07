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
cp -R skills/hermes/vectorcraft-upscaler ~/.hermes/skills/creative/vectorcraft-upscaler
```

Or, if your Hermes build supports path install:

```sh
hermes skills install ./skills/hermes/vectorcraft
hermes skills install ./skills/hermes/vectorcraft-draw
hermes skills install ./skills/hermes/vectorcraft-export
hermes skills install ./skills/hermes/vectorcraft-upscaler
```

Skills:

| Skill | When Hermes should load it |
|---|---|
| `vectorcraft` | Any VectorCraft / MCP session: connect, inspect, command catalogue |
| `vectorcraft-draw` | Drawing, paint, type, Pathfinder, transforms, effects |
| `vectorcraft-export` | Open, save, export SVG/PDF/PNG and visual QA via screenshot |
| `vectorcraft-upscaler` | High-power XL prompt upscaling: converts raw creative prompts into exact vector specs |

## High-Power Prompt Upscaling (XL Reasoning Tier)

To avoid exploratory tool thrashing and minimize back-and-forth roundtrips over MCP, VectorCraft includes a specialized Prompt Upscaler package (`packages/vectorcraft_upscaler/`).

### How It Works

1. **Periodic Best-Model Resolution**: The upscaler dynamically queries the provider's `/models` endpoint on a configurable TTL cycle (default: 3600s / 1 hour) to identify the highest-scoring reasoning/coding model in the requested tier (e.g. `xl` tier: Moonshot Kimi K3, Claude Opus 5, Grok 4.20, DeepSeek V4 Pro).
2. **VectorCraft Architecture Specification**: The resolved model transforms brief user ideas into comprehensive specifications with exact SVG cubic Bezier anchors (`M ... C ... S ... Z`), geometric coordinates, 5-swatch palettes with hex codes, and 5-turn MCP batch execution plans.
3. **Turn Minimization**: Equips the downstream executor to execute vector construction in 3-5 cohesive turns rather than 20+ piecemeal queries.

### Configuration

Set standard environment variables in your Hermes or system environment:

```sh
export UPSCALER_API_KEY="your-api-key"             # Provider API key
export UPSCALER_BASE_URL="https://api.venice.ai/api/v1" # OpenAI/Venice endpoint
export UPSCALER_TIER="xl"                           # Target tier: xl, l, m, s
export UPSCALER_CACHE_TTL="3600"                    # Model refresh TTL in seconds
```

### Direct CLI Usage

```sh
python3 packages/vectorcraft_upscaler/cli.py "draw an art deco badge" --tier xl
```

Protocol details remain in [`docs/mcp.md`](docs/mcp.md) and [`docs/control-protocol.md`](docs/control-protocol.md).

## Brand note

Upstream's brand license (`docs/brand/LICENSE-brand.txt`) says forks and modified versions must remove the ArtCraft name, wordmark, and logos. This fork currently keeps them so it stays a faithful fork of upstream. Strip `docs/brand/` before redistributing a modified build.
