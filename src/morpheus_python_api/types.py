"""types.py
Module for any type and enum definitions useful across modules.
"""

from enum import auto, Enum
from pydantic import BaseModel, ConfigDict


class Language(Enum):
    GREEK = auto()
    LATIN = auto()
    ITALIAN = auto()


class CrunchOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: Language = Language.GREEK
    non_strict_case: bool = False
    ignore_accents: bool = False
    database_format: bool = False
    ending_index: bool = False
    keep_beta_code: bool = False
    lemma: bool = False
    perseus_format_off: bool = False
    verbs_only: bool = False
    raise_on_failure: bool = True
