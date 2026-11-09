"""models.py

Module for Pydantic models.
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict

from morpheus_python_api.types import Language, WordParse


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
    raw_cruncher_output: bool = False


# envelopes for parse objects
class CrunchMsg(BaseModel):
    type: Literal["structured", "raw"]
    word: str
    parse: str | WordParse


class ErrorMsg(BaseModel):
    type: Literal["unparsed", "runtime", "validation", "other"]
    word: str | None = None
    detail: str
