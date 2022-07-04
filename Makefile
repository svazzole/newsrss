install:
	@echo "Installing..."
	poetry install --no-root

activate:
	@echo "Activating virtual environment"
	poetry shell

test:
	pytest

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
