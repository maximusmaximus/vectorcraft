# Hermes Agent

VectorCraft's MCP server is already the agent API. Hermes Agent consumes it as a stdio MCP server and uses the skills in `skills/hermes/`.

See [HERMES.md](../HERMES.md) for install steps.

## Modes

| Mode | Launch | Use when |
|---|---|---|
| Headless | `vectorcraft-cli mcp --headless` | Batch drawing and export. No `inspect_ui`, `type_text`, `open_panel`, or window screenshots. |
| Remote | App with `--control 7979`, server with `mcp --connect 127.0.0.1:7979` | You want to watch the app update live. |
| Auto | `vectorcraft-cli mcp` | Tries `127.0.0.1:7979`, then falls back to headless. |

Logs go to stderr. Stdout is protocol only.

## Tool names inside Hermes

Hermes prefixes MCP tools with the server name. A config key of `vectorcraft` and a tool `draw_path` becomes `mcp_vectorcraft_draw_path`.

Prefer dedicated tools. Use `list_commands` then `run_command` for the rest of the ~400 engine commands (swatches, appearance stacks, graphs, blends, envelopes).
