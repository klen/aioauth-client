# AGENTS.md

Guidance for coding agents working in this repository.

## Repository overview

`aioauth-client` is a small Python library providing OAuth 1.0a and OAuth 2.0
client helpers for asyncio and trio. HTTP is done with `httpx`. Python >= 3.11,
packaged and locked with uv (`uv.lock` is committed).

- `aioauth_client/__init__.py` — public API: re-exports every name below;
  users import from here (`from aioauth_client import GithubClient`).
- `aioauth_client/base.py` — `OAuthError`, `User`, `ClientRegistry`, `Client`.
- `aioauth_client/oauth1.py` — `OAuth1Client`, `Signature`, `HmacSha1Signature`.
- `aioauth_client/oauth2.py` — `OAuth2Client`.
- `aioauth_client/clients/` — one module per provider, file name equals the
  registry name (`github.py`, `vk.py`, ...). `clients/__init__.py` imports all
  of them, which is what registers them in `ClientRegistry`.
- `aioauth_client/types.py` — shared type aliases (`TRes`, `THeaders`,
  `TParams`).
- `aioauth_client/utils.py` — small helpers shared by provider parsers.
- `aioauth_client/py.typed` — PEP 561 marker; keep it in the package.
- `tests/` — pytest suite; `conftest.py` mocks `httpx.AsyncClient.request` and
  parametrizes every test over asyncio and trio.
- `example/` — optional ASGI demo app (needs the `example` uv dependency group),
  not part of the library.
- `.github/workflows/tests.yml` — CI: ruff, mypy, pytest on Python 3.11-3.15.
- `Makefile`, `pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml`,
  `README.md`, `Changelog` (plain text, hand-written).

## Repo conventions

- Adding a provider means adding `aioauth_client/clients/<name>.py` with one
  class that subclasses `OAuth1Client` or `OAuth2Client` and sets `name`,
  `base_url`, `authorize_url`, `access_token_url`, `user_info_url` and a static
  generator `user_parse(data)` yielding `(field, value)` pairs for
  `User.__slots__`, then importing the class in `clients/__init__.py` and
  adding it to the package `__all__`s.
- Every subclass is auto-registered in `ClientRegistry.clients` by its `name`
  at import time. Names must be unique and are used by `example/app.py` and
  tests.
- `Client.user_parse` uses `assert isinstance(data, dict)` for type narrowing;
  keep that pattern (ruff `S101` is intentionally ignored).
- Library code targets Python 3.11+: use `X | Y` unions and builtin generics
  (`dict[str, int]`), and do not add `from __future__ import annotations`.
  Avoid 3.12+ syntax.
- Style: ruff with `select = ["ALL"]` (long ignore list in `pyproject.toml`),
  line length 100, formatting by `ruff format` (not black). Match existing
  style; do not add per-file `noqa` unless the existing config genuinely
  cannot express it.
- Tests import client classes inside the test functions and rely on the
  autouse `http`/`response` fixtures. Never make real network calls in tests.
- Pre-commit runs `ruff format`, ruff, and `uv lock --check` on commit, and
  mypy + pytest on push. Do not bypass hooks with `--no-verify`.

## Safe validation

Run from the repo root; `uv run` uses the project `.venv`:

```bash
uv sync --all-groups                 # dev + example deps (recreates .venv if needed)
uv run ruff check aioauth_client     # lint (CI runs exactly this)
uv run ruff format --check           # formatting check (CI runs this too)
uv run mypy                          # type-check aioauth_client
uv run pytest tests                  # tests + mypy (addopts = -svx --mypy)
uv lock --check                      # lockfile matches pyproject.toml
uv run pre-commit run --all-files    # commit-stage hooks: ruff format, ruff, uv-lock
make test                            # same as the pytest line
make mypy
```

- `pytest` addopts include `--mypy`, so a test run also type-checks; `-x` means
  it stops at the first failure.
- Type annotations are not lazy: there is no `from __future__ import
  annotations`, so imports used only in annotations must be real imports.
- `mypy` runs with `check_untyped_defs`, `warn_unused_ignores`,
  `warn_redundant_casts`, and `strict_equality`; keep it clean instead of
  adding `# type: ignore` (the one exception is `VKClient.request`, whose
  signature predates the base class).
- Ruff resolves from `uv.lock`; `select = ["ALL"]` means a lock upgrade can
  introduce new rule codes. Add new codes to the ignore list instead of
  reformatting unrelated code in a focused change.
- Narrowing a run is cheap: `uv run pytest tests/test_oauth2.py -k oauth2`.
- Lint only `aioauth_client`; `ruff check .` also lints `tests/`, which is not
  what CI enforces.

## High-risk commands

- `make release`, `make minor`, `make patch`, `make major` — bump the version,
  commit, tag, merge `develop` into `master`, and push branches and tags.
  Never run these unless the user explicitly asks for a release.
- `uv publish` / the `release` GitHub workflow publishes to PyPI.
  Do not publish from a local checkout.
- `make clean` — `rm -rf build/ dist/ docs/_build *.egg-info` plus bytecode.
  Destructive; avoid unless the user asks.
- `uv lock` / `uv lock --upgrade` re-resolves dependencies and rewrites
  `uv.lock` (upgrade may pull new versions). Only do it when dependency
  changes require it, and commit the resulting lockfile.
- Do not commit, tag, push, or rewrite history unless explicitly instructed.

## Files and directories not to edit casually

- `uv.lock` — generated; change it with uv, never by hand.
- `pyproject.toml` — version, dependencies and uv groups, build backend
  (hatchling), ruff/mypy/pytest config; edits affect CI and packaging.
- `.pre-commit-config.yaml`, `.github/workflows/*` — CI and release behavior.
- `example/config.py` — demo OAuth credentials checked into the repo (already
  public). Do not replace them with real secrets; never commit live secrets.
- `aioauth_client/py.typed` — must not be deleted.
- Generated/cache dirs: `dist/`, `build/`, `aioauth_client.egg-info/`, `.venv/`,
  `.tox/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `env/`.

## Good defaults for agents

- Prefer small edits in `aioauth_client/base.py`, `oauth1.py`, `oauth2.py` or
  the relevant client module. Keep one provider per module (there is a test
  for that) and re-export new public names from `aioauth_client/__init__.py`.
- After changing a base class or `Client` behavior, check all three base
  classes plus the provider subclasses that override `user_parse`,
  `request`, or token handling.
- Add or extend a test in `tests/` for behavior changes (the suite is small and
  fast). Finish with ruff + mypy + pytest.
- Branch flow is `develop` -> `master`; `master` is release-only.
  `.github/workflows/release.yml` publishes on version tags (`make release`
  pushes them) after running the tests in the tag.
- Keep `README.md` and `Changelog` updated only when user-facing behavior or
  the public API changes.
