import pandas as pd
import pytest


@pytest.fixture
def mock_df() -> pd.DataFrame:
    """Fixture to create a sample DataFrame for testing."""
    data = {
        "barcode": ["1234567890123", "0000001234567", "0000000001111"],
        "product_name": ["Product A", "Product B", "Product C"],
        "brand": ["Brand A", "Brand B", "Brand C"],
        "quantity": ["100 kg", "200 L", "300 g"],
        "nutriscore": ["a", "b", "c"],
    }
    return pd.DataFrame(data)
