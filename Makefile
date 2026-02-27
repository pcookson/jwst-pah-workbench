.PHONY: venv install run test

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
DEPS_STAMP := .venv/.deps-installed

venv: $(PYTHON)

$(PYTHON):
	python3 -m venv .venv

$(DEPS_STAMP): pyproject.toml $(PYTHON)
	$(PIP) install --upgrade pip
	$(PIP) install "hatchling>=1.24.0" "editables>=0.5"
	$(PIP) install --no-build-isolation -e .[dev]
	touch $(DEPS_STAMP)

install: $(DEPS_STAMP)

run: $(DEPS_STAMP)
	$(PYTHON) -m pah_workbench

test: $(DEPS_STAMP)
	$(PYTEST) -q
