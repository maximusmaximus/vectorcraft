"""
VectorCraft Prompt Upscaler Engine.

Connects to high-power reasoning and creative models (XL tier) to upscale
user design requests into turnkey VectorCraft MCP execution blueprints.
"""

from __future__ import annotations

import os
import sys
import time
import json
import logging
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

from .model_resolver import DynamicModelResolver
from .system_prompt import VECTORCRAFT_UPSCALER_SYSTEM_PROMPT

logger = logging.getLogger("vectorcraft_upscaler.upscaler")


@dataclass
class UpscaleResult:
    original_prompt: str
    upscaled_text: str
    model_used: str
    tier: str
    cached_model: bool
    duration_seconds: float
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VectorCraftPromptUpscaler:
    """
    Main engine for transforming raw creative requests into
    VectorCraft MCP-optimized master specifications using high-power models.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tier: str = "xl",
        model: Optional[str] = None,
        cache_ttl_seconds: int = 3600,
        timeout_seconds: int = 45,
    ):
        self.api_key = (
            api_key
            or os.environ.get("UPSCALER_API_KEY")
            or os.environ.get("VENICE_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or ""
        )
        self.base_url = (
            base_url
            or os.environ.get("UPSCALER_BASE_URL")
            or os.environ.get("VENICE_BASE_URL")
            or "https://api.venice.ai/api/v1"
        ).rstrip("/")

        self.override_model = model or os.environ.get("UPSCALER_MODEL")
        self.tier = (tier or os.environ.get("UPSCALER_TIER") or "xl").lower()
        self.timeout = timeout_seconds

        self.resolver = DynamicModelResolver(
            api_key=self.api_key,
            base_url=self.base_url,
            tier=self.tier,
            cache_ttl_seconds=cache_ttl_seconds,
        )

    def _fallback_specification(self, raw_prompt: str, reason: str) -> str:
        """Constructs a structured fallback blueprint if the upstream model call fails."""
        return (
            f"# 🎨 VectorCraft Master Specification (Local Fallback)\n\n"
            f"> [!NOTE] Upscaler model call fell back ({reason}). Applying standard VectorCraft best-practice structure.\n\n"
            f"## 1. Executive Art Direction & Objective\n"
            f"- **User Request**: {raw_prompt}\n"
            f"- **Artboard**: Standard 1024x1024 pt (or 1920x1080 pt widescreen if multi-asset).\n"
            f"- **Execution Directive**: Construct clean vector geometry with cubic Bezier curves (`M ... C ... Z`) "
            f"and batched MCP operations.\n\n"
            f"## 2. Appearance & Palette\n"
            f"- Establish a cohesive 5-swatch palette (Dark, Primary, Midtone, Highlight, Accent).\n"
            f"- Use smooth gradients where depth is required.\n\n"
            f"## 3. Layer Stack\n"
            f"1. Background canvas\n"
            f"2. Primary vector silhouettes\n"
            f"3. Internal accents & shading\n"
            f"4. Typography & overlays\n\n"
            f"## 4. MCP Action Plan\n"
            f"- Batch shapes via `draw_shape` and `draw_path`.\n"
            f"- Merge overlapping forms with `pathfinder`.\n"
            f"- Export to SVG, PDF, and PNG in minimal turns.\n"
        )

    def upscale(
        self,
        raw_prompt: str,
        context: Optional[str] = None,
        force_model_refresh: bool = False,
    ) -> UpscaleResult:
        """
        Upscales a user prompt into a complete VectorCraft MCP master specification.
        """
        t0 = time.time()

        # 1. Resolve model
        if self.override_model:
            model_name = self.override_model
            is_cached = False
        else:
            model_info = self.resolver.resolve_best_model(force_refresh=force_model_refresh)
            model_name = model_info["model"]
            is_cached = model_info.get("cached", False)

        if not self.api_key:
            err = "No API key configured for prompt upscaler (UPSCALER_API_KEY, VENICE_API_KEY, or OPENAI_API_KEY)."
            logger.warning(err)
            return UpscaleResult(
                original_prompt=raw_prompt,
                upscaled_text=self._fallback_specification(raw_prompt, "missing API key"),
                model_used="local_fallback",
                tier=self.tier,
                cached_model=is_cached,
                duration_seconds=round(time.time() - t0, 2),
                success=False,
                error=err,
            )

        # 2. Prepare payload
        user_message = f"User Creative Request: {raw_prompt}"
        if context:
            user_message += f"\n\nAdditional Context / Requirements:\n{context}"

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": VECTORCRAFT_UPSCALER_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
        }

        # Optimization for Venice.ai reasoning models: disable internal reasoning chain to maximize output tokens & speed
        if "venice.ai" in self.base_url:
            payload["venice_parameters"] = {
                "disable_thinking": True,
                "strip_thinking_response": True,
                "include_venice_system_prompt": False,
            }

        endpoint = f"{self.base_url}/chat/completions"
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "VectorCraft-Upscaler/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if not choices:
                    raise ValueError("No choices returned from completions endpoint")
                
                msg = choices[0].get("message", {})
                content = msg.get("content") or ""

                # Handle reasoning models where output might reside in reasoning_content or body
                if not content and msg.get("reasoning_content"):
                    content = msg.get("reasoning_content")

                if not content.strip():
                    raise ValueError("Empty completion text received from model")

                duration = round(time.time() - t0, 2)
                return UpscaleResult(
                    original_prompt=raw_prompt,
                    upscaled_text=content.strip(),
                    model_used=model_name,
                    tier=self.tier,
                    cached_model=is_cached,
                    duration_seconds=duration,
                    success=True,
                )

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            err_msg = f"HTTP {e.code}: {err_body[:200]}"
            logger.error("Upscaler request failed: %s", err_msg)
            return UpscaleResult(
                original_prompt=raw_prompt,
                upscaled_text=self._fallback_specification(raw_prompt, f"HTTP {e.code}"),
                model_used=model_name,
                tier=self.tier,
                cached_model=is_cached,
                duration_seconds=round(time.time() - t0, 2),
                success=False,
                error=err_msg,
            )
        except Exception as e:
            logger.error("Upscaler exception: %s", e)
            return UpscaleResult(
                original_prompt=raw_prompt,
                upscaled_text=self._fallback_specification(raw_prompt, str(e)),
                model_used=model_name,
                tier=self.tier,
                cached_model=is_cached,
                duration_seconds=round(time.time() - t0, 2),
                success=False,
                error=str(e),
            )
