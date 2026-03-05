"""
Process Soul Foods morsel CSVs: keep Pink Morsel only, compute sales, output Sales/Date/Region.
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
INPUT_FILES = [
    DATA_DIR / "daily_sales_data_0.csv",
    DATA_DIR / "daily_sales_data_1.csv",
    DATA_DIR / "daily_sales_data_2.csv",
]
OUTPUT_FILE = DATA_DIR / "output.csv"


def main() -> None:
    frames = [pd.read_csv(f) for f in INPUT_FILES]
    df = pd.concat(frames, ignore_index=True)

    # Keep only Pink Morsel (case-insensitive)
    df = df[df["product"].str.strip().str.lower() == "pink morsel"].copy()

    # Parse price: remove $ and convert to float
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

    # Sales = quantity * price
    df["sales"] = df["quantity"] * df["price"]

    # Keep only sales, date, region; rename to Sales, Date, Region
    out = df[["sales", "date", "region"]].rename(
        columns={"sales": "Sales", "date": "Date", "region": "Region"}
    )

    # Group by Date and Region, sum Sales
    out = out.groupby(["Date", "Region"], as_index=False)["Sales"].sum()

    # Sort by Date then Region for readability
    out = out.sort_values(["Date", "Region"]).reset_index(drop=True)

    # Output column order: Sales, Date, Region
    out = out[["Sales", "Date", "Region"]]
    out.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(out)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
