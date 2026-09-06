.PHONY: test lint typecheck check

UV_CACHE_DIR ?= .uv-cache

test:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --extra dev pytest

lint:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --extra dev ruff check .

typecheck:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --extra dev mypy

check: test lint typecheck
