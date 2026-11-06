"""test_parser.py

Pytest tests for public functions in parser.py. The test cases also illustrate
the kind of input expected by Morpheus binaries. The fiddliest part to test is
that the functions throw the right exceptions for a given STDOUT and STDERR."""

# The tests aren't very DRY, but the workarounds given synchronous and
# asynchronous versions of the same function aren't worth the added complexity.

from enum import StrEnum
import pytest

from betacode import beta_to_uni

from morpheus_python_api.parse.parser import (
    async_crunch,
    crunch,
    async_gen,
    gen,
)
from morpheus_python_api.types import (
    POS,
    Case,
    Deriv,
    Dialect,
    Feature,
    Gender,
    Language,
    Mood,
    Num,
    Person,
    StemType,
    Tense,
    Voice,
    WordParse,
)


def _in_frozen_set(
    field_values: str | StrEnum | list[str | StrEnum],
    fr_set: frozenset[str | StrEnum] | None,
):
    if not fr_set:
        return False
    if not isinstance(field_values, list):
        field_values = [field_values]
    return all(fv in fr_set for fv in field_values)


@pytest.mark.asyncio
async def test_async_crunch_raw():
    input_str = "lu/w"
    result = [
        result
        async for result in async_crunch(input_str, raw_cruncher_output=True)
    ][0]

    assert result[0] == input_str
    assert result[1] == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )

    input_str = "luw/"
    with pytest.raises(ValueError):
        # accent is wrong
        result = [
            result
            async for result in async_crunch(
                input_str, raw_cruncher_output=True
            )
        ][0]

    result = [
        result
        async for result in async_crunch(
            input_str, ignore_accents=True, raw_cruncher_output=True
        )
    ][0]

    assert result[0] == input_str
    assert result[1] == (
        "luw/\n"
        "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st "
        "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st "
        "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st "
        "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st "
        "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  imperf ind mp 2nd "
        "sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
    )


@pytest.mark.asyncio
async def test_async_crunch_structured():
    await _process_async_crunch_structured_greek_verb()
    await _process_async_crunch_structured_greek_noun()
    await _process_async_crunch_structured_greek_part()


async def _process_async_crunch_structured_greek_verb():
    input_str = "lu/w"
    result = [result async for result in async_crunch(input_str)][0]

    assert result[0] == input_str
    assert isinstance(result[1], WordParse)
    # assert result[1] == (
    #     "lu/w\n"
    #     "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    # )

    input_str = "luw/"
    with pytest.raises(ValueError):
        # accent is wrong
        result = [result async for result in async_crunch(input_str)][0]

    result = [
        result async for result in async_crunch(input_str, ignore_accents=True)
    ][0]
    assert result[0] == input_str

    word_parse = result[1]
    assert isinstance(word_parse, WordParse)
    assert word_parse.lemma == "λυώ"

    # things that whould hold for all parses of luw
    for parse in word_parse.parses:
        assert parse.language == Language.GREEK
        assert parse.pos == POS.VERB
        assert parse.case is None
        assert parse.gender is None

    cur_form = word_parse.parses[0]
    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.SUBJ, cur_form.mood),
            _in_frozen_set(Voice.ACT, cur_form.voice),
            _in_frozen_set(Person.FIRST, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set(Dialect.EPIC, cur_form.dialect),
            cur_form.dict_forms == [beta_to_uni("lu/w"), beta_to_uni("lu/w")],
        ]
    )

    assert cur_form.features is None
    assert cur_form.stem_type is StemType.W_STEM
    assert cur_form.deriv is Deriv.REG_CONJ

    cur_form = word_parse.parses[1]
    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.IND, cur_form.mood),
            _in_frozen_set(Voice.ACT, cur_form.voice),
            _in_frozen_set(Person.FIRST, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set(Dialect.EPIC, cur_form.dialect),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("lu/w"), beta_to_uni("lu/w")]

    assert cur_form.features is None
    assert cur_form.stem_type is StemType.W_STEM
    assert cur_form.deriv is Deriv.REG_CONJ

    cur_form = word_parse.parses[4]
    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.IMPERAT, cur_form.mood),
            _in_frozen_set(Voice.MP, cur_form.voice),
            _in_frozen_set(Person.SECOND, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("luw="), beta_to_uni("lua/w")]
    assert cur_form.dialect is None

    assert _in_frozen_set(Feature.CONTR, cur_form.features)
    assert cur_form.stem_type is StemType.AW_PR
    assert cur_form.deriv is Deriv.AW_DENOM

    cur_form = word_parse.parses[9]
    assert all(
        [
            _in_frozen_set(Tense.IMPERF, cur_form.tense),
            _in_frozen_set(Mood.IND, cur_form.mood),
            _in_frozen_set(Voice.MP, cur_form.voice),
            _in_frozen_set(Person.SECOND, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set([Dialect.HOMERIC, Dialect.IONIC], cur_form.dialect),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("luw="), beta_to_uni("lua/w")]

    assert _in_frozen_set(
        [Feature.CONTR, Feature.UNAUGMENTED], cur_form.features
    )
    assert cur_form.stem_type is StemType.AW_PR
    assert cur_form.deriv is Deriv.AW_DENOM

    # raw output of crunching luw/ ignoring accents:
    #  "luw/\n"
    #  "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #  "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #  "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #  "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #  "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
    #  "<NL>V luw=,lua/w  pres subj act 1st "
    #  "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #  "<NL>V luw=,lua/w  pres ind act 1st "
    #  "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #  "<NL>V luw=,lua/w  pres subj act 1st "
    #  "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #  "<NL>V luw=,lua/w  pres ind act 1st "
    #  "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #  "<NL>V luw=,lua/w  imperf ind mp 2nd "
    #  "sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"


async def _process_async_crunch_structured_greek_noun():
    input_str = "lo/gos"
    result = [result async for result in async_crunch(input_str)][0]
    assert result[0] == input_str
    word_parse = result[1]
    assert isinstance(word_parse, WordParse)
    assert word_parse.lemma == beta_to_uni(input_str)
    assert len(word_parse.parses) == 1

    morph_parse = word_parse.parses[0]

    assert all(
        [
            morph_parse.person is None,
            morph_parse.tense is None,
            morph_parse.voice is None,
            morph_parse.mood is None,
            morph_parse.dialect is None,
            morph_parse.features is None,
        ]
    )

    assert all(
        [
            _in_frozen_set(Gender.MASC, morph_parse.gender),
            _in_frozen_set(Case.NOM, morph_parse.case),
            _in_frozen_set(Num.SG, morph_parse.num),
        ]
    )


async def _process_async_crunch_structured_greek_part():
    input_str = "lu/ousa"
    result = [result async for result in async_crunch(input_str)][0]
    assert result[0] == input_str
    word_parse = result[1]
    assert isinstance(word_parse, WordParse)
    assert word_parse.lemma == beta_to_uni(input_str)
    assert len(word_parse.parses) == 1

    morph_parse = word_parse.parses[0]

    assert all(
        [
            morph_parse.person is None,
            morph_parse.tense is None,
            morph_parse.voice is None,
            morph_parse.mood is None,
            morph_parse.dialect is None,
            morph_parse.features is None,
        ]
    )

    assert all(
        [
            morph_parse.gender is Gender.MASC,
            morph_parse.case is Case.NOM,
            morph_parse.num is Num.SG,
        ]
    )


def test_crunch_structured():
    input_str = "lu/w"
    result = list(crunch(input_str))[0]

    assert result[0] == input_str
    assert isinstance(result[1], WordParse)

    input_str = "luw/"
    with pytest.raises(ValueError):
        # accent is wrong
        result = list(crunch(input_str))[0]

    result = list(crunch(input_str, ignore_accents=True))[0]

    assert result[0] == input_str
    assert isinstance(result[1], WordParse)

    word_parse = result[1]
    assert isinstance(word_parse, WordParse)
    assert word_parse.lemma == "λυώ"

    # things that whould hold for all parses of luw
    for parse in word_parse.parses:
        assert parse.language == Language.GREEK
        assert parse.pos == POS.VERB
        assert not parse.case
        assert not parse.gender

    cur_form = word_parse.parses[0]

    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.SUBJ, cur_form.mood),
            _in_frozen_set(Voice.ACT, cur_form.voice),
            _in_frozen_set(Person.FIRST, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set(Dialect.EPIC, cur_form.dialect),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("lu/w"), beta_to_uni("lu/w")]

    assert cur_form.features is None
    assert cur_form.stem_type is StemType.W_STEM
    assert cur_form.deriv is Deriv.REG_CONJ

    cur_form = word_parse.parses[1]
    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.IND, cur_form.mood),
            _in_frozen_set(Voice.ACT, cur_form.voice),
            _in_frozen_set(Person.FIRST, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set(Dialect.EPIC, cur_form.dialect),
        ]
    )

    assert cur_form.dict_forms == [beta_to_uni("lu/w"), beta_to_uni("lu/w")]
    assert cur_form.features is None
    assert cur_form.stem_type is StemType.W_STEM
    assert cur_form.deriv is Deriv.REG_CONJ

    cur_form = word_parse.parses[4]
    assert all(
        [
            _in_frozen_set(Tense.PRES, cur_form.tense),
            _in_frozen_set(Mood.IMPERAT, cur_form.mood),
            _in_frozen_set(Voice.MP, cur_form.voice),
            _in_frozen_set(Person.SECOND, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("luw="), beta_to_uni("lua/w")]

    assert cur_form.dialect is None
    assert _in_frozen_set(Feature.CONTR, cur_form.features)
    assert cur_form.stem_type is StemType.AW_PR
    assert cur_form.deriv is Deriv.AW_DENOM

    cur_form = word_parse.parses[9]
    assert all(
        [
            _in_frozen_set(Tense.IMPERF, cur_form.tense),
            _in_frozen_set(Mood.IND, cur_form.mood),
            _in_frozen_set(Voice.MP, cur_form.voice),
            _in_frozen_set(Person.SECOND, cur_form.person),
            _in_frozen_set(Num.SG, cur_form.num),
            _in_frozen_set([Dialect.HOMERIC, Dialect.IONIC], cur_form.dialect),
        ]
    )
    assert cur_form.dict_forms == [beta_to_uni("luw="), beta_to_uni("lua/w")]
    assert _in_frozen_set(
        [Feature.CONTR, Feature.UNAUGMENTED], cur_form.features
    )
    assert cur_form.stem_type is StemType.AW_PR
    assert cur_form.deriv is Deriv.AW_DENOM

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


def test_italian_crunch():
    input_str = "amando"
    result = list(crunch(input_str, language=Language.ITALIAN))[0]
    assert result[0] == input_str
    assert isinstance(result[1], WordParse)
    assert len(result[1].parses) == 1

    morph_parse = result[1].parses[0]
    assert all(
        [
            morph_parse.dict_forms == ["amare"],
            morph_parse.pos is POS.VERB,
            _in_frozen_set(Tense.GERUNDIVE, morph_parse.tense),
            _in_frozen_set(Mood.GERUNDIVE, morph_parse.mood),
            _in_frozen_set(Gender.MASC, morph_parse.gender),
        ]
    )

    # <NL>V amare  gerundive masc sg\t\t\tconj1,are_vb</NL>


@pytest.mark.asyncio
async def test_async_gen():
    input_str = ":le:lo/gos\n:no:lo/g os_ou masc"
    result = [result async for result in async_gen(input_str)][0]

    assert result[0] == input_str
    assert result[1] == (
        "\n:le:lo/gos\n"
        "<G>lo/gos</G>  os_ou masc nom sg\n"
        "<G>lo/gou</G>  os_ou masc gen sg\n"
        "<G>lo/gw</G>  os_ou masc gen sg doric aeolic\n"
        "<G>lo/goio</G>  os_ou masc gen sg epic\n"
        "<G>lo/gw|</G>  os_ou masc dat sg\n"
        "<G>lo/gon</G>  os_ou masc acc sg\n"
        "<G>lo/ge</G>  os_ou masc voc sg\n"
        "<G>lo/goi</G>  os_ou masc nom/voc pl\n"
        "<G>lo/gwn</G>  os_ou masc gen pl\n"
        "<G>lo/gois</G>  os_ou masc dat pl\n"
        "<G>lo/gofi</G>  os_ou masc dat pl epic\n"
        "<G>lo/goisin</G>  os_ou masc dat pl epic ionic aeolic nu_movable\n"
        "<G>lo/goisi</G>  os_ou masc dat pl epic ionic aeolic\n"
        "<G>lo/gous</G>  os_ou masc acc pl\n"
        "<G>lo/gws</G>  os_ou masc acc pl doric\n"
        ":no:lo/g os_ou masc\n"
    )

    with pytest.raises(ValueError, match=r"(?i)specified"):
        # missing newline after the lemma :le:lo/gos
        result = [result async for result in async_gen(":le:lo/gos:no:lo/g")][0]

    with pytest.raises(ValueError, match=r"(?i)garbage"):
        # missing newline after the lemma :le:lo/gos
        result = [result async for result in async_gen("some junk")][0]

    with pytest.raises(ValueError, match=r"(?i)stem"):
        result = [result async for result in async_gen(":no:lo/g bogus")][0]


def test_gen():
    input_str = ":le:lo/gos\n:no:lo/g os_ou masc"
    result = list(gen(input_str))[0]

    assert result[0] == input_str
    assert result[1] == (
        "\n:le:lo/gos\n"
        "<G>lo/gos</G>  os_ou masc nom sg\n"
        "<G>lo/gou</G>  os_ou masc gen sg\n"
        "<G>lo/gw</G>  os_ou masc gen sg doric aeolic\n"
        "<G>lo/goio</G>  os_ou masc gen sg epic\n"
        "<G>lo/gw|</G>  os_ou masc dat sg\n"
        "<G>lo/gon</G>  os_ou masc acc sg\n"
        "<G>lo/ge</G>  os_ou masc voc sg\n"
        "<G>lo/goi</G>  os_ou masc nom/voc pl\n"
        "<G>lo/gwn</G>  os_ou masc gen pl\n"
        "<G>lo/gois</G>  os_ou masc dat pl\n"
        "<G>lo/gofi</G>  os_ou masc dat pl epic\n"
        "<G>lo/goisin</G>  os_ou masc dat pl epic ionic aeolic nu_movable\n"
        "<G>lo/goisi</G>  os_ou masc dat pl epic ionic aeolic\n"
        "<G>lo/gous</G>  os_ou masc acc pl\n"
        "<G>lo/gws</G>  os_ou masc acc pl doric\n"
        ":no:lo/g os_ou masc\n"
    )

    with pytest.raises(ValueError, match=r"(?i)specified"):
        # missing newline after the lemma :le:lo/gos
        result = list(gen(":le:lo/gos:no:lo/g"))[0]

    with pytest.raises(ValueError, match=r"(?i)garbage"):
        # missing newline after the lemma :le:lo/gos
        result = list(gen("some junk"))[0]

    with pytest.raises(ValueError, match=r"(?i)stem"):
        result = list(gen(":no:lo/g bogus"))[0]
