
install:
	@echo "\nInstalling Dependencies .."
	@uv --version
	@uv lock --check
	@uv sync --no-dev
	@echo "Done."

install-all:
	@echo "Installing all dependencies..."
	@uv sync --all-groups
	@echo "\nCleaning pre-commit cache.."
	@uv run pre-commit gc
	@echo "\nInstalling pre-commit hooks.."
	@uv run pre-commit install --install-hooks
	@echo "Done."

tag:
	@echo "\nChecking commits .."
	@uvx --from commitizen cz bump
	@echo "\nGenerating changelog .."
	@uvx --from commitizen cz bump -ch

test:
	@echo "Running tests..."
	@pytest
	@echo "Tests completed."

app:
	@echo "Running app..."
	@uv run streamlit run app.py
