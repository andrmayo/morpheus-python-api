"""types.py
Module for any type and enum definitions useful across modules.
"""

from dataclasses import dataclass
from enum import auto, Enum, StrEnum
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


class POS(StrEnum):
    NOUN = "noun"
    VERB = "verb"
    ADJ = "adj"  # adjective
    ADV = "adv"  # adverb
    PREP = "prep"  # preposition
    PRON = "pron"  # pronoun
    CONJ = "conj"  # conjunction
    PART = "part"  # participle


class Case(StrEnum):
    NOM = "nom"  # nominative
    GEN = "gen"  # genitive
    DAT = "dat"  # dative
    ACC = "acc"  # accusative
    VOC = "voc"  # vocative
    ABL = "abl"  # ablative


class Num(StrEnum):
    SG = "sg"  # singular
    PL = "pl"  # plural
    DUAL = "dual"  # dual


class Gender(StrEnum):
    MASC = "masc"  # masculine
    FEM = "fem"  # feminine
    NEUT = "neut"  # neuter


class Tense(StrEnum):
    PRES = "pres"  # present
    IMPF = "impf"  # imperfect
    FUT = "fut"  # future
    AOR = "aor"  # aorist
    PERF = "perf"  # perfect
    PLUP = "pluperf"  # pluperfect
    FUTPERF = "futperf"  # future perfect


class Mood(StrEnum):
    IND = "ind"  # indicative
    SUBJ = "subj"  # subjunctive
    OPT = "opt"  # optative
    IMPERAT = "imperat"  # imperative
    INF = "inf"  # infinitive
    PART = "part"  # participle


class Voice(StrEnum):
    ACT = "act"  # active
    MID = "mid"  # middle
    PASS = "pass"  # passive
    MP = "mp"  # medio-passive


class Person(StrEnum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"


@dataclass
class Dialect:
    epic: bool = False
    ionic: bool = False
    doric: bool = False


# NOTE: It's important that field names for these dataclasses be lowercase
# since they're accessed at certainpoints by doing something like
# Tense.__name__.lower()
@dataclass
class MorphParse:
    # Since this class is part of the API
    # we want to store Greek text in utf-8
    # and convert to betacode when needed
    language: Language
    pos: POS
    vowel_forms: list[str] | None = None
    case: Case | None = None
    num: Num | None = None
    gender: Gender | None = None
    tense: Tense | None = None
    mood: Mood | None = None
    voice: Voice | None = None
    person: Person | None = None


@dataclass
class WordParse:
    lemma: str
    parses: list[MorphParse]
