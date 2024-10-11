# Define the directories to be processed
DIRECTORIES := config connections tests

# Define Python and tool commands
PYTHON := python
PYTEST := $(PYTHON) -m pytest
BLACK := black
ISORT := isort

.PHONY: all test format clean debug

# Default target
all: test format

# Run tests with coverage
test:
	@echo "Running tests with coverage for config and connections directories"
	$(PYTEST) -vv --cov=config --cov=connections --cov-report=term-missing tests

# Format code using black and isort
format:
	$(BLACK) $(DIRECTORIES)
	$(ISORT) $(DIRECTORIES)

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	# Clean pytest cache
	rm -rf .pytest_cache

# Debug information
debug:
	@echo "Directories to be processed: $(DIRECTORIES)"
	@echo "Python command: $(PYTHON)"
	@echo "Pytest command: $(PYTEST)"
	@echo "Project structure:"
	@find . -type d -not -path '*/\.*'
	@echo "Python files:"
	@find . -name "*.py" -not -path '*/\.*'