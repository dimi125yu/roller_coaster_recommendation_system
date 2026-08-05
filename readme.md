# Rollercoaster Recommendation System

A Python-based recommendation tool that pairs users with roller coasters across amusement parks in the United States based on target physical attributes, location filtering, and custom feature importance weights.

## Description

This project processes roller coaster data from Kaggle, filters out defunct or closed rides, cleans and derives temporal features (such as coaster age and age category), and ranks active coasters according to personalized user inputs using a weighted similarity algorithm.

# Set-Up

1. Download the Kaggle dataset from source: https://www.kaggle.com/datasets/robikscube/rollercoaster-database
2. Save the dataset file as coaster_db.csv in the same directory as cleaning.py and main.py.

Afterwards, run main script directly:
```
python main.py
```

# How it Works

## Data Cleaning

Filtering: Retains only operational coasters (removing rides marked as "Closed" or "Removed").

Feature Extraction: Calculates Coaster Age relative to the current year (current_year - year_introduced) and categorizes rides into Modern, Classic, or Historic.

Standardization: Drops redundant metric units and cleans required fields including height restriction, speed, duration, and location.

## Filtering

Before scoring, strict constraints are applied to narrow down candidate coasters:

Location Filter: Performs a case-insensitive string match on location (if provided).

Height Restriction: Excludes coasters with height restrictions exceeding the user's specified limit (Height restriction <= user_limit).

## Ranking Algorithm

The engine normalizes attributes into match ratios between $0.0$ and $1.0$:

Speed Match: Calculates ratio against target speed capped at $1.0$,
Duration Match: Calculates ratio against target duration capped at $1.0$,
Age Match: Scores proximity to the target age relative to the dataset's maximum age span

Then

Final Score Calculation: User weights ($W_{speed}, W_{duration}, W_{age}$) are normalized to sum to $1.0$. The final score is calculated as a weighted sum expressed as a percentage:

# Tuning the Algorithm

You can adjust how recommendations are prioritized by modifying parameter logic in main.py:

Adjust Default Fallback Weights: If a user enters zero total weight during the prompt, the system falls back to equal weighting. You can modify this distribution in get_user_preferences():

```
weights = {"speed": 0.50, "duration": 0.30, "age": 0.20}
```

Penalty Functions for Exceeding Targets: Currently, speed and duration ratios cap at $1.0$ (meaning faster rides receive a perfect score). To penalize speeds higher than requested, replace the ratio logic in rank_coasters() with absolute difference scaling:

```
speed_diff = np.abs(filtered["Speed (mph)"] - prefs["speed"])
filtered["speed_match"] = np.maximum(0.0, 1.0 - (speed_diff / prefs["speed"]))
```

Adding New Features: To incorporate additional metrics (such as drop height or inversion count), add corresponding entry prompts in get_user_preferences(), compute their normalized $0.0 - 1.0$ score in rank_coasters(), and include them in the weights calculation dictionary.