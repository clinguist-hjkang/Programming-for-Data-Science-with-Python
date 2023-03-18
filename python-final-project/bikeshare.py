import time
import pandas as pd
import numpy as np
import calendar
# from datetime import datetime
import datetime
from pathlib import Path

CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\"s explore some US bikeshare data!")
    cities = list(CITY_DATA.keys())
    cities_title = [city.title() for city in cities]

    print(f"We have the data for {', '.join(cities_title)}.\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Enter a city: ").lower())

        if city not in cities:
            print(f"Sorry, your response is not valid. Choose a city from the following list: {cities_title}")
            continue
        else:
            # city was successfully parsed, and we"re happy with its value.
            # we"re ready to exit the loop.
            city = "_".join(city.split())
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Enter a month: ").lower())
        months_title = list(calendar.month_name)[1:]  #Note the blank at index 0. There is no month zero.
        months = [month.lower() for month in months_title]

        if month not in months:
            print(f"Sorry, your response is not valid. Choose a month from the following list: {months_title}")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Enter a day: ").lower())
        days_title = list(calendar.day_name)
        days = [day.lower() for day in days_title]

        if day not in days:
            print(f"Sorry, your response is not valid. Choose a day from the following list: {days_title}")
            continue
        else:
            break

    print("-"*40)
    return city, month, day
    


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    p = Path(__file__).with_name(f"{city}.csv")
    filename = p.absolute()

    df = pd.read_csv(filename)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # display the most common month
    df["month"] = df["Start Time"].dt.month
    popular_month_int = df["month"].mode()[0]
    popular_month = calendar.month_name[popular_month_int]
    print(f" - Most Popular Month: {popular_month}")

    # display the most common day of week
    df["day"] = df["Start Time"].dt.weekday
    popular_day_int = df["day"].mode()[0]
    popular_day = calendar.day_name[popular_day_int]
    print(f" - Most Popular Day: {popular_day}")

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = str(df["hour"].mode()[0])
    popular_hour_formated = datetime.datetime.strptime(popular_hour, "%H")
    # print(f"Most Popular Hour: {popular_hour_formated}")
    print(f" - Most Popular Hour: {popular_hour_formated.strftime('%I:%M %p')}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print(f" - Most Popular Start Station: {popular_start_station}")

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print(f" - Most Popular End Station: {popular_end_station}")

    # display most frequent combination of start station and end station trip
    station_series = pd.concat([df["Start Station"], df["End Station"]])
    popular_station = station_series.mode()[0]
    print(f" - Most Popular Station: {popular_station}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time_sec = float(df["Trip Duration"].sum())
    total_travel_time = datetime.timedelta(seconds=total_travel_time_sec)
    total_days, total_hours, total_minutes = total_travel_time.days, total_travel_time.seconds // 3600, total_travel_time.seconds // 60 % 60
    print(f" - Total Travel Time: {total_days} days, {total_hours} hours and {total_minutes} minutes")

    # display mean travel time
    mean_travel_time_sec = float(df["Trip Duration"].mean())
    mean_travel_time = datetime.timedelta(seconds=mean_travel_time_sec)
    mean_minutes = mean_travel_time.seconds // 60 % 60
    print(f" - Mean Travel Time: {mean_minutes} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    count_user_type = df["User Type"].value_counts()
    percs_user_type = df["User Type"].value_counts(normalize=True)
    dist_user_type = pd.concat([count_user_type, percs_user_type], axis=1, keys=["count", "percentage"])
    print(f" - Number / Percentage of User Types:\n{dist_user_type}\n")

    # Display counts of gender
    try:
        count_gender = df["Gender"].value_counts()
        percs_gender = df["Gender"].value_counts(normalize=True)
        dist_gender = pd.concat([count_gender, percs_gender], axis=1, keys=["count", "percentage"])
        print(f" - Number / Percentage of Gender:\n{dist_gender}\n")
    except KeyError:
        print(" -- No data available about gender. --\n")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df["Birth Year"].min())
        print(f" - Earliest Year of Birth: {earliest_year}")
    except KeyError:
        print(" -- No data available about the earliest year of birth. --\n")

    try:
        recent_year = int(df["Birth Year"].max())
        print(f" - Most Recent Year of Birth: {recent_year}")
    except KeyError:
        print(" -- No data available about the most recent year of birth. --\n")

    try:
        common_year = int(df["Birth Year"].mode()[0])
        print(f" - Most Common Year of Birth: {common_year}")
    except KeyError:
        print(" -- No data available about the most common yaer of birth. --\n")        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def display_raw_data(df):
    """
    Asks users if they want to see 5 lines of raw data.

    Args:    
        (dataframe) df - dataframe of the selected city
    Returns:
        Nothing
    """
    window = 5
    display = input(f"\nWould you like to see {window} lines of raw data? Enter Y (yes) or N (no).\n")

    if display.lower() == "y":
        row_index = 0
        print(df.iloc[row_index:row_index+window])
        row_index += window
                
        while row_index < len(df):
            continue_display = input("\nWould you like to see next 5 lines? Enter Y (yes) or N (no).\n")
            if continue_display.lower() == "y":
                print(df.iloc[row_index:row_index+window])
                row_index += window
            else:
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter Y (yes) or N (no).\n")
        if restart.lower() != "y":
            break


if __name__ == "__main__":
	main()
