from cleaning import df
import doctest

def get_float(prompt):

    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Value must be positive.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int(prompt):

    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Value must be positive.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_string(prompt):

    while True:
        value = input(prompt).strip()

        if value == "":
            print("Input cannot be empty.")
        else:
            return value


user_preferences = {
    "location": get_string("Theme Park Location: "),
    "height": get_float("Height Required: "),
    "duration": get_float("Duration of Coaster: "),
    "speed": get_float("Speed: "),
    "age": get_int("Age of Coaster: ")
}


def location_validation(location):
    """
    Checks validity of location input

    >>> location_validation("Sea Lion Park")
    True

    >>> location_validation("")
    False

    >>> location_validation(1234)
    False
    """

    return isinstance(location, str) and location.strip() != ""


def height_validation(height):
    """
    Checks validity of height input

    >>> height_validation(12.5)
    True

    >>> height_validation(-1.2)
    False

    >>> height_validation("12.5")
    False
    """

    return isinstance(height, (int, float)) and height >= 0


def duration_validation(duration):
    """
    Checks validity of duration input

    >>> duration_validation(1.22)
    True

    >>> duration_validation(-1.22)
    False

    >>> duration_validation("1.22")
    False
    """

    return isinstance(duration, (int, float)) and duration >= 0


def speed_validation(speed):
    """
    Checks validity of speed input

    >>> speed_validation(123)
    True

    >>> speed_validation(-123)
    False

    >>> speed_validation("123")
    False
    """

    return isinstance(speed, (int, float)) and speed >= 0


def age_validation(age):
    """
    Checks validity of age input

    >>> age_validation(13)
    True

    >>> age_validation(-13)
    False

    >>> age_validation("13")
    False
    """

    return isinstance(age, int) and age >= 0


filtered = df[
    (df["Location"].str.contains(
        user_preferences["location"],
        case=False,
        na=False
    )) &

    (df["Height restriction"] <= user_preferences["height"]) &

    (df["Duration"] >= user_preferences["duration"]) &

    (df["Speed (mph)"] >= user_preferences["speed"]) &

    (df["Coaster Age"] <= user_preferences["age"])
]

if filtered.empty:
    print("No matching coasters found.")

else:

    filtered = filtered.copy()

    filtered["Score"] = (
        abs(filtered["Speed (mph)"] - user_preferences["speed"])
        +
        abs(filtered["Duration"] - user_preferences["duration"])
    )

    top_matches = filtered.sort_values("Score").head(10)

    print(top_matches)

doctest.testmod()