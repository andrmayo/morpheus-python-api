import pytest

from morpheus_python_api.parse.parser import async_crunch, crunch


@pytest.mark.asyncio
async def test_async_crunch():
    result = await async_crunch("lu/w")
    assert result == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )

    with pytest.raises(ValueError):
        # accent is wrong
        result = await async_crunch("luw/")

    result = await async_crunch("luw/", ignore_accents=True)
    assert result == (
        "luw/\n"
        "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  imperf ind mp 2nd sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
    )


def test_crunch():
    result = crunch("lu/w")
    assert result == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )

    with pytest.raises(ValueError):
        # accent is wrong
        result = crunch("luw/")

    result = crunch("luw/", ignore_accents=True)
    assert result == (
        "luw/\n"
        "<NL>V lu/w,lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w,lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V luw=,lua/w  pres imperat mp 2nd sg\t\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st sg\tattic epic ionic\tcontr\taw_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres subj act 1st sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  pres ind act 1st sg\tattic epic doric ionic\tcontr\tew_pr,aw_denom</NL>"
        "<NL>V luw=,lua/w  imperf ind mp 2nd sg\thomeric ionic\tcontr unaugmented\taw_pr,aw_denom</NL>\n"
    )
