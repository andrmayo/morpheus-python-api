"""test_large_streaming_inputs.py

Test crunch functionality for large streaming inputs.

The issue here is that every 1000 inputs, the cruncher prints a progress line
to stderr, which causes issues with handling outputs.

The fix that this is testing is in the Makefile
and simply patches the C code using `sed` so that the -T flag to cruncher also
disables the progress bar.
"""

from collections.abc import AsyncIterator, Iterable
from itertools import cycle, islice

import pytest

from morpheus_python_api.parse.parser import async_crunch, crunch
from morpheus_python_api.types import WordParse

items: list[str] = ["lo/gos", "lu/w", "ai)/nigma", "dei/knumi", "a)=ra"]
n = 500


async def _async_wrap_iterable(items: Iterable[str]) -> AsyncIterator[str]:
    for item in items:
        yield item


@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_async_crunch_large_input():
    input_generator = _async_wrap_iterable(islice(cycle(items), len(items) * n))
    result_count = 0
    async for _, parse in async_crunch(input_generator):
        assert isinstance(parse, WordParse)
        result_count += 1
    assert result_count == len(items) * n


@pytest.mark.timeout(30)
def test_crunch_large_input():
    input_generator = islice(cycle(items), len(items) * n)
    result_count = 0
    for _, parse in crunch(input_generator):
        assert isinstance(parse, WordParse)
        result_count += 1
    assert result_count == len(items) * n
