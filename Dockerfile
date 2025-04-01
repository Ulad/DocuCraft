# UV in Docker docs: https://docs.astral.sh/uv/guides/integration/docker/#getting-started
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
ENV UV_PYTHON_DOWNLOADS=0 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

LABEL Name="DocuCraft" \
      Authors="Levchenko V.V"

WORKDIR /DocuCraft

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/DocuCraft/.venv/bin:$PATH"

CMD ["python", "docucraft/main.py"]
