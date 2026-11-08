"""test_cli.py

Pytest tests for the Typer cli.

These tests also indirectly test some of the streaming functionality in
`parser.py` that isn't really probed in test_parser.py."""

from typer.testing import CliRunner

from morpheus_python_api.cli import cli

runner = CliRunner()


def test_morpheus_cruncher():
    result = runner.invoke(cli, ["morpheus", "cruncher", "lu/w"])
    assert result.exit_code == 0
    assert result.stdout == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>\n"
    )


def test_morpheus_cruncher_stream_stdin():
    result = runner.invoke(
        cli, ["morpheus", "cruncher", "-"], input="lu/w\nluw/\nlo/gos\n"
    )
    assert result.exit_code == 0
    parses = result.stdout.split("\n")[:-1]
    parses = [
        "\n".join([parses[0], parses[1]]),
        parses[2],
        "\n".join([parses[3], parses[4]]),
    ]
    print(f"{parses=}")
    assert parses[0] == (
        "lu/w\n"
        "<NL>V lu/w  pres subj act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu/w  pres ind act 1st sg\tepic\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres subj act 1st sg\t\t\tw_stem,reg_conj</NL>"
        "<NL>V lu_/w,lu/w  pres ind act 1st sg\t\t\tw_stem,reg_conj</NL>"
    )
    assert parses[1] == "luw/"


def test_morpheus_gener():
    input_str = ":le:lo/gos\n:no:lo/g os_ou masc"
    result = runner.invoke(cli, ["morpheus", "gener", input_str])

    output = result.stdout
    assert output == (
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
