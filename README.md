![GitHub](https://img.shields.io/github/license/CAprogs/off_explorer?color=blue)
![Python Versions](https://img.shields.io/badge/python-3.12_|_3.13_|_3.14-blue)
![CI status](https://img.shields.io/github/actions/workflow/status/CAprogs/off_explorer/ci.yml)
[![codecov](https://codecov.io/gh/CAprogs/off_explorer/graph/badge.svg?token=4NNWO47JTH)](https://codecov.io/gh/CAprogs/off_explorer)

# About
A simple streamlit app based on open food facts data

The data displayed in this app is based on the [Open Food Facts](https://world.openfoodfacts.org/) database, which is a collaborative project that collects and shares information about food products from around the world. The data is available under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/).


# Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended)
- Python 3.12 or higher (can be installed via `uv python install 3.12`)
- make (optional but recommended for convenience)

> [!NOTE]
> On Windows, you can install `GNU Make` as mentioned [here](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows#:~:text=make%20is%20a,the%20previous%20choices.). \
> On Linux and MacOS, `Make` should be already installed by default.

# Installation

Using _make_ (recommended)
```bash
make install
```

Using uv (within a virtual environment)
```bash
# Install python dependencies
pip install -r requirements.txt
```

# Running the app


> [!IMPORTANT]
> Please before running the app, ensure to export the `PYTHONPATH` environment variable to include the `src` directory by running :
>
>```bash
>export PYTHONPATH="./src"
>```
>
>If you are familiar with [direnv](https://direnv.net/), you can use it to automatically set the `PYTHONPATH` variable when you enter the project directory via the `.envrc` file.
>
>> The feature to automatically add a directory path to the `PYTHONPATH` via uv is currently discussed [here](https://github.com/astral-sh/uv/issues/11175).


There is multiple ways to run this app :

```bash
# using the provided make command
make app

# using uv
uv run streamlit app.py

# using streamlit within your virtual environment
streamlit run app.py

# using python
python -m streamlit run app.py
```

# Data extraction & analysis

### Reproducing the extracted data from this project


- First download the parquet file from the OFF database available [here](https://huggingface.co/datasets/openfoodfacts/product-database/tree/main).

- From there you can start exploring using [duckdb](https://duckdb.org/docs/stable/)

Assuming you are using the CLI version of duckdb, you can run the following command to start exploring the data :

```bash
# enter duckdb CLI
duckdb

# create a persistent database named food.duckdb
.open food.duckdb
```

```sql
-- Print all available columns in the parquet file
DESCRIBE read_parquet('food.parquet');

-- create a table from the parquet file
CREATE TABLE IF NOT EXISTS off_french_food_analysis AS (
    SELECT g['unnest']['text'] AS product_name,
            brands AS brand,
            quantity,
            nutriscore_grade AS nutriscore,
            code AS barcode,
            additives_n,
            allergens_tags,
            categories,
            ingredients,
            manufacturing_places,
            owner,
            stores
        FROM read_parquet('food.parquet') AS f,
            UNNEST(f.generic_name) AS g
            WHERE lang = 'fr' -- only keep french products
            AND obsolete IS FALSE
            AND completeness > 0.8
            AND g['unnest']['lang'] = 'fr' -- only keep products with french description available
            AND nutriscore_grade NOT IN ('not-applicable','unknown')
            WHERE len(code) = 13 -- only keep products with a 13 digit code
            ORDER BY nutriscore_grade DESC
        );

-- export the table to a parquet file
COPY (SELECT * FROM off_french_food_analysis)
TO 'off_french_food_analysis.parquet' (FORMAT PARQUET);
```

# License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

# Contributing

Feel free to open issues or pull requests. Contributions are welcome !


# References
- [Open Food Facts](https://world.openfoodfacts.org/)
- [Open Food Facts x DuckDB : Article](https://blog.openfoodfacts.org/en/news/food-transparency-in-the-palm-of-your-hand-explore-the-largest-open-food-database-using-duckdb-%f0%9f%a6%86x%f0%9f%8d%8a)
- [Data analysis examples using DuckDB on OFF data](https://wiki.openfoodfacts.org/DuckDB_Cheatsheet)
- [Reusing Open Food Facts data](https://wiki.openfoodfacts.org/Reusing_Open_Food_Facts_Data#DuckDB_to_query_the_database)
- [Using Open Food Facts AWS images dataset](https://openfoodfacts.github.io/openfoodfacts-server/api/aws-images-dataset/)
- [First steps with Streamlit](https://docs.streamlit.io/get-started/tutorials)
