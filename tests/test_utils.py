import pytest
import pandas as pd
from off_streamlit_app.utils import (
    process_ean13,
    fetch_nutricore_color,
    value_isin_df,
    fetch_product_details,
    process_barcode,
    find_image_by_barcode,
)
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    ["barcode", "expected"],
    [
        ("1234567890123", "123/456/789/0123"),
        ("0000001234567", "000/000/123/4567"),
        ("123", "123///"),
        ("abcdefghi", "abc/def/ghi/"),
    ],
)
def test_process_ean13(barcode: str, expected: str) -> None:
    assert process_ean13(barcode) == expected


@pytest.mark.parametrize(
    ["nutriscore", "expected"],
    [
        ("a", "#006400"),
        ("b", "#00cc44"),
        ("c", "#ffcc00"),
        ("d", "#ff6600"),
        ("e", "#cc0000"),
        ("something_else", "#808080"),
    ],
)
def test_fetch_nutricore_color(nutriscore: str, expected: str) -> None:
    assert fetch_nutricore_color(nutriscore) == expected


@pytest.mark.parametrize(
    ["column", "value", "expected"],
    [
        ("barcode", "1234567890123", True),
        ("nutriscore", "d", False),
        ("barcode", "0000000001111", True),
        ("brand", "Brand F", False),
    ],
)
def test_value_isin_df(mock_df: pd.DataFrame, column: str, value: str, expected: bool) -> None:
    assert value_isin_df(mock_df, column, value) == expected


@pytest.mark.parametrize(
    ["barcode", "expected"],
    [
        ("1234567890123", {"product_name": "Product A", "brand": "Brand A", "quantity": "100 kg", "nutriscore": "a"}),
        ("123", {"product_name": "", "brand": "", "quantity": "", "nutriscore": ""}),
    ],
)
def test_fetch_product_details(mock_df: pd.DataFrame, barcode: str, expected: dict[str, str]) -> None:
    assert fetch_product_details(mock_df, barcode) == expected


def test_process_barcode(capsys: pytest.CaptureFixture[str], mock_df: pd.DataFrame) -> None:
    assert process_barcode("abcd", mock_df, print) == (
        None,
        {"product_name": "", "brand": "", "quantity": "", "nutriscore": ""},
    )
    captured = capsys.readouterr()
    assert "Barcode must be a 13 length digit value present in the dataset." in captured.out
    assert process_barcode("1234567890123", mock_df) == (
        "123/456/789/0123",
        {"product_name": "Product A", "brand": "Brand A", "quantity": "100 kg", "nutriscore": "a"},
    )


def test_find_image_by_barcode(mocker: MockerFixture) -> None:
    mock_process_barcode = mocker.patch("off_streamlit_app.utils.process_barcode")
    mock_process_barcode.return_value = ("123/456/789/0123", {"key": "value"})
    assert find_image_by_barcode("1234567890123", "https://some/url/path/") == (
        "https://some/url/path/123/456/789/0123/1.400.jpg",
        {"key": "value"},
    )
    mock_process_barcode.return_value = (None, {"key": "value"})
    assert find_image_by_barcode("some_invalid_value") == (None, {"key": "value"})
