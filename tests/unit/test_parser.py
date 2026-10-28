"""
test_parser.py

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


@pytest.mark.asyncio
async def test_async_crunch():
    result = [result async for result in async_crunch("lu/w")][0]
    assert result == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )

    with pytest.raises(ValueError):
        # accent is wrong
        result = [result async for result in async_crunch("luw/")][0]

    result = [
        result async for result in async_crunch("luw/", ignore_accents=True)
    ][0]
    assert result == (
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


def test_crunch():
    result = list(crunch("lu/w"))[0]
    assert result == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )

    with pytest.raises(ValueError):
        # accent is wrong
        result = list(crunch("luw/"))

    result = list(crunch("luw/", ignore_accents=True))[0]
    assert result == (
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


# with gener, when the input is malformed, it simply gets echoed to STDOUT
# when the lemma isn't found, @failed message gets sent to STDOUT and STDERR
# while the "Something wrong with stemkeys" line gets sent just to STDERR


@pytest.mark.asyncio
async def test_async_gen():
    result = await async_gen(":le:lo/gos\n:no:lo/g os_ou masc\n")
    assert result == (
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

    with pytest.raises(ValueError):
        # missing newline after the lemma :le:lo/gos
        result = await async_gen(":le:lo/gos:no:lo/g os_ou masc\n")


def test_gen():
    result = gen(":le:lo/gos\n:no:lo/g os_ou masc\n")
    assert result == (
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

    with pytest.raises(ValueError):
        # missing newline after the lemma :le:lo/gos
        result = gen(":le:lo/gos:no:lo/g os_ou masc\n")

    # result = gen(":")
