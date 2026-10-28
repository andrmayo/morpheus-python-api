"""parser
parser.py

This module provides thin synchronous and asynchronous wrappers around the
Morpheus binaries cruncher, gener, and pname. The gener and pname binaries have
less functionality, and are not well-documented in the perseids-tools codebase.
"""

import subprocess
from asyncio import StreamReader, create_subprocess_exec, StreamWriter
from asyncio.subprocess import PIPE
from collections.abc import AsyncIterator, Iterator
from io import StringIO, BufferedReader
from os import environ
from subprocess import CalledProcessError
from typing import cast

from morpheus_python_api.config import bin_path, morphlib_path
from morpheus_python_api.types import Language

# sentinel value for end of input
_SENTINEL = "@@@@"
# for identifying end of input
_END = f"{_SENTINEL}\n".encode("utf-8")


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
    # the stdbuff part is to disable buffering, which lets us stream
    cmd_args = ["stdbuf", "-o0", "-e0", f"{cur_bin_path}/cruncher"]
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
    input_str,
    buffer: bytes,
    # output is either the STDOUT and STDERR bytes,
    # or a selector.select() object
    raise_on_failure: bool,
) -> str:
    # NOTE: It might be worth logging stderr when raise_on_failure = False
    output_str = buffer[: -len(_END)].decode()

    if len(output_str) - 1 == len(input_str):
        if not raise_on_failure:
            return output_str
        raise ValueError(f"input_str could not be parsed:\n{input_str}")
    return output_str


async def async_crunch(
    inputs: str | list[str] | StringIO,
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
    raise_on_failure: bool = True,
) -> AsyncIterator[str]:
    """Parses strings using Morpheus. Unparsable input_strs raise a ValueError.
    For meaning of arguments, see
    https://github.com/perseids-tools/morpheus#command-line-options."""
    if isinstance(inputs, str):
        # If you want to handle empty input_str gracefully, do so from caller
        # An empty list doesn't raise
        if len(inputs) == 0:
            raise ValueError("Empty input_str cannot be parsed!")
        inputs = [inputs]

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
        stderr=subprocess.STDOUT,
    )
    proc.stdin = cast(StreamWriter, proc.stdin)
    proc.stdout = cast(StreamReader, proc.stdout)
    for input_str in inputs:
        proc_input = (input_str + "\n").encode("utf-8") + _END
        proc.stdin.write(proc_input)
        await proc.stdin.drain()
        buffer = await proc.stdout.readuntil(_END)
        yield _handle_crunch(input_str, buffer, raise_on_failure)


def crunch(
    inputs: str | list[str] | StringIO,
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
    raise_on_failure: bool = True,
) -> Iterator[str]:
    """Parses a single string using Morpheus. Unparsable input_strs raise a
    ValueError. For meaning of arguments, see
    https://github.com/perseids-tools/morpheus#command-line-options."""
    # If you want to handle empty input_strs gracefully, do so from caller
    # An empty list doesn't raise
    if isinstance(inputs, str):
        if len(inputs) == 0:
            raise ValueError("Empty input_str cannot be parsed!")
        inputs = [inputs]

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

    with subprocess.Popen(
        cmd_args,
        env=env,
        stdin=PIPE,
        stdout=PIPE,
        # Merge stdout and stderr
        stderr=subprocess.STDOUT,
    ) as proc:
        proc.stdin, proc.stdout = (
            cast(BufferedReader, proc.stdin),
            cast(BufferedReader, proc.stdout),
        )
        for input_str in inputs:
            proc_input = f"{input_str}\n{_SENTINEL}\n"
            proc.stdin.write(proc_input.encode("utf-8"))
            proc.stdin.flush()

            buffer = b""
            while not buffer.endswith(_END):
                # 65536 is default maximum for pipe buffer
                # since we're streaming individual inputs,
                # this should always be sufficient
                chunk = proc.stdout.read1(65536)
                if not chunk:
                    raise RuntimeError("Cruncher exited unexpectedly")
                buffer += chunk
            yield _handle_crunch(input_str, buffer, raise_on_failure)


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
