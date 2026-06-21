import pandas as pd
from datetime import datetime

# source for data: https://www.kaggle.com/datasets/robikscube/rollercoaster-database

directory = '/Users/robert/Desktop/rollercoaster/coaster_db.csv' # replace with your own directory here

df = pd.read_csv(directory)

df.head()
df.describe()

df = df.drop(["speed1_value", "speed1_unit", "speed_mph",
              "height_value", "height_unit", "height_ft", "Speed"], axis=1)

df = df[~df["Status"].str.contains("Closed", na=False)]
df = df[~df["Status"].str.contains("Removed", na=False)]
df = df.dropna(subset=["Status"])

df = df.dropna(subset=["speed1"])
df = df.dropna(subset=["speed2"])

df = df.rename(columns={"speed1": "Speed (mph)", "speed2": "Speed (km/h)"})

current_year = datetime.now().year

df["Coaster Age"] = current_year - df["year_introduced"]

def age_category(age):

    if age < 5:
        return "Modern"
    elif age < 20:
        return "Classic"
    else:
        return "Historic"

df["Age Category"] = df["Coaster Age"].apply(age_category)

df = df.dropna(subset=["Height"])
df = df.dropna(subset=["Type"])
df = df.dropna(subset=["Duration"])
df = df.dropna(subset=["Location"])





