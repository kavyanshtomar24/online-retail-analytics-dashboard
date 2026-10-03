"""Core cleaning and example SQL analysis for the Online Retail Analytics project."""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "online_retail_II.csv.gz"
CLEAN_PATH = ROOT / "data" / "cleaned" / "online_retail_II_cleaned.csv.gz"


def clean_data(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(raw_path, low_memory=False)

    # Remove exact duplicate transaction rows.
    df = df.drop_duplicates()

    # Standardize the transaction date and remove unusable core records.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate", "Price", "Country"])

    # Recover missing product descriptions from the most common description
    # associated with the same StockCode whenever possible.
    description_mode = (
        df[df["Description"].notna()]
        .groupby("StockCode")["Description"]
        .agg(lambda x: x.mode().iloc[0])
    )
    df["Description"] = df["Description"].fillna(
        df["StockCode"].map(description_mode)
    )

    # Add fields used in the dashboard.
    df["TransactionType"] = np.where(df["Quantity"] < 0, "Return", "Sale")
    df["Revenue"] = df["Quantity"] * df["Price"]

    return df


def example_sql_analysis(df: pd.DataFrame) -> None:
    from pandasql import sqldf

    query = """
    SELECT
        Country,
        COUNT(DISTINCT `Customer ID`) AS unique_customers,
        SUM(Revenue) AS total_revenue
    FROM df
    GROUP BY Country
    ORDER BY total_revenue DESC
    LIMIT 10;
    """
    print(sqldf(query, {"df": df}))


if __name__ == "__main__":
    cleaned = clean_data()
    print("Cleaned shape:", cleaned.shape)
    print("Duplicates:", cleaned.duplicated().sum())
    print("Missing values:\n", cleaned.isna().sum())

    # Uncomment to regenerate the compressed cleaned dataset.
    # cleaned.to_csv(CLEAN_PATH, index=False, compression="gzip")

    example_sql_analysis(cleaned)
