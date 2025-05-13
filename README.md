# About
A simple streamlit app based on open food facts data

The data displayed in this app is based on the [Open Food Facts](https://world.openfoodfacts.org/) database, which is a collaborative project that collects and shares information about food products from around the world. The data is available under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/).


# Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended)
- Python 3.12 or higher (can be installed via `uv python install 3.12`)
- make (optional, for convenience)

> On Windows, you can install `GNU Make` as mentioned [here](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows#:~:text=make%20is%20a,the%20previous%20choices.).

# Installation

Using UV (recommended)
```bash
uv sync
```

Using pip (within a virtual environment)
```bash
pip install -r requirements.txt
```

# Running the app

Please before running the app, ensure to export the `PYTHONPATH` environment variable to include the `src` directory by running :
```bash
export PYTHONPATH="./src"
```
If you are familiar with [direnv](https://direnv.net/), you can use it to automatically set the `PYTHONPATH` variable when you enter the project directory.

There is multiple ways to run this app :

```bash
# using streamlit within your virtual environment
streamlit run app.py

# using uv
uv run streamlit app.py

# using python
python -m streamlit run app.py

# using the provided make command
make app
```


# License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

# Contributing

Feel free to open issues or pull requests. Contributions are welcome!

# Bonus

<details><summary>Reproducing the extracted data from this project</summary>

<br>

- First download the parquet file from the OFF database available [here](https://huggingface.co/datasets/openfoodfacts/product-database/tree/main).

- From there you can start exploring using [duckdb](https://duckdb.org/docs/stable/)

Assuming you are using the CLI client of duckdb, you can run the following command to start exploring the data:

```bash
# enter duckdb CLI
duckdb

# create a persistent database
.open food.duckdb
```

```sql
-- create a table from the parquet file
CREATE TABLE IF NOT EXISTS off_french_food_analysis AS (
    SELECT g['unnest']['text'] AS product_name, {', '.join(FIELDS)}
        FROM read_parquet('{parquet_filepath}') AS f,
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

</details>

<br>

# References
- [Open Food Facts](https://world.openfoodfacts.org/)
- [Open Food Facts x DuckDB : Article](https://blog.openfoodfacts.org/en/news/food-transparency-in-the-palm-of-your-hand-explore-the-largest-open-food-database-using-duckdb-%f0%9f%a6%86x%f0%9f%8d%8a)
- [Data analysis examples using DuckDB on OFF data](https://wiki.openfoodfacts.org/DuckDB_Cheatsheet)
- [Reusing Open Food Facts data](https://wiki.openfoodfacts.org/Reusing_Open_Food_Facts_Data#DuckDB_to_query_the_database)
- [Using Open Food Facts AWS images dataset](https://openfoodfacts.github.io/openfoodfacts-server/api/aws-images-dataset/)
- [First steps with Streamlit](https://docs.streamlit.io/get-started/tutorials)