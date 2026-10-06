---
name: vectorcraft-export
description: Open, save, and export VectorCraft documents over MCP. Use when the user wants SVG, PDF, PNG, JPEG, WebP, AI-compatible PDF, or native .vectorcraft output, or a screenshot QA of the artboard.
version: 1.0.0
author: Max Infeld
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Creative, Vector, Export, SVG, PDF]
    related_skills: [vectorcraft, vectorcraft-draw]
---

# Export from VectorCraft

Requires the `vectorcraft` MCP server.

## Open

`open_file` with a path. Accepts `.vectorcraft`, `.drawcraft`, `.svg`, `.svgz`, `.pdf`, `.ai`, `.ait`, PNG, JPEG, GIF, WebP, TIFF, BMP. Images open as a document of their pixel size.

## Save

`save_file` with a path. The extension selects the format:

- `.vectorcraft` native JSON
- `.svg` / `.svgz`
- `.pdf`
- `.ai` PDF that still carries the native document and reopens editable
- `.vctemplate`

Omit the path to save the document's own file.

## Export

`export` for a rendition that does not retarget the document path.

- `format`: `svg`, `pdf`, `png`, `jpg`, `webp`, `gif`, `png8`, `tiff`, `bmp`, `tga`, `psd`, `txt`, `vectorcraft`. If omitted, taken from the path extension.
- PDF is one page per artboard. Other formats write one artboard. Use `artboard` (0-based) or `range` (`"1-3, 5"`, 1-based).
- `selection: true` crops to the selection. `outlineText: true` converts SVG text to paths.
- `options` holds format extras, for example `{"quality": 80}` for JPEG, or SVG options (`styling`, `decimals`, `minify`, `preserveEditing`).
- Without `path`, bytes come back as `dataBase64`.
- `run_command` `document.formats` lists formats and option defaults.

## Visual QA

Call `screenshot` before handing a file to the user. It returns PNG image content. Compare it to the request. Fix with `undo` plus another edit, then export again.

Tell the user the absolute output path and the format. Do not claim PDF/X or font embedding unless `document.formats` or the export result says that option was applied.
