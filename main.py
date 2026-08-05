import doctest
import numpy as np
import pandas as pd
from cleaning import load_and_clean_data

def location_validation(location) -> bool:
    """
    >>> location_validation("Sea Lion Park")
    True
    >>> location_validation("")
    False
    >>> location_validation(1234)
    False
    """
    return isinstance(location, str) and bool(location.strip())


def numeric_validation(val, min_val=0) -> bool:
    """
    >>> numeric_validation(12.5)
    True
    >>> numeric_validation(-1.2)
    False
    >>> numeric_validation("12.5")
    False
    """
    return isinstance(val, (int, float)) and not isinstance(val, bool) and val >= min_val

def get_input(prompt, val_type=str, validator=lambda x: True, err_msg="Invalid input."):
    while True:
        try:
            raw_val = input(prompt).strip()
            val = val_type(raw_val)
            if validator(val):
                return val
            print(err_msg)
        except ValueError:
            print(err_msg)


def get_user_preferences() -> tuple[dict, dict]:
    """Collects both target preferences and importance weights from the user."""
    print("=== Step 1: Set Target Preferences ===")
    location = get_input("Theme Park Location (leave blank for any): ", str)
    height = get_input("Max Height Restriction Required (inches/cm): ", float, numeric_validation, "Must be positive.")
    speed = get_input("Target Speed (mph): ", float, numeric_validation, "Must be positive.")
    duration = get_input("Target Duration (seconds): ", float, numeric_validation, "Must be positive.")
    age = get_input("Target Max Age of Coaster (years): ", int, numeric_validation, "Must be a positive integer.")

    print("\n=== Step 2: Set Importance Weights (0 - 100) ===")
    print("How important is each feature to you?")
    speed_w = get_input("Speed Importance Weight: ", float, numeric_validation, "Must be a positive number.")
    duration_w = get_input("Duration Importance Weight: ", float, numeric_validation, "Must be a positive number.")
    age_w = get_input("Age Importance Weight: ", float, numeric_validation, "Must be a positive number.")

    total_weight = speed_w + duration_w + age_w
    if total_weight == 0:

        weights = {"speed": 0.34, "duration": 0.33, "age": 0.33}
    else:
        weights = {
            "speed": speed_w / total_weight,
            "duration": duration_w / total_weight,
            "age": age_w / total_weight,
        }

    preferences = {
        "location": location,
        "height": height,
        "speed": speed,
        "duration": duration,
        "age": age,
    }

    return preferences, weights

def rank_coasters(df: pd.DataFrame, prefs: dict, weights: dict):

    filtered = df.copy()

    if prefs["location"]:
        filtered = filtered[
            filtered["Location"].str.contains(prefs["location"], case=False, na=False)
        ]

    filtered = filtered[filtered["Height restriction"] <= prefs["height"]]

    if filtered.empty:
        print("\nNo coasters matched your strict location and height filters.")
        return

    # Criteria match scores scaled 0.0 to 1.0

    filtered["speed_match"] = np.minimum(1.0, filtered["Speed (mph)"] / prefs["speed"])

    filtered["duration_match"] = np.minimum(1.0, filtered["Duration"] / prefs["duration"])

    age_diff = np.abs(filtered["Coaster Age"] - prefs["age"])
    max_age_span = filtered["Coaster Age"].max() - filtered["Coaster Age"].min()
    if max_age_span == 0:
        max_age_span = 1
    filtered["age_match"] = np.maximum(0.0, 1.0 - (age_diff / max_age_span))

    filtered["Match_Score"] = (
            (filtered["speed_match"] * weights["speed"]) +
            (filtered["duration_match"] * weights["duration"]) +
            (filtered["age_match"] * weights["age"])
    )

    filtered["Match_%"] = (filtered["Match_Score"] * 100).round(1)

    ranked = filtered.sort_values(by="Match_%", ascending=False)

    print("\n=== Rollercoaster Rankings (Highest to Lowest Match) ===")
    display_cols = ["Location", "Speed (mph)", "Duration", "Coaster Age", "Match_%"]
    print(ranked[display_cols].to_string(index=False))


if __name__ == "__main__":
    doctest.testmod()

    coaster_df = load_and_clean_data()
    preferences, weights = get_user_preferences()
    rank_coasters(coaster_df, preferences, weights)