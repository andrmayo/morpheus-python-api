FROM python:3.15-rc-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/



