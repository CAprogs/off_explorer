"""Utility functions."""

import duckdb
import streamlit as st
from typing import Any
import pandas


def process_EAN13(barcode: str) -> str:
    """Process EAN13 barcode to a specific format."""
    last_four_digits = barcode[9:]
    first_nine_digits = barcode[:9]
    first_digits_splitted = [first_nine_digits[i : i + 3] for i in range(0, 9, 3)]
    first_digits_splitted.append(last_four_digits)
    return "/".join(first_digits_splitted)


@st.cache_data
def fetch_nutricore_color(nutriscore: str) -> str:
    """Fetch the color associated with a specific nutriscore."""
    nutriscore_colors = {
        "a": "#006400",
        "b": "#00cc44",
        "c": "#ffcc00",
        "d": "#ff6600",
        "e": "#cc0000",
    }
    return nutriscore_colors.get(nutriscore.lower(), "#808080")


def value_isin_df(
    df: pandas.DataFrame, column: str, value: str, reader: Any = duckdb.sql
) -> bool:
    """Check if a value is in a specific column of a DataFrame."""
    df = df
    return (
        reader(f"SELECT {column} FROM df WHERE {column} = '{value}'").fetchone()
        is not None
    )


@st.cache_data
def fetch_product_details(
    df: pandas.DataFrame, barcode: str, reader: Any = duckdb.sql
) -> dict[str, str]:
    """Get product details from a DataFrame based on a barcode."""
    df = df
    query = f"SELECT product_name, brand, quantity, nutriscore FROM df WHERE barcode = '{barcode}'"
    result = reader(query).fetchone()
    if result:
        return {
            "product_name": result[0],
            "brand": result[1],
            "quantity": result[2],
            "nutriscore": result[3],
        }
    else:
        return {"product_name": "", "brand": "", "quantity": "", "nutriscore": ""}


@st.cache_data
def fetch_data(
    reader: Any = duckdb.sql, data_path: str = "data.parquet"
) -> pandas.DataFrame:
    """Fetch data from a Parquet file using DuckDB."""
    query = f"""SELECT product_name,
                      brand,
                      quantity,
                      nutriscore,
                      barcode
                FROM {data_path}"""
    data = reader(query)
    return data.df()


def process_barcode(
    barcode: str, df: pandas.DataFrame = fetch_data(), warn: Any = st.warning
) -> tuple[str | None, dict[str, str]]:
    """Process the barcode input from the user."""
    product_details = fetch_product_details(df, barcode)
    if (
        barcode.isdigit()
        and value_isin_df(df, "barcode", barcode)
        and len(barcode) == 13
    ):
        return process_EAN13(barcode), product_details
    else:
        warn("Barcode must be a 13 length digit value present in the dataset.")
        return None, product_details


@st.cache_data
def find_image_by_barcode(
    barcode: str,
    url_prefix: str = "https://openfoodfacts-images.s3.eu-west-3.amazonaws.com/data/",
) -> tuple[str | None, dict[str, str]] | None:
    """Find the image URL using the barcode."""
    processed_barcode, products_details = process_barcode(barcode)
    if processed_barcode:
        return f"{url_prefix}{processed_barcode}/1.400.jpg", products_details
    else:
        return None, products_details
