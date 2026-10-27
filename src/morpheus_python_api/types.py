"""types.py
Module for any type and enum definitions useful across modules.
"""

from enum import auto, Enum


class Language(Enum):
    GREEK = auto()
    LATIN = auto()
    ITALIAN = auto()
