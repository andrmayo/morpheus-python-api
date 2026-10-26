import subprocess
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from io import StringIO
from subprocess import CalledProcessError
from typing import cast

from morpheus_python_api.types import Language


def _build_cmd_args(
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
) -> list[str]:
    cmd_args = ["cruncher"]
    if language is Language.LATIN:
        cmd_args.append("-L")
    if language is Language.ITALIAN:
        cmd_args.append("-I")
    if non_strict_case:
        cmd_args.append("-S")
    if ignore_accents:
        cmd_args.append("-n")
    if database_format:
        cmd_args.append("-d")
    if ending_index:
        cmd_args.append("-e")
    if keep_beta_code:
        cmd_args.append("-k")
    if lemma:
        cmd_args.append("-l")
    if perseus_format_off:
        cmd_args.append("-P")
    if verbs_only:
        cmd_args.append("-V")

    return cmd_args


def _handle_crunch(
    input: str, stdout: bytes, stderr: bytes, returncode: int, cmd_args: list[str]
) -> str:
    output, error = stdout.decode(), stderr.decode()
    if returncode != 0:
        raise CalledProcessError(returncode, cmd_args, output, error)
    if len(output) == 0 and error == f"{input}\n":
        raise ValueError(f"Input could not be parsed:\n{input}\n{stderr}")
    if len(stdout) == 0:
        raise RuntimeError(
            f"Parsing failed for unclear reasons with cruncher stderr:\n{stderr}"
        )
    return output


async def async_crunch(
    input: str | StringIO,
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
    retry_ignoring_accents: bool = False,
) -> str:
    """Parses a single string using Morpheus. Unparsable inputs raise a ValueError. For meaning of arguments, see https://github.com/perseids-tools/morpheus#command-line-options. retry_ignoring_accents parses with accents and breathings initially, but if this fails, falls back to running as if ignore_accents = True."""
    if isinstance(input, StringIO):
        input = input.getvalue()
    # If you want to handle empty inputs gracefully, do so from the calling context
    if len(input) == 0:
        raise ValueError("Empty input cannot be parsed!")

    cmd_args = _build_cmd_args(
        language,
        non_strict_case,
        ignore_accents,
        database_format,
        ending_index,
        keep_beta_code,
        lemma,
        perseus_format_off,
        verbs_only,
    )

    proc = await create_subprocess_exec(
        *cmd_args,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await proc.communicate(input=input.encode("utf-8"))

    if (
        retry_ignoring_accents
        and stdout == 0
        and stderr == input
        and not ignore_accents
    ):
        cmd_args.append("-n")
        proc = await create_subprocess_exec(
            *cmd_args, stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await proc.communicate(input=input.encode("utf-8"))

    return _handle_crunch(input, stdout, stderr, cast(int, proc.returncode), cmd_args)


def crunch(
    input: str | StringIO,
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
    retry_ignoring_accents: bool = False,
) -> str:
    """Parses a single string using Morpheus. Unparsable inputs raise a ValueError. For meaning of arguments, see https://github.com/perseids-tools/morpheus#command-line-options. retry_ignoring_accents parses with accents and breathings initially, but if this fails, falls back to running as if ignore_accents = True."""
    if isinstance(input, StringIO):
        input = input.getvalue()
    # If you want to handle empty inputs gracefully, do so from the calling context
    if len(input) == 0:
        raise ValueError("Empty input cannot be parsed!")

    cmd_args = _build_cmd_args(
        language,
        non_strict_case,
        ignore_accents,
        database_format,
        ending_index,
        keep_beta_code,
        lemma,
        perseus_format_off,
        verbs_only,
    )

    result = subprocess.run(cmd_args, input=input.encode("utf-8"), capture_output=True)

    stdout, stderr = result.stdout, result.stderr

    if (
        retry_ignoring_accents
        and stdout == 0
        and stderr == input
        and not ignore_accents
    ):
        cmd_args.append("-n")
        result = subprocess.run(
            cmd_args, input=input.encode("utf-8"), capture_output=True
        )
        stdout, stderr = result.stdout, result.stderr

    return _handle_crunch(input, stdout, stderr, result.returncode, cmd_args)
