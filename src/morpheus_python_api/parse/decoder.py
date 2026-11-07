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
    Case,
    Degree,
    Deriv,
    Dialect,
    Feature,
    Gender,
    Language,
    Mood,
    MorphParse,
    Num,
    Person,
    StemType,
    Tense,
    Voice,
    WordParse,
)


# We need gender because Italian gerundives are parsed as verbs
_VERB_PARSE_STACK = [
    Num,
    Person,
    Degree,
    Case,
    Voice,
    Gender,
    Mood,
    Tense,
    "dict_forms",
]
_NOUN_PARSE_STACK = [Num, Degree, Person, Case, Gender, "dict_forms"]
_PART_PARSE_STACK = [Num, Case, Gender, Voice, Mood, Tense, "dict_forms"]


def _split_by_first_tab(input_str: str) -> tuple[str, str]:
    pre_tab, post_tab = input_str.split("\t", 1)
    return pre_tab, post_tab


def _iter_parses(input_str: str) -> Iterator[str]:
    for parse in input_str.split(r"</NL>"):
        yield parse[4:]


def _set_morphparse_field(
    parse: MorphParse, word_part: type[StrEnum], component: list[str]
) -> None:
    fields = []
    for fieldname in component:
        # special logic for Latin/Italian gerundive, which covers mood and tense
        if fieldname == "gerundive":
            assert word_part is Tense
            parse.tense = frozenset((Tense.GERUNDIVE,))
            parse.mood = frozenset((Mood.GERUNDIVE,))
            return
        # same logic for Latin supline
        if fieldname == "supine":
            assert word_part is Tense
            parse.tense = frozenset((Tense.SUPINE,))
            parse.mood = frozenset((Mood.SUPINE,))
            return
        fields.append(word_part(fieldname))

    setattr(parse, word_part.__name__.lower(), frozenset(fields))


def _convert_morpheus_tag(tag: str) -> list[str]:
    # these conditionals need to include all the instances where Morpheus
    # notation differs the relevant StrEnum value in types.py
    if tag == "1st":
        return ["first"]
    if tag == "2nd":
        return ["second"]
    if tag == "3rd":
        return ["third"]
    # this also handle alternatives, e.g. nom/voc
    return tag.split("/")


def _process_extra_fields(morph_parse: MorphParse, extra_fields: str) -> None:
    fields = extra_fields.split("\t")
    assert len(fields) == 3
    dialects = fields[0].split()
    features = fields[1].split()
    stem_deriv = [f for f in fields[2].split(",") if len(f)]

    if len(dialects):
        morph_parse.dialect = frozenset(Dialect(dial) for dial in dialects)

    if len(features):
        morph_parse.features = frozenset(Feature(feat) for feat in features)

    assert 0 < len(stem_deriv) < 3
    if len(stem_deriv) > 0:
        stem = stem_deriv[0]
        morph_parse.stem_type = StemType(stem)
    if len(stem_deriv) > 1:
        deriv = stem_deriv[1]
        morph_parse.deriv = Deriv(deriv)


# NOTE: Dispatch to _decode_verb, _decode_noun etc. is not very DRY
# at the moment, but it's worth keeping for now in case more custom
# logic is needed for a given POS
def _decode_verb(
    input_str: str, language: Language, keep_betacode: bool
) -> MorphParse:
    main_fields, extra_fields = _split_by_first_tab(input_str)

    verb_parse_fields = _VERB_PARSE_STACK.copy()
    parse_components = main_fields.split()
    parse_components.reverse()
    # Remove POS tag
    parse_components.pop()
    morph_parse = MorphParse(language, POS.VERB)
    while parse_components and verb_parse_fields:
        component = _convert_morpheus_tag(parse_components.pop())
        # special case: adverbial
        if component[0] == "adverbial":
            morph_parse.adverbial = True
            if len(component) > 1:
                parse_components.append("/".join(component[1:]))
            continue

        # Special case: when short-vowel and long-vowel forms are given
        # Since tense has to follow these forms when they're present, we can
        # check for a tense
        if (
            verb_parse_fields[-1] == "dict_forms"
            and component[0] not in Tense.__members__.values()
            and component[0] not in Gender.__members__.values()
        ):
            # _convert_morpheus_tag will erroneously split
            # dict_forms
            component = "/".join(component)
            morph_parse.dict_forms = [
                beta_to_uni(form)
                if (language is Language.GREEK and not keep_betacode)
                else form
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
            and component[0]
            not in cast(
                type[StrEnum], verb_parse_fields[-1]
            ).__members__.values()
        ):
            verb_parse_fields.pop()
        if verb_parse_fields:
            # these are assumed to be lower case
            verb_part = verb_parse_fields.pop()
            _set_morphparse_field(morph_parse, verb_part, component)

    _process_extra_fields(morph_parse, extra_fields)
    return morph_parse


def _decode_noun(
    input_str: str, language: Language, keep_betacode: bool
) -> MorphParse:
    main_fields, extra_fields = _split_by_first_tab(input_str)

    noun_parse_fields = _NOUN_PARSE_STACK.copy()
    parse_components = main_fields.split()
    parse_components.reverse()
    # Remove POS tag
    parse_components.pop()
    morph_parse = MorphParse(language, POS.NOUN)

    while parse_components and noun_parse_fields:
        component = _convert_morpheus_tag(parse_components.pop())
        # Special case: when short-vowel and long-vowel forms are given
        # Since tense has to follow these forms when they're present, we can
        # check for a tense
        if (
            noun_parse_fields[-1] == "dict_forms"
            and component[0] not in Gender.__members__.values()
            and component[0] not in Tense.__members__.values()
        ):
            # _convert_morpheus_tag will erroneously split
            # dict_forms
            component = "/".join(component)
            morph_parse.dict_forms = [
                beta_to_uni(form)
                if (language is Language.GREEK and not keep_betacode)
                else form
                for form in component.split(",")
            ]
            noun_parse_fields.pop()
            continue
        # Any special tags should be processed before this point and the loop
        # should be continued
        assert (not noun_parse_fields) or hasattr(
            noun_parse_fields[-1], "__members__"
        )
        while (
            noun_parse_fields
            and component[0]
            not in cast(
                type[StrEnum], noun_parse_fields[-1]
            ).__members__.values()
        ):
            noun_parse_fields.pop()
        if noun_parse_fields:
            # these are assumed to be lower case
            noun_part = noun_parse_fields.pop()
            _set_morphparse_field(morph_parse, noun_part, component)

    _process_extra_fields(morph_parse, extra_fields)
    return morph_parse


# For participles
def _decode_part(
    input_str: str, language: Language, keep_betacode: bool
) -> MorphParse:
    main_fields, extra_fields = _split_by_first_tab(input_str)

    part_parse_fields = _PART_PARSE_STACK.copy()
    parse_components = main_fields.split()
    parse_components.reverse()
    # Remove POS tag
    parse_components.pop()
    morph_parse = MorphParse(language, POS.PART)
    while parse_components and part_parse_fields:
        component = _convert_morpheus_tag(parse_components.pop())
        # Special case: when short-vowel and long-vowel forms are given
        # Since tense has to follow these forms when they're present, we can
        # check for a tense
        if (
            part_parse_fields[-1] == "dict_forms"
            and component[0] not in Tense.__members__.values()
        ):
            # _convert_morpheus_tag will erroneously split
            # dict_forms
            component = "/".join(component)
            morph_parse.dict_forms = [
                beta_to_uni(form)
                if (language is Language.GREEK and not keep_betacode)
                else form
                for form in component.split(",")
            ]
            part_parse_fields.pop()
            continue
        # Any special tags should be processed before this point and the loop
        # should be continued
        assert (not part_parse_fields) or hasattr(
            part_parse_fields[-1], "__members__"
        )
        while (
            part_parse_fields
            and component[0]
            not in cast(
                type[StrEnum], part_parse_fields[-1]
            ).__members__.values()
        ):
            part_parse_fields.pop()
        if part_parse_fields:
            # these are assumed to be lower case
            part_part = part_parse_fields.pop()
            _set_morphparse_field(morph_parse, part_part, component)

    _process_extra_fields(morph_parse, extra_fields)
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
            word_parse.parses.append(
                _decode_verb(parse, language, keep_betacode)
            )
        elif parse[0] == "N":
            word_parse.parses.append(
                _decode_noun(parse, language, keep_betacode)
            )
        elif parse[0] == "P":
            word_parse.parses.append(
                _decode_part(parse, language, keep_betacode)
            )
        else:
            raise ValueError(f"POS not recognized, with POS input {parse[0]}")
    return word_parse
