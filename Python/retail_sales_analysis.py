"""
Retail Sales Data Pipeline & Analysis

ETL workflow: Kaggle extraction -> Pandas transformation -> SQLite load -> SQL analysis

Usage:
    python Python/retail_sales_analysis.py                 # download from Kaggle, then run everything
    python Python/retail_sales_analysis.py --csv orders.csv  # use a CSV you already have
"""

import argparse
import re
import sqlite3
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = PROJECT_DIR / "SQL" / "retail_sales_analysis.sql"
OUTPUT_DIR = PROJECT_DIR / "outputs"
KAGGLE_DATASET = "ankitbansal06/retail-orders"


def extract_data(dest: Path = PROJECT_DIR) -> Path:
    """Download and unzip orders.csv from Kaggle (needs a Kaggle API token)."""
    subprocess.run(
        ["kaggle", "datasets", "download", KAGGLE_DATASET, "-f", "orders.csv", "-p", str(dest)],
        check=True,
    )
    zip_path = dest / "orders.csv.zip"
    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dest)
        zip_path.unlink()
    print("Dataset extracted successfully.")
    return dest / "orders.csv"


def transform_data(file_path: Path) -> pd.DataFrame:
    """Clean and transform the retail orders dataset."""
    # Treat the dataset's placeholder text as missing values
    df = pd.read_csv(file_path, na_values=["Not Available", "unknown"])

    # Standardize column headers to snake_case
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    duplicates = df.duplicated().sum()
    if duplicates:
        df = df.drop_duplicates()
    print(f"Removed {duplicates} duplicate rows.")

    # Calculate financial metrics
    df["discount"] = df["list_price"] * df["discount_percent"] * 0.01
    df["sale_price"] = df["list_price"] - df["discount"]
    df["profit"] = df["sale_price"] - df["cost_price"]

    # Convert order_date to a proper date
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d")

    print(f"Data transformed successfully. Shape: {df.shape}")
    return df


def load_to_sqlite(df: pd.DataFrame, db_path: Path = PROJECT_DIR / "retail_orders.db",
                   table_name: str = "df_orders") -> sqlite3.Connection:
    """Load the transformed DataFrame into a SQLite database."""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, con=conn, index=False, if_exists="replace")
    print(f"Loaded {len(df)} records into '{table_name}' in '{db_path.name}'.")
    return conn


def run_analysis(conn: sqlite3.Connection, sql_file: Path = SQL_FILE,
                 output_dir: Path = OUTPUT_DIR) -> dict:
    """Run each query in the SQL file, print the result and save it as a CSV."""
    output_dir.mkdir(exist_ok=True)
    blocks = re.split(r"\n(?=-- \d+\.)", sql_file.read_text(encoding="utf-8").strip())
    results = {}
    for block in blocks:
        title_match = re.match(r"-- (\d+)\.\s*(.+)", block)
        query = re.sub(r"^--.*$", "", block, flags=re.M).strip().rstrip(";")
        if not title_match or not query:
            continue
        number, title = title_match.groups()
        result = pd.read_sql_query(query, conn)
        slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
        result.to_csv(output_dir / f"{int(number):02d}_{slug}.csv", index=False)
        results[title] = result
        print(f"\n{number}. {title}\n{result.head(10).to_string(index=False)}")
    print(f"\nSaved {len(results)} result tables to '{output_dir.name}/'.")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Retail sales ETL and SQL analysis")
    parser.add_argument("--csv", type=Path, help="Path to orders.csv (skips the Kaggle download)")
    args = parser.parse_args()

    csv_path = args.csv if args.csv else extract_data()
    df = transform_data(csv_path)
    conn = load_to_sqlite(df)
    try:
        run_analysis(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
