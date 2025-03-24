# Официальная документация UV in Docker: https://docs.astral.sh/uv/guides/integration/docker/#getting-started
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
ENV UV_PYTHON_DOWNLOADS=0 UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
LABEL Name="DocuCraft"
LABEL authors="Levchenko V.V"
WORKDIR /DocuCraft

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /DocuCraft
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

CMD ["uv", "run", "docucraft/main.py"]
