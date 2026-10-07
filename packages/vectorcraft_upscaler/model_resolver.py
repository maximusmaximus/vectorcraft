"""
Dynamic Best-Model Resolver for High-Power Prompt Upscaling.

Periodically queries the model provider endpoint (Venice or OpenAI-compatible)
to dynamically identify, rank, and cache the highest-capability model in the requested
tier (e.g. XL reasoning/creative flagship), refreshing on a configurable TTL cycle.
"""

from __future__ import annotations

import os
import sys
import time
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("vectorcraft_upscaler.model_resolver")

# Default Tier Rankings (ordered from strongest flagship down)
DEFAULT_TIER_PRIORITIES = {
    "xl": [
        "kimi-k3",
        "claude-opus-5",
        "deepseek-v4-pro",
        "grok-4-20",
        "hermes-3-llama-3.1-405b",
        "openai-gpt-55-pro",
        "openai-gpt-54",
        "e2ee-kimi-k3-p",
        "deepseek-r1",
        "llama-3.3-70b",
    ],
    "l": [
        "deepseek-v4-pro",
        "kimi-k2-6",
        "claude-sonnet-5",
        "grok-4-5",
        "openai-gpt-54-mini",
        "e2ee-kimi-k2-6",
    ],
    "m": [
        "deepseek-v4-flash",
        "mistral-small-3-2-24b-instruct",
        "google-gemma-3-27b-it",
        "deepseek-v4-1-flash",
        "e2ee-deepseek-v4-flash",
    ],
    "s": [
        "mercury-2-5",
        "qwen-2-5-7b",
        "llama-3.2-3b",
        "e2ee-qwen-2-5-7b-p",
    ],
}


class DynamicModelResolver:
    """
    Periodically resolves the best available model for prompt upscaling
    based on quality tier, reasoning capabilities, and context headroom.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tier: str = "xl",
        cache_ttl_seconds: int = 3600,
        cache_path: Optional[str] = None,
        fallback_model: Optional[str] = None,
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

        self.tier = (tier or os.environ.get("UPSCALER_TIER") or "xl").lower()
        self.cache_ttl = int(
            os.environ.get("UPSCALER_CACHE_TTL") or cache_ttl_seconds
        )
        self.fallback_model = (
            fallback_model
            or os.environ.get("UPSCALER_FALLBACK_MODEL")
            or (DEFAULT_TIER_PRIORITIES.get(self.tier, ["kimi-k3"])[0])
        )

        if cache_path:
            self.cache_file = Path(cache_path)
        else:
            default_dir = Path(os.environ.get("HOME", os.environ.get("USERPROFILE", "."))) / ".cache" / "vectorcraft"
            self.cache_file = default_dir / f"upscaler_model_{self.tier}.json"

    def _read_cache(self) -> Optional[Dict[str, Any]]:
        """Reads cached model resolution if present and unexpired."""
        if not self.cache_file.exists():
            return None
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            cached_time = data.get("timestamp", 0)
            if time.time() - cached_time < self.cache_ttl:
                return data
        except Exception as e:
            logger.debug("Failed to read upscaler model cache: %s", e)
        return None

    def _write_cache(self, data: Dict[str, Any]) -> None:
        """Persists model resolution cache safely."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            tmp_file = self.cache_file.with_suffix(".tmp")
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            tmp_file.replace(self.cache_file)
        except Exception as e:
            logger.warning("Failed to write upscaler model cache: %s", e)

    def fetch_available_models(self) -> List[Dict[str, Any]]:
        """Queries the /models endpoint of the configured provider."""
        if not self.api_key:
            return []

        models_endpoint = f"{self.base_url}/models"
        req = urllib.request.Request(
            models_endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "VectorCraft-Upscaler/1.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("data", [])
        except Exception as e:
            logger.warning("Could not fetch remote models from %s: %s", models_endpoint, e)
            return []

    def rank_best_model(self, models: List[Dict[str, Any]]) -> str:
        """Ranks models to select the premier candidate for prompt upscaling."""
        if not models:
            return self.fallback_model

        active_models = {
            m.get("id"): m
            for m in models
            if not m.get("model_spec", {}).get("offline", False)
            and m.get("type", "text") in ("text", "chat", None)
        }

        # 1. First priority: Check predefined tier priorities
        tier_picks = DEFAULT_TIER_PRIORITIES.get(self.tier, DEFAULT_TIER_PRIORITIES["xl"])
        for pick in tier_picks:
            if pick in active_models:
                return pick

        # 2. Dynamic scoring based on reasoning, code optimization, and context window
        scored = []
        for mid, m in active_models.items():
            spec = m.get("model_spec", {})
            caps = spec.get("capabilities", {})
            ctx = m.get("context_length", 0) or spec.get("availableContextTokens", 0) or 0
            
            score = 0
            if caps.get("supportsReasoning", False):
                score += 50
            if caps.get("optimizedForCode", False):
                score += 30
            if ctx >= 1_000_000:
                score += 20
            elif ctx >= 128_000:
                score += 10

            scored.append((score, ctx, mid))

        if scored:
            scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
            return scored[0][2]

        return self.fallback_model

    def resolve_best_model(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Resolves the best model, utilizing the TTL cache when valid.
        Returns a dict containing the resolved model ID, tier, and cache metadata.
        """
        if not force_refresh:
            cached = self._read_cache()
            if cached and "model" in cached:
                return {
                    "model": cached["model"],
                    "tier": self.tier,
                    "cached": True,
                    "resolved_at": cached.get("resolved_at"),
                    "ttl_remaining_seconds": max(0, int(self.cache_ttl - (time.time() - cached.get("timestamp", 0)))),
                }

        # Query fresh models
        models = self.fetch_available_models()
        best_model = self.rank_best_model(models)

        resolved_data = {
            "model": best_model,
            "tier": self.tier,
            "cached": False,
            "timestamp": time.time(),
            "resolved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_models_evaluated": len(models),
        }

        self._write_cache(resolved_data)
        return resolved_data
