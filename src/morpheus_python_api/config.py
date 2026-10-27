"""
config.py

Configuration functions useful across modules.

Instead of setting environment variables directly, which a given application
might reasonably do, bin_path and morphlib_path copy the existing environment
as a dictionary and add the relevant paths to the dictionary.
"""

import os
from pathlib import Path


def bin_path() -> Path:
    override = os.environ.get("BIN_PATH")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / "bin"


def morphlib_path() -> Path:
    override = os.environ.get("MORPHLIB")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / "stemlib"
