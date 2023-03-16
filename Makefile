all: $(VIRTUAL_ENV)

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Display callable targets
clean:
	rm -rf build/ dist/ docs/_build *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR)/$(MODULE) -name "__pycache__" | xargs rm -rf

# =============
#  Development
# =============

VIRTUAL_ENV ?= .venv
$(VIRTUAL_ENV): pyproject.toml
	@poetry install --with dev,example
	@poetry self add poetry-bumpversion
	@poetry run pre-commit install --hook-type pre-push
	@touch $(VIRTUAL_ENV)

.PHONY: t test
# target: test - Runs tests
t test: $(VIRTUAL_ENV)
	@poetry run pytest -xsv --mypy tests

.PHONY: mypy
mypy:
	@poetry run mypy aioauth_client

OPEN := $(shell command -v open 2> /dev/null)
open:
	sleep 1
ifdef OPEN
	open http://localhost:5000
endif

server: $(VIRTUAL_ENV)
	@poetry run uvicorn --reload --port 5000 example.app:app

.PHONY: example
example:
	make -j server open

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release: $(VIRTUAL_ENV)
	@$(eval VFROM := $(shell poetry version -s))
	@poetry version $(VERSION)
	@git commit -am "Bump version $(VFROM) → `poetry version -s`"
	@git tag `poetry version -s`
	@git checkout master
	@git merge develop
	@git checkout develop
	@git push origin develop master
	@git push --tags

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VERSION=patch

.PHONY: major
major:
	make release VERSION=major
