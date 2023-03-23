import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all','january', 'february', 'march', 'april','may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']

DAYS = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Please enter city name (Chicago, New York City or Washington):").lower()
        if city in CITY_DATA:
            break
        else:
            print('Your input invalid.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter month, for all enter all: ").lower()
        if month in MONTHS:
            break
        else:
            print('Your input invalid.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter day, (all) for all: ").lower()
        if day in DAYS:
            break
        else:
            print('Your input invalid.')

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

    df = pd.read_csv(CITY_DATA[city])
    
    #add a new column (Month) with value exctracted from (Start Time)
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    
    #add a new column (Day) with value exctracted from (Start Time)
    df['Day'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour
        
    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month)
        df = df[df['Month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        day = DAYS.index(day)
        df = df[df['Day'] == day]
        
    print('-'*40)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    common_month = df['Month'].mode()[0]    
    common_day = df['Day'].mode()[0]
    common_start_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()[0]
    
    # extract data and output them
    table_data = pd.Series({"Common Month":MONTHS[common_month].title(),
                           "Common Day":DAYS[common_day].title(),
                           "Common Hour":common_start_hour})
    tabulate_output(table_data, headers=["Time Unit", "Value"])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    common_combination_stations = df.groupby(["Start Station", "End Station"]).size().idxmax()

    table_data = pd.Series({"Common Start Station":common_start_station,
                           "Common End Station":common_end_station,
                           "Common Combination Stations":common_combination_stations})
    tabulate_output(table_data, headers=["Station", "Value"])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time in hour
    total_travel_time = df['Hour'].sum()

    # mean travel time in minutes
    mean_travel_time = df['Trip Duration'].mean()/60
    
    # format data to output
    output_table_data = [["Label", "Value"],
                        ["Total Travel Time", "{} hours".format(round(total_travel_time, 3))],
                        ["Mean Travel Time", "{} minutes".format(round(mean_travel_time), 3)]]
    output_table = tabulate(output_table_data, headers="firstrow", tablefmt="grid")
    print(output_table)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertype_data = df.groupby(['User Type'])['User Type'].count()
    
    print("Table of User Types:")
    tabulate_output(usertype_data)

    # Display counts of gender
    if 'Gender' in df.columns:
        count_of_gender = df.groupby('Gender')['Gender'].count()
        
        print("Table of Gender Type: ")
        tabulate_output(count_of_gender)
    else:
        print("There is no (Gender) in data source")
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'][df['Birth Year'].idxmin()]
        most_recent_birth = df['Birth Year'][df['Birth Year'].idxmax()]
        common_birth_year = df['Birth Year'].mode()[0]
    
        birth_data = pd.Series({"Earliest Birth": earliest_birth,
                  "Most Recent Birth": most_recent_birth,
                  "Common Year": common_birth_year})
        
        print("Table of Birth data: ")
        tabulate_output(birth_data)
    else:
        print("There is no (Birth Year) in data source")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def tabulate_output(data: pd.Series, headers = ["Label", "Value"]):
    """preparing data to be displayed by tabulate function"""
    data_list = [headers]
    for i, v in data.items():
        data_list.append([i, v])
    
    print(tabulate(data_list, headers="firstrow", tablefmt="grid"))

def show_raw_data(df):
    """show raw data upon user request"""
    next_flag = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (next_flag != "no"):
        print(df[start_loc:start_loc+5])
        next_flag = input('\nDo you wish to show next 5 rows? Enter yes or no\n').lower()
        start_loc += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()