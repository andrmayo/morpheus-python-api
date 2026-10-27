# Python API for Morpheus (Work in Progress)

## Scope and Goals

This project aims to make the Morpheus morphological analysis tool easy to use.
To my mind this means:

- providing API endpoints, which I've chosen to do via FastAPI
- exposing Python functions, including:
  - thin wrappers for Morpheus binaries in
    `src/morpheus-python-api/parse/parser.py`
  - convenience functions that abstract away the strict string formatting
    expected by Morpheus binaries as input
  - possibly second-order functionality, e.g. giving parses as structured data
- providing a CLI
- Including the Morpheus binaries in the Python wheel, so the package doubles as
  distribution for Morpheus via pip
