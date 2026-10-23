import asyncio
from asyncio import create_subprocess_exec
from subprocess import CalledProcessError
from typing import cast

from morpheus_python_api.types import Language


async def crunch(
    input: str,
    language: Language = Language.GREEK,
    non_strict_case: bool = False,
    ignore_accents: bool = False,
    database_format: bool = False,
    ending_index: bool = False,
    keep_beta_code: bool = False,
    lemma: bool = False,
    perseus_format_off: bool = False,
    verbs_only: bool = False,
) -> str:
    """For meaning of arguments, see https://github.com/perseids-tools/morpheus#command-line-options"""
    cmd_args = ["cruncher"]
    if language is Language.LATIN:
        cmd_args.append("-L")
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
    cmd_args.append(input)

    proc = await create_subprocess_exec(
        *cmd_args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise CalledProcessError(cast(int, proc.returncode), cmd_args, stdout, stderr)

    stdout, stderr = stdout.decode(), stderr.decode()

    # TODO: Error checking

    return stdout
