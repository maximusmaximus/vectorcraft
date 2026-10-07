---
name: vectorcraft-upscaler
description: Upscale raw creative prompts into exhaustive VectorCraft MCP design specifications using a high-power XL reasoning model. Minimizes tool turns and guesswork before executing vector art.
version: 1.0.0
author: Maximus
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Creative, Vector, MCP, Illustrator, Design, Prompt-Engineering, Upscaler]
    related_skills: [vectorcraft, vectorcraft-draw, vectorcraft-export]
---

# VectorCraft Prompt Upscaler

Use this skill whenever a user submits an ambiguous, high-level, or complex illustration request targeting VectorCraft / Adobe Illustrator MCP.

Instead of guessing artboard bounds, trying random color palettes, or making exploratory tool calls, the Prompt Upscaler queries a top-tier **XL reasoning model** (periodically resolved to the latest flagship) to produce an authoritative, turnkey vector design blueprint.

## When to Upscale

1. The user asks to draw, design, or generate complex vector assets (logos, badges, character art, packaging suites, tessellation patterns).
2. The user's prompt lacks explicit mathematical coordinates, color hex codes, or layer ordering.
3. You need to execute an illustration in **minimal MCP roundtrips** without back-and-forth trial and error.

## Running the Upscaler

From within Hermes, execute the upscaler script via `execute_code` or `terminal`:

```bash
python3 packages/vectorcraft_upscaler/cli.py "User's raw prompt" --tier xl
```

Or programmatically in Python:

```python
from vectorcraft_upscaler import VectorCraftPromptUpscaler

upscaler = VectorCraftPromptUpscaler(tier="xl")
result = upscaler.upscale(
    raw_prompt="design a 10-artboard packaging suite for luxury matcha tea",
    context="Artboards: 10 artboards @ 800x800pt. Formats: PDF and SVG."
)

print(result.upscaled_text)
```

## How It Minimizes MCP Roundtrips

The upscaler converts the prompt into a 5-part blueprint:
1. **Artboard & Canvas Setup**: Exact dimensions and bleed margins.
2. **Harmonious Palette**: Exact hex codes for solid fills and linear/radial gradient stops.
3. **Layer Hierarchy**: Z-indexed stacks (`[Background]`, `[Structural Geometry]`, `[Primary Subject]`, `[Accents]`, `[Typography]`).
4. **Cubic Bezier & Boolean Math**: Clean SVG path data (`M ... C ... Z`) and Pathfinder operations (`unite`, `minusFront`, `intersect`).
5. **Batch Execution Plan**: Groups commands into 3-5 cohesive turns rather than 20+ piecemeal queries.
