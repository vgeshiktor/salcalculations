# Makefile for Python Project

# Define the virtual environment directory
VENV_DIR := .venv

# Define the requirements file
REQUIREMENTS_FILE := requirements.txt

# Define the source and test directories
SRC_DIR := .
TEST_DIR := tests

.PHONY: all install_deps lint format sort_imports type_check test clean

all: install_deps lint format sort_imports type_check test

# Create virtual environment and install dependencies
install_deps:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip3 install --upgrade pip
	$(VENV_DIR)/bin/pip3 install -r $(REQUIREMENTS_FILE)

# Format with black
format:
	#$(VENV_DIR)/bin/pip3 install black
	$(VENV_DIR)/bin/black $(SRC_DIR) $(TEST_DIR) --line-length 79

# Lint with flake8
lint: sort_imports format
	#$(VENV_DIR)/bin/pip3 install flake8
	$(VENV_DIR)/bin/flake8 $(SRC_DIR) $(TEST_DIR)

# Sort imports with isort
sort_imports:
	#$(VENV_DIR)/bin/pip3 install isort
	$(VENV_DIR)/bin/isort $(SRC_DIR) $(TEST_DIR)

# Type check with mypy
type_check:
	#$(VENV_DIR)/bin/pip3 install mypy
	$(VENV_DIR)/bin/mypy $(SRC_DIR)

# Run tests with pytest
test:
	#$(VENV_DIR)/bin/pip3 install pytest
	$(VENV_DIR)/bin/pytest $(TEST_DIR)

# Clean the project
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
