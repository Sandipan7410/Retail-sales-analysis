"""
Retail Sales Data Pipeline & Analysis
ETL workflow: Kaggle Extraction -> Pandas Transformation -> SQLite Load & Querying
"""

import os
import sqlite3
import zipfile
import pandas as pd


def extract_data():
    """Download and extract dataset from Kaggle."""
    # Download dataset via Kaggle CLI
    os.system("kaggle datasets download ankitbansal06/retail-orders -f orders.csv")[cite: 1]

    # Unzip file
    with zipfile.ZipFile("orders.csv.zip", "r") as zip_ref:[cite: 1]
        zip_ref.extractall()[cite: 1]
    print("Dataset extracted successfully.")


def transform_data(file_path="orders.csv") -> pd.DataFrame:
    """Clean and transform the retail orders dataset."""
    # Read CSV and handle explicit missing values
    df = pd.read_csv(file_path, na_values=["Not Available", "unknown"])[cite: 1]

    # Standardize column headers to snake_case
    df.columns = df.columns.str.lower().str.replace(" ", "_")[cite: 1]

    # Calculate financial metrics
    df["discount"] = df["list_price"] * df["discount_percent"] * 0.01[cite: 1]
    df["sale_price"] = df["list_price"] - df["discount"][cite: 1]
    df["profit"] = df["sale_price"] - df["cost_price"][cite: 1]

    # Convert order_date to proper datetime format
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d")[cite: 1]

    print(f"Data transformed successfully. Shape: {df.shape}")[cite: 1]
    return df


def load_to_sqlite(df: pd.DataFrame, db_name="retail_orders.db", table_name="df_orders"):
    """Load transformed DataFrame into SQLite database."""
    conn = sqlite3.connect(db_name)[cite: 1]
    df.to_sql(table_name, con=conn, index=False, if_exists="replace")[cite: 1]
    print(f"Loaded {len(df)} records into '{table_name}' table in '{db_name}'.")
    return conn
