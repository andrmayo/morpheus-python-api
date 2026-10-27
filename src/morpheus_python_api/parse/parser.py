"""parser
parser.py

This module provides thin synchronous and asynchronous wrappers around the
Morpheus binaries cruncher, gener, and pname. The gener and pname binaries have
less functionality, and are not well-documented in the perseids-tools codebase.
"""

import subprocess
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from io import StringIO
from os import environ
from subprocess import CalledProcessError
from typing import cast

from morpheus_python_api.config import bin_path, morphlib_path
from morpheus_python_api.types import Language


def _build_env() -> dict[str, str]:
    env = environ.copy()
    env["MORPHLIB"] = env.get("MORPHLIB") or str(morphlib_path())
    env["BIN_PATH"] = env.get("BIN_PATH") or str(bin_path())
    return env


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
) -> tuple[list[str], dict[str, str]]:
    env = _build_env()
    cur_bin_path = env["BIN_PATH"]
    cmd_args = [f"{cur_bin_path}/cruncher"]
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

    return cmd_args, env


def _handle_crunch(
    input_str: str,
    stdout: bytes,
    stderr: bytes,
    returncode: int,
    cmd_args: list[str],
) -> str:
    output_str, error = stdout.decode(), stderr.decode()
    if returncode != 0:
        raise CalledProcessError(returncode, cmd_args, output_str, error)
    if len(output_str) == 0 and error == f"{input_str}\n":
        raise ValueError(f"input_str could not be parsed:\n{input}\n{stderr}")
    if len(stdout) == 0:
        raise RuntimeError(
            "Parsing failed for unclear reasons with cruncher. "
            f"stderr:\n{stderr}"
        )
    return output_str


async def async_crunch(
    input_str: str | StringIO,
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
    """Parses a single string using Morpheus. Unparsable input_strs raise a
    ValueError. For meaning of arguments, see
    https://github.com/perseids-tools/morpheus#command-line-options.
    retry_ignoring_accents parses with accents and breathings initially, but if
    this fails, falls back to running as if ignore_accents = True."""
    if isinstance(input_str, StringIO):
        input_str = input_str.getvalue()
    # If you want to handle empty input_str gracefully, do so from caller
    if len(input_str) == 0:
        raise ValueError("Empty input_str cannot be parsed!")

    cmd_args, env = _build_cmd_args(
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
        env=env,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await proc.communicate(input=input_str.encode("utf-8"))

    if (
        retry_ignoring_accents
        and stdout == 0
        and stderr == input_str
        and not ignore_accents
    ):
        cmd_args.append("-n")
        proc = await create_subprocess_exec(
            *cmd_args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=_build_env()
        )
        stdout, stderr = await proc.communicate(input=input_str.encode("utf-8"))

    return _handle_crunch(
        input_str, stdout, stderr, cast(int, proc.returncode), cmd_args
    )


def crunch(
    input_str: str | StringIO,
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
    """Parses a single string using Morpheus. Unparsable input_strs raise a
    ValueError. For meaning of arguments, see
    https://github.com/perseids-tools/morpheus#command-line-options.
    retry_ignoring_accents parses with accents and breathings initially, but if
    this fails, falls back to running as if ignore_accents = True."""
    if isinstance(input_str, StringIO):
        input_str = input_str.getvalue()
    # If you want to handle empty input_strs gracefully, do so from caller
    if len(input_str) == 0:
        raise ValueError("Empty input_str cannot be parsed!")

    cmd_args, env = _build_cmd_args(
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

    result = subprocess.run(
        cmd_args,
        env=env,
        input=input_str.encode("utf-8"),
        capture_output=True,
        check=False,
    )

    stdout, stderr = result.stdout, result.stderr

    if (
        retry_ignoring_accents
        and stdout == 0
        and stderr == input_str
        and not ignore_accents
    ):
        cmd_args.append("-n")
        result = subprocess.run(
            cmd_args,
            env=env,
            input=input_str.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        stdout, stderr = result.stdout, result.stderr

    return _handle_crunch(
        input_str, stdout, stderr, result.returncode, cmd_args
    )


def _handle_gen(
    input_str: str,
    stdout: bytes,
    stderr: bytes,
    returncode: int,
    cmd_args: list[str],
) -> str:
    output_str, error = stdout.decode(), stderr.decode()
    if returncode != 0:
        raise CalledProcessError(returncode, cmd_args, output_str, error)
    if len(output_str) == len(input_str):
        raise ValueError(
            "input_str is malformed.\n"
            f"input_str:\n{input}\nstdout:{stdout}\nstderr:{stderr}\n{stderr}"
        )
    if len(error) > 0:
        raise ValueError(
            "Lemma not found.\n"
            f"input_str:\n{input}\nstdout:{stdout}\nstderr:{stderr}\n{stderr}"
        )
    if len(stdout) == 0:
        raise RuntimeError(
            "Parsing failed for unclear reasons.\n"
            f"input_str:\n{input}\nstdout:{stdout}\nstderr:{stderr}\n{stderr}"
        )
    return output_str


async def async_gen(
    input_str: str | StringIO,
) -> str:
    """Generates a parse table from a lemma using Morpheus.
    Unparsable input_strs raise a ValueError."""
    if isinstance(input_str, StringIO):
        input_str = input_str.getvalue()
    # If you want to handle empty input_strs gracefully, do so from caller
    if len(input_str) == 0:
        raise ValueError("Empty input_str cannot be parsed!")

    env = _build_env()
    cur_bin_path = env["BIN_PATH"]
    cmd_args = [f"{cur_bin_path}/gener"]

    proc = await create_subprocess_exec(
        *cmd_args,
        env=env,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await proc.communicate(input=input_str.encode("utf-8"))

    return _handle_gen(
        input_str, stdout, stderr, cast(int, proc.returncode), cmd_args
    )


def gen(
    input_str: str | StringIO,
) -> str:
    """Generates a parse table from a lemma using Morpheus.
    Unparsable input_strs raise a ValueError."""
    if isinstance(input_str, StringIO):
        input_str = input_str.getvalue()
    # If you want to handle empty input_strs gracefully, do so from caller
    if len(input_str) == 0:
        raise ValueError("Empty input_str cannot be parsed!")

    env = _build_env()
    cur_bin_path = env["BIN_PATH"]
    cmd_args = [f"{cur_bin_path}/gener"]

    result = subprocess.run(
        cmd_args,
        env=env,
        input=input_str.encode("utf-8"),
        capture_output=True,
        check=False,
    )

    stdout, stderr = result.stdout, result.stderr

    return _handle_gen(input_str, stdout, stderr, result.returncode, cmd_args)
