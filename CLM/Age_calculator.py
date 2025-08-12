from datetime import datetime


def calculate_age(dob, actual_date=None):
    # Parse the date of birth (DOB) and actual date
    dob = datetime.strptime(dob, "%Y-%m-%d")

    # If actual date is not provided, use today's date
    if actual_date is None:
        actual_date = datetime.today()
    else:
        actual_date = datetime.strptime(actual_date, "%Y-%m-%d")

    # Calculate difference in years
    years_diff = actual_date.year - dob.year

    # Calculate the actual difference in days
    days_in_year = 365.25  # Approximate number of days in a year (considering leap years)
    age = years_diff + ((actual_date - datetime(actual_date.year, dob.month, dob.day)).days / days_in_year)

    return round(age, 4)  # Return age rounded to 4 decimal places


# Example Usage:
dob = "1948-07-27"
actual_date = "2023-07-05"  # Optional, can be omitted for today's date
age = calculate_age(dob, actual_date)
print(f"Age: {age} years")