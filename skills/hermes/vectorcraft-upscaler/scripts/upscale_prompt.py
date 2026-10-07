#!/usr/bin/env python3
"""
Hermes Skill Runner for VectorCraft Prompt Upscaler.
"""

import sys
import os
from pathlib import Path

# Add package root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
PACKAGES_DIR = REPO_ROOT / "packages" / "vectorcraft_upscaler"

if str(REPO_ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "packages"))

try:
    from vectorcraft_upscaler.cli import main
except ImportError:
    # Direct import fallback if installed as package or submodule
    sys.path.insert(0, str(PACKAGES_DIR))
    from vectorcraft_upscaler.cli import main

if __name__ == "__main__":
    main()
