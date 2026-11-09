"""
main.py

Setup for FastAPI application.
"""

import logging

from fastapi import FastAPI

from morpheus_python_api.api.routes import router


logger = logging.getLogger(__name__)

app = FastAPI(title="Morpheus-API", description="Python API for Morpheus")
app.include_router(router)
