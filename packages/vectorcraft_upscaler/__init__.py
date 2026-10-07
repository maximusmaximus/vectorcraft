"""
VectorCraft Prompt Upscaler
Autonomous High-Power Prompt Upscaling and Architecture Blueprint Engine for VectorCraft MCP.
"""

from .upscaler import VectorCraftPromptUpscaler, UpscaleResult
from .model_resolver import DynamicModelResolver
from .system_prompt import VECTORCRAFT_UPSCALER_SYSTEM_PROMPT

__version__ = "1.0.0"
__all__ = [
    "VectorCraftPromptUpscaler",
    "UpscaleResult",
    "DynamicModelResolver",
    "VECTORCRAFT_UPSCALER_SYSTEM_PROMPT",
]
