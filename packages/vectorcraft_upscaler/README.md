# VectorCraft Prompt Upscaler

Autonomous high-power prompt upscaling engine specialized for **VectorCraft** (an open-source Adobe Illustrator clone with an in-engine MCP server).

## Overview

AI agents interacting with VectorCraft over MCP often suffer from high token usage and excessive tool roundtrips when working from short, vague prompts. The **VectorCraft Prompt Upscaler** solves this by pre-processing user creative requests through flagship high-power models (**XL tier**, e.g. Moonshot Kimi K3, Claude Opus 5, Grok 4.20, DeepSeek V4 Pro).

The upscaler transforms high-level creative prompts into **exhaustive, mathematically sound vector design specifications** that map directly to the VectorCraft MCP tool suite (`draw_path`, `draw_shape`, `set_paint`, `add_text`, `pathfinder`, `transform`, `export`).

### Key Capabilities

1. **Illustrator-Domain Specialization**: Generates exact SVG cubic Bezier curve anchors (`M`, `C`, `S`, `Z`), geometric coordinates, 5-swatch color systems with exact hex codes, gradient stops, and ordered layer hierarchies.
2. **Minimal MCP Roundtrips**: Supplies the downstream agent with an actionable batch execution recipe, eliminating exploratory guesswork turns and speculative probing.
3. **Periodic Best-Model Resolution**: Dynamically queries the model provider endpoint (`/models`) on a configurable TTL cycle (default: 1 hour) to always select the latest, top-performing flagship reasoning/code model in the requested tier.
4. **Resilient Fallback**: Non-blocking design with local cache persistence. If network connectivity drops or the remote endpoint is unavailable, it gracefully falls back to cached resolutions or structured local templates.

---

## Configuration

The upscaler is fully generalized and configurable via environment variables:

| Variable | Description | Default |
|---|---|---|
| `UPSCALER_API_KEY` | Provider API key (also checks `VENICE_API_KEY`, `OPENAI_API_KEY`) | None (required for remote inference) |
| `UPSCALER_BASE_URL` | Base API URL (OpenAI / Venice compatible) | `https://api.venice.ai/api/v1` |
| `UPSCALER_TIER` | Target model quality tier (`xl`, `l`, `m`, `s`) | `xl` |
| `UPSCALER_MODEL` | Explicit model override (bypasses dynamic resolution) | Dynamic / Top-ranked |
| `UPSCALER_CACHE_TTL` | Model resolution cache lifespan in seconds | `3600` (1 hour) |
| `UPSCALER_FALLBACK_MODEL` | Emergency fallback model if resolution fails | `kimi-k3` |

---

## Installation & CLI Usage

### Install

```sh
cd packages/vectorcraft_upscaler
pip install -e .
```

### CLI Command

```sh
# Upscale a creative prompt
vectorcraft-upscale "draw a vintage Japanese woodblock wave illustration"

# Target specific tier or model
vectorcraft-upscale "design a luxury matcha tea packaging suite" --tier xl -o spec.md

# Pipe from standard input
echo "cyberpunk motorcycle technical vector emblem" | vectorcraft-upscale --json
```

---

## Python API

```python
from vectorcraft_upscaler import VectorCraftPromptUpscaler

upscaler = VectorCraftPromptUpscaler(tier="xl")
result = upscaler.upscale(
    raw_prompt="design a 10-artboard icon set for sustainable energy",
    context="Artboards: 512x512 pt each. Style: Minimalist duotone vector."
)

print("Model Used:", result.model_used)
print("Duration:", result.duration_seconds, "s")
print(result.upscaled_text)
```
