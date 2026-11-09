# Python API for Morpheus

## Scope and Goals

This project aims to make the Morpheus morphological analysis tool easy to use.
To my mind this means:

- providing API endpoints, which I've chosen to do via FastAPI
- exposing Python functions, including:
  - thin wrappers for Morpheus binaries in
    `src/morpheus-python-api/parse/parser.py`
  - giving parses as structured data
- providing a CLI
- Including the Morpheus binaries in the Python wheel, so the package doubles as
  distribution for Morpheus via pip

## Current State of the Project

The core functionality of the project is present, with FastAPI routes for
cruncher, library functions for cruncher and gener, and structured parsing for
cruncher integration with both. In addition, the Typer CLI serves as a drop-in
replacement for the Morpheus cruncher and gener binaries.

## To Do

The main desiderata at this point are:

- broader test coverage, especially with the FastAPI routes
- reading words to parse from a file
- FastAPI routes for gener
- pname functionality (somewhat more difficult given that pname is not well
  documented)
- structured parsing for gener
