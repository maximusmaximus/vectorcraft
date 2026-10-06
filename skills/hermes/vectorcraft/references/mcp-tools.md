# VectorCraft MCP tools

Source of truth is upstream `docs/mcp.md`. This is the agent cheat sheet.

| Tool | Arguments | Notes |
|---|---|---|
| `list_commands` | `{filter?, enabledOnly?}` | Catalogue: id, label, menu, shortcut, params, enablement. |
| `run_command` | `{command, params?}` | Any engine command. Use when no dedicated tool exists. |
| `inspect_document` | `{}` | Artboards, layer tree, selection, history, tool. |
| `inspect_ui` | `{}` | Remote only. |
| `select_tool` | `{tool}` | `selection`, `directSelection`, `pen`, `rectangle`, `ellipse`, `polygon`, `star`, `lineSegment`, ... |
| `pointer_gesture` | `{events:[{kind,x,y,mods?}], tool?, mods?}` | `kind`: `down`, `drag`, `up`, `move`, `doubleclick`. |
| `draw_path` | `{points \| d, closed?, fill?, stroke?, strokeWidth?}` | `points` is `[[x,y],...]` or handles. `d` is SVG path data. |
| `draw_shape` | `{shape, ...geometry, fill?, stroke?, strokeWidth?}` | rectangle/ellipse: x,y,width,height. polygon: cx,cy,radius,sides. star: cx,cy,radius1,radius2,points. line: x1,y1,x2,y2. |
| `set_paint` | `{fill?, stroke?, strokeWidth?, ids?}` | Selection or ids. Becomes the default for new art. |
| `press_key` | `{key, mods?}` | Remote: real key. Headless: bound command. |
| `type_text` | `{text}` | Remote only. Prefer `add_text` in headless. |
| `invoke_menu` | `{command, params?}` | Menu command id. |
| `open_panel` | `{panel}` | Remote only. |
| `screenshot` | `{path?, scale?, artboard?, window?}` | Returns PNG image content. `window: true` is remote only. |
| `open_file` | `{path}` | `.vectorcraft`, SVG, PDF, `.ai`, raster. |
| `save_file` | `{path?}` | Extension picks format. |
| `export` | `{path?, format?, scale?, artboard?, range?, selection?, outlineText?, options?}` | svg, pdf, png, jpg, webp, gif, tiff, bmp, psd, txt, vectorcraft. |
| `add_text` | `{text, x?, y?, width?, height?, path?, mode?, size?, font?, color?}` | Point, area, or on-path type. |
| `apply_effect` | `{effect?, params?, ids?}` | No effect: returns the catalogue. |
| `pathfinder` | `{operation, ids?}` | unite, minusFront, intersect, exclude, divide, trim, merge, crop, outline, minusBack. |
| `transform` | `{ids?, dx?, dy?, rotate?, scale?, scaleX?, scaleY?, reflect?, shear?, origin?, copy?}` | Move, rotate, scale, reflect, shear. `copy` duplicates. |
| `create_graph` | `{type?, x, y, width, height, csv? \| series?, categories?, rows?}` | Nine graph types. |
| `text_wrap` | `{ids?, offset?, invert?, release?}` | Area type flows around objects. |
| `undo` / `redo` | `{}` | |

Resources: `vectorcraft://document`, `vectorcraft://document/json`.

Common `run_command` ids: `swatch.list`, `swatch.new`, `swatch.edit`, `file.new`, `appearance.addFill`, `appearance.addStroke`, `effect.apply`, `effect.list`, `color.harmony`, `colorTheme.save`, `document.formats`.
