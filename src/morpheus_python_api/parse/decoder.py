"""decoder.py
Functions for converting raw Morpheus binary outputs in betacode into structured
data.
"""

from collections.abc import Iterator
from enum import StrEnum
from typing import cast

from betacode import beta_to_uni

from morpheus_python_api.types import (
    POS,
    Language,
    Mood,
    MorphParse,
    Num,
    Person,
    Tense,
    Voice,
    WordParse,
)


_VERB_PARSE_STACK = [Num, Person, Voice, Mood, Tense, "vowel_forms"]


def _iter_parses(input_str: str) -> Iterator[str]:
    for parse in input_str.split(r"</NL>"):
        yield parse[4:]


def _set_morphparse_field(
    parse: MorphParse, word_part: type[StrEnum], fieldname: str
):
    setattr(parse, word_part.__name__.lower(), word_part(fieldname))


def _convert_morpheus_tag(tag: str) -> str:
    # these conditionals need to include all the instances where Morpheus
    # notation differs the relevant StrEnum value in types.py
    if tag == "1st":
        return "first"
    if tag == "2nd":
        return "second"
    if tag == "3rd":
        return "third"
    return tag


def _decode_greek_verb(input_str: str, keep_betacode: bool) -> MorphParse:
    verb_parse_fields = _VERB_PARSE_STACK.copy()
    parse_components = input_str.split()
    parse_components.reverse()
    # Remove POS tag
    parse_components.pop()
    morph_parse = MorphParse(Language.GREEK, POS.VERB)
    while parse_components and verb_parse_fields:
        component = _convert_morpheus_tag(parse_components.pop())
        # Special case: when short-vowel and long-vowel forms are given
        # Since tense has to follow these forms when they're present, we can
        # check for a tense
        if (
            verb_parse_fields[-1] == "vowel_forms"
            and component not in Tense.__members__.values()
        ):
            morph_parse.vowel_forms = [
                beta_to_uni(form) if keep_betacode else form
                for form in component.split(",")
            ]
            verb_parse_fields.pop()
            continue
        # Any special tags should be processed before this point and the loop
        # should be continued
        assert (not verb_parse_fields) or hasattr(
            verb_parse_fields[-1], "__members__"
        )
        while (
            verb_parse_fields
            and component
            not in cast(
                type[StrEnum], verb_parse_fields[-1]
            ).__members__.values()
        ):
            verb_parse_fields.pop()
        if verb_parse_fields:
            # these are assumed to be lower case
            verb_part = verb_parse_fields.pop()
            _set_morphparse_field(morph_parse, verb_part, component)
        else:
            # keep last component for processing less standard data
            parse_components.append(component)

    # TODO: process less standard data, e.g. dialect information
    return morph_parse


def decode_crunch(
    input_str: str, language: str | Language, keep_betacode: bool = False
) -> WordParse:
    if isinstance(language, str):
        language = language.lower()
        if language == "greek" or language == "g":
            language = Language.GREEK
        elif language == "latin" or language == "l":
            language = Language.LATIN
        elif language == "italian" or language == "i":
            language = Language.ITALIAN
        else:
            raise ValueError(
                f"Language should be greek, latin, or italian, got {language}."
            )
    # crunches end with a new line, but might as well strip all whitespace
    input_str = input_str.strip()[:-5]  # drop final <\NL>
    lemma, input_str = input_str.split("\n", 1)
    lemma = lemma if keep_betacode else beta_to_uni(lemma)
    # TODO: assume greek verb for now
    word_parse = WordParse(lemma, [])
    for parse in _iter_parses(input_str):
        if parse[0] == "V":
            word_parse.parses.append(_decode_greek_verb(parse, keep_betacode))
    return word_parse

    # "luw/\n"
    # "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    # "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    # "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
    # "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
    # "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
    # "<NL>V luw=,lua/w  pres subj act 1st "
    # "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    # "<NL>V luw=,lua/w  pres ind act 1st "
    # "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    # "<NL>V luw=,lua/w  pres subj act 1st "
    # "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    # "<NL>V luw=,lua/w  pres ind act 1st "
    # "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    # "<NL>V luw=,lua/w  imperf ind mp 2nd "
    # "sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
