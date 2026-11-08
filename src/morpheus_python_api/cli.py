"""cli.py
Typer cli for morpheus.

The main goal here is the mirror the CLI of the morpheus C application itself,
but in a Python package that's easy to install. To avoid conflicts with any
Morpheus binaries that have been installed, we have `morpheus cruncher` instead
of `cruncher`, and `morpheus gener` instead of `gener`.
"""

import sys
from contextlib import ExitStack
from pathlib import Path
from typing import Annotated

from typer import Argument, BadParameter, echo, Option, Typer

from morpheus_python_api.parse.parser import crunch, gen
from morpheus_python_api.types import Language

cli = Typer()
morpheus_cli = Typer()
cli.add_typer(morpheus_cli, name="morpheus")


@morpheus_cli.command("cruncher")
def morpheus_cruncher(
    cruncher_input: Annotated[str, Argument()] = "-",
    read_file: Annotated[
        bool, Option("--file", "-f", help="Read lines from a file as input.")
    ] = False,
    latin: Annotated[
        bool, Option("--Latin", "-L", help="Set language to Latin.")
    ] = False,
    italian: Annotated[
        bool, Option("--Italian", "-I", help="Set language to Italian.")
    ] = False,
    non_strict_case: Annotated[
        bool,
        Option(
            "--Strict",
            "-S",
            help="Turn off Strict case. For Greek, this allows words with an "
            "initial capital to be recognized. For languages in the Roman "
            "alphabet, allows words with initial capital or in all "
            "capitals.",
        ),
    ] = False,
    ignore_accents: Annotated[
        bool, Option("--ignore_accents", "-n", help="Ignore accents.")
    ] = False,
    database_format: Annotated[
        bool,
        Option(
            "--database_format",
            "-d",
            help="Database format. This switch changes the output from "
            "'Perseus format' to 'database format.' Output appears in a series "
            "of tagged fields.",
        ),
    ] = False,
    ending_index: Annotated[
        bool,
        Option(
            "--ending_index",
            "-e",
            help="Ending index. Instead of showing the analysis in readable "
            "form, this switch gives the indices of the tense, mood, case, "
            "number, and so on (as appropriate) in the internal tables.",
        ),
    ] = False,
    keep_beta_code: Annotated[
        bool,
        Option(
            "--keep_beta_code",
            "-k",
            help="Keep beta-code. When 'Perseus format' is enabled (the "
            "default), this switch does nothing. When 'Perseus format' "
            "is off, output (Greek as well as Latin) is converted to the "
            "old Greek Keys encoding. This switch disables that conversion "
            "so that Greek output stays in beta-code.",
        ),
    ] = False,
    lemma: Annotated[
        bool,
        Option(
            "--lemma",
            "-l",
            help="Show lemma. When this switch is set, instead of printing the "
            "entire analysis, cruncher will only show the lemma or headword "
            "from which the given form is made.",
        ),
    ] = False,
    perseus_format_off: Annotated[
        bool,
        Option(
            "--perseus_format_off",
            "-P",
            help=r"Turn off Perseus format. Output will be in the form "
            r"$feminam& is^M &from$ femina^M $fe\_minam^M "
            r"[&stem $fe\_min-& ]^M & a\_ae fem acc sg^M. Note the returns, "
            r"without line feeds, between the fields.",
        ),
    ] = False,
    verbs_only: Annotated[
        bool, Option("--verbs_only", "-V", help="Analyze verbs only.")
    ] = False,
):
    if latin and italian:
        raise BadParameter("Options --Latin and --Italian both passed.")
    if latin:
        language = Language.LATIN
    elif italian:
        language = Language.ITALIAN
    else:
        language = Language.GREEK

    with ExitStack() as stack:
        if cruncher_input == "-":
            if sys.stdin.isatty():
                raise BadParameter(
                    "Provide an argument or pipe input to stdin."
                )
            inputs = sys.stdin
        elif read_file:
            file_path = Path(cruncher_input)
            if not file_path.is_file():
                raise BadParameter(
                    "Got -f flag, but input is not a valid filename."
                )
            inputs = stack.enter_context(open(file_path, encoding="utf-8"))
        else:
            inputs = cruncher_input.split()

        for output in crunch(
            inputs,
            language,
            non_strict_case,
            ignore_accents,
            database_format,
            ending_index,
            keep_beta_code,
            lemma,
            perseus_format_off,
            verbs_only,
            raise_on_failure=False,
            raw_cruncher_output=True,
        ):
            echo(output[1], nl=False)


@morpheus_cli.command("gener")
def morpheus_gener(input_str: str):
    for output in gen(input_str):
        echo(output[1], nl=False)
