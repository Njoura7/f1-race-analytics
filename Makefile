PYTHON ?= python

ifeq ($(OS),Windows_NT)
	VENV_PYTHON := .venv/Scripts/python
else
	VENV_PYTHON := .venv/bin/python
endif

.PHONY: setup test lint app clean

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

lint:
	$(VENV_PYTHON) -m ruff check .

test:
	$(VENV_PYTHON) -m pytest

app:
	$(VENV_PYTHON) -m streamlit run app/app.py

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)"
