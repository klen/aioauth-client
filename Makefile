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

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install bump2version
	@$(VIRTUAL_ENV)/bin/bump2version $(VERSION)
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

# ===============
#  Build package
# ===============

.PHONY: register
# target: register - Register module on PyPi
register:
	@$(VIRTUAL_ENV)/bin/python setup.py register

.PHONY: upload
# target: upload - Upload module on PyPi
upload: clean
	@$(VIRTUAL_ENV)/bin/pip install twine wheel
	@$(VIRTUAL_ENV)/bin/python setup.py sdist bdist_wheel
	@$(VIRTUAL_ENV)/bin/twine upload dist/*

# =============
#  Development
# =============

VIRTUAL_ENV ?= env
$(VIRTUAL_ENV): setup.cfg
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -e .[build]
	@touch $(VIRTUAL_ENV)

$(VIRTUAL_ENV)/bin/pytest: requirements-tests.txt $(VIRTUAL_ENV) 
	@$(VIRTUAL_ENV)/bin/pip install -r requirements-tests.txt
	@touch $(VIRTUAL_ENV)/bin/py.test

.PHONY: t test
# target: test - Runs tests
t test: $(VIRTUAL_ENV)/bin/pytest
	@$(VIRTUAL_ENV)/bin/pytest -xsv tests.py

.PHONY: mypy
mypy:
	$(VIRTUAL_ENV)/bin/mypy aioauth_client.py

OPEN := $(shell command -v open 2> /dev/null)
open:
	sleep 1
ifdef OPEN
	open http://localhost:5000
endif

server: $(VIRTUAL_ENV)/bin/pytest
	@$(VIRTUAL_ENV)/bin/uvicorn --reload --port 5000 example.app:app

.PHONY: example
example:
	make -j server open
