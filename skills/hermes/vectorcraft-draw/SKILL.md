---
name: vectorcraft-draw
description: Draw and edit VectorCraft artwork over MCP. Use when the user wants shapes, pen paths, paint, type, Pathfinder booleans, transforms, live effects, or graphs in VectorCraft.
version: 1.0.0
author: Max Infeld
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Creative, Vector, Drawing, Pathfinder, Type]
    related_skills: [vectorcraft, vectorcraft-export]
---

# Draw in VectorCraft

Requires the `vectorcraft` MCP server. Load the `vectorcraft` skill for connection and coordinates.

## Shapes and paths

- Rectangles and ellipses: `draw_shape` with `shape`, `x`, `y`, `width`, `height`, optional `radius`, `fill`, `stroke`, `strokeWidth`.
- Polygons and stars: `cx`, `cy`, `radius` / `radius1`, `radius2`, `sides` or `points`.
- Freeform: `draw_path` with `points` or SVG `d`. Set `closed: true` for filled shapes.
- After each draw, the new object is selected.

## Paint

`set_paint` on the selection or `ids`. Hex, `none`, RGB 0..1, CMYK, or gray. For swatches and gradients, `run_command` `swatch.list` / `swatch.new` / `paint.setFill`.

## Type

Prefer `add_text`. Point type needs `x` and `y`. Area type needs `width` and `height`. On-path type needs `path` and `mode`. Do not use `type_text` in headless mode.

## Booleans and transforms

- `pathfinder` operations: `unite`, `minusFront`, `intersect`, `exclude`, `divide`, `trim`, `merge`, `crop`, `outline`, `minusBack`.
- Live Pathfinder is an effect on a group via `run_command` `effect.apply`.
- `transform` applies move, rotate, scale, reflect, shear. Pass `copy: true` to duplicate.

## Effects and graphs

- `apply_effect` with no `effect` returns the catalogue and defaults. Then call it with `effect` and `params`.
- `create_graph` for column, bar, line, area, scatter, pie, radar. Edit later with `graph.setData` via `run_command`.

## Check your work

`inspect_document`, then `screenshot`. If the picture is wrong, `undo` and fix the arguments. Never claim a drawing succeeded without a screenshot or an inspect that shows the expected ids and bounds.
