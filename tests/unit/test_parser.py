"""test_parser.py

Pytest tests for public functions in parser.py. The test cases also illustrate
the kind of input expected by Morpheus binaries. The fiddliest part to test is
that the functions throw the right exceptions for a given STDOUT and STDERR."""

# The tests aren't very DRY, but the workarounds given synchronous and
# asynchronous versions of the same function aren't worth the added complexity.

import pytest

from morpheus_python_api.parse.parser import (
    async_crunch,
    crunch,
    async_gen,
    gen,
)
from morpheus_python_api.types import (
    POS,
    Language,
    Mood,
    Num,
    Person,
    Tense,
    Voice,
    WordParse,
)


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
        assert not parse.case
        assert not parse.gender

    cur_form = word_parse.parses[0]
    assert cur_form.tense == Tense.PRES
    assert cur_form.mood == Mood.SUBJ
    assert cur_form.voice == Voice.ACT
    assert cur_form.person == Person.FIRST
    assert cur_form.num == Num.SG

    #     "luw/\n"
    #     "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #     "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres subj act 1st "
    #     "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres ind act 1st "
    #     "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres subj act 1st "
    #     "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres ind act 1st "
    #     "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  imperf ind mp 2nd "
    #     "sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
    # )


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
    # assert result[1] == (
    #     "luw/\n"
    #     "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #     "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
    #     "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres subj act 1st "
    #     "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres ind act 1st "
    #     "sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres subj act 1st "
    #     "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  pres ind act 1st "
    #     "sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
    #     "<NL>V luw=,lua/w  imperf ind mp 2nd "
    #     "sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
    # )


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
