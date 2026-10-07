"""
Command-Line Interface for VectorCraft Prompt Upscaler.
"""

from __future__ import annotations

import argparse
import sys
import json
from .upscaler import VectorCraftPromptUpscaler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upscale user creative prompts into VectorCraft MCP master design blueprints."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The raw user design or illustration request (e.g. 'draw an art deco badge').",
    )
    parser.add_argument(
        "--tier",
        default="xl",
        choices=["xl", "l", "m", "s"],
        help="Model quality tier to target (default: xl).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Explicitly override the model ID instead of dynamic resolution.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Bypass TTL cache and force a fresh model resolution query.",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Optional additional context (artboard sizes, style guidelines, existing layers).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to write the upscaled markdown specification to.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full metadata in JSON format.",
    )

    args = parser.parse_args()

    if not args.prompt:
        if not sys.stdin.isatty():
            raw_prompt = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)
    else:
        raw_prompt = args.prompt

    upscaler = VectorCraftPromptUpscaler(
        tier=args.tier,
        model=args.model,
    )

    res = upscaler.upscale(
        raw_prompt=raw_prompt,
        context=args.context,
        force_model_refresh=args.refresh,
    )

    if args.json:
        out_text = json.dumps(res.to_dict(), indent=2)
    else:
        out_text = res.upscaled_text

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_text)
        print(f"Upscaled specification written to {args.output} (Model: {res.model_used}, Tier: {res.tier})", file=sys.stderr)
    else:
        print(out_text)

    if not res.success:
        sys.exit(1)


if __name__ == "__main__":
    main()
