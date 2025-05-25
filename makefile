.PHONY: install install-all tag test app


install:## install only necessary dependencies
	@echo "\nInstalling Dependencies .."
	@uv --version
	@uv lock --check
	@uv sync --no-dev
	@echo "Done."


install-all:## install all dependencies including dev
	@echo "Installing all dependencies..."
	@uv sync --all-groups
	@echo "\nCleaning pre-commit cache.."
	@uv run pre-commit gc
	@echo "\nInstalling pre-commit hooks.."
	@uv run pre-commit install --install-hooks
	@echo "Done."


tag:## bump version and generate changelog
	@echo "\nChecking commits .."
	@uvx --from commitizen cz bump
	@echo "\nGenerating changelog .."
	@uvx --from commitizen cz bump -ch


test:## run tests and validate codecov configuration
	@echo "Running tests..."
	@pytest
	@echo "Validating codecov configuration..."
	@curl --data-binary @.codecov.yml https://codecov.io/validate
	@echo "Tests completed."


app:## run app
	@echo "Running app..."
	@uv run streamlit run app.py


help:
	@bash ./help.sh $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
