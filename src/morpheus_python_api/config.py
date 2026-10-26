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
