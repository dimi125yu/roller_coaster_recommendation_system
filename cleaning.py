# source for data: https://www.kaggle.com/datasets/robikscube/rollercoaster-database

from datetime import datetime
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "coaster_db.csv"


def load_and_clean_data(csv_path=DATA_DIR) -> pd.DataFrame:
    """Loads and cleans the rollercoaster dataset."""
    df = pd.read_csv(csv_path)

    # Drop unnecessary columns
    cols_to_drop = [
        "speed1_value", "speed1_unit", "speed_mph",
        "height_value", "height_unit", "height_ft", "Speed"
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # Filter out closed/removed coasters
    df = df[~df["Status"].str.contains("Closed|Removed", case=False, na=True)]

    # Clean required numeric columns
    df = df.dropna(subset=["speed1", "speed2", "Height", "Type", "Duration", "Location"])
    df = df.rename(columns={"speed1": "Speed (mph)", "speed2": "Speed (km/h)"})

    # Calculate coaster age
    current_year = datetime.now().year
    df["Coaster Age"] = current_year - df["year_introduced"]

    def age_category(age):
        if age < 5:
            return "Modern"
        elif age < 20:
            return "Classic"
        return "Historic"

    df["Age Category"] = df["Coaster Age"].apply(age_category)

    return df


if __name__ == "__main__":
    cleaned_df = load_and_clean_data()
    print(f"Data cleaned successfully. Loaded {len(cleaned_df)} rows.")





