VENV_NAME = env
PYTHON = python
PIP = $(VENV_NAME)/Scripts/pip
PYTEST = $(VENV_NAME)/Scripts/pytest
BLACK = $(VENV_NAME)/Scripts/black
ISORT = $(VENV_NAME)/Scripts/isort

.PHONY: setup test run lint

setup:
    $(VENV_NAME)/Scripts/activate requirements.txt test/requirements.txt
    @echo "Setting up virtual environment and installing application requirements..."
    . $(VENV_NAME)/Scripts/activate; \
    $(PIP) install -r requirements.txt

test-setup:
    $(VENV_NAME)/Scripts/activate test/requirements.txt
    @echo "Installing test requirements..."
    . $(VENV_NAME)/Scripts/activate; \
    $(PIP) install -r test/requirements.txt

$(VENV_NAME)/Scripts/activate: requirements.txt
    @echo "Creating virtual environment..."
    python -m venv $(VENV_NAME)
    @echo "Virtual environment created."

test: test-setup
    @echo "Running tests..."
    . $(VENV_NAME)/Scripts/activate; \
    $(PYTEST) --cov-report html:test_runs --cov=yourmodule tests
    @echo "Tests complete. HTML test report saved in test_runs directory."

run:
    @echo "Running the FastAPI application..."
    . $(VENV_NAME)/Scripts/activate; \
    python api/asgi.py

lint: setup
    @echo "Running Black and Isort..."
    . $(VENV_NAME)/Scripts/activate; \
    $(BLACK) yourmodule; \
    $(ISORT) yourmodule

# Default target
all: venv activate install init start
