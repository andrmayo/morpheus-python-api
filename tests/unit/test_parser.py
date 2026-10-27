import pytest

from morpheus_python_api.parse.parser import async_crunch, crunch, async_gen, gen


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


# when the input is malformed, it simply gets echoed to STDOUT
# when the lemma isn't found, @failed message gets sent to STDOUT and STDERR
# while the "Something wrong with stemkeys" line gets sent just to STDERR


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
