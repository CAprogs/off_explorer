test:
	@echo "Running tests..."
	@pytest
	@echo "Tests completed."

app:
	@echo "Running app..."
	@uv run streamlit run app.py