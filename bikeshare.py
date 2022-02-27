import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """ Get user input for city (chicago, new york city, washington). """

    while True:
        try:
            city = input("Which city would you like to analyze? Type Chicago, New York City, or Washington.  ").lower()
            if city in ('chicago', 'new york city', 'washington'):
                break
            print('Please type Chicago, New York City, or Washington only. ')
        except:
            print("I don't understand your answer. Please try again. ")


    """ Get user input for month (all, january, february, ... , june) """

    while True:
        try:
            month = input("Which month would you like to filter by? Type a month from January throuugh June, or type 'all' to view all months. " ).lower()
            if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                break
            print("Please type a valid month or 'all' to view all months. ")
        except:
            print("I don't understand your answer. Please try again. ")

    """ Get user input for day of week (all, monday, tuesday, ... sunday) """

    while True:
        try:
            day = input("Which day would you like to filter by? Type a day of the week, or type 'all' to view all days. " ).lower()
            if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                break
            print("Please type a valid day of the week or 'all' to view all days. ")
        except:
            print("I don't understand your answer. Please try again. ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    """ Load data file into a dataframe """
    df = pd.read_csv(CITY_DATA[city])

    """ Convert the Start Time column to datetime """
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ Extract month and day of week from Start Time to create new columns """
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    """ Filter by month if applicable """
    if month != 'all':
        """ Use the index of the months list to get the corresponding int """
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        """ Filter by month to create the new dataframe """
        df = df[df['month'] == month]

    """ Filter by day of week if applicable """
    if day != 'all':
        """ Filter by day of week to create the new dataframe """
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ Display the most common month """
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_name = months[popular_month - 1]
    print('Most Common Month: ', popular_month_name)

    """ Display the most common day of week """
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week: ', popular_weekday)

    """ Display the most common start hour
    convert the Start Time column to datetime """
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ Extract hour from the Start Time column to create an hour column """
    df['hour'] = df['Start Time'].dt.hour

    """ Find the most common hour (from 0 to 23) """
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (round(time.time() - start_time, 4)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ Display most commonly used start station """
    popular_start_stn = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', popular_start_stn)

    """ Display most commonly used end station """
    popular_end_stn = df['End Station'].mode()[0]
    print('Most Popular End Station: ', popular_end_stn)

    """ Display most frequent combination of start station and end station trip """
    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combination = df['Station Combination'].mode()[0]
    print('Most Popular Combination of Start and End Stations: ', popular_combination)

    print("\nThis took %s seconds." % (round(time.time() - start_time, 4)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """ Display total travel time """
    total_trip_time = df['Trip Duration'].sum()
    print('The total travel time is ', total_trip_time, ' seconds.')

    """ Display mean travel time """
    mean_trip_time = df['Trip Duration'].mean()
    print('The mean travel time is ', mean_trip_time, ' seconds.')

    print("\nThis took %s seconds." % (round(time.time() - start_time, 4)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Display counts of user types """
    print('Counts of user types: ')
    print(df['User Type'].value_counts())

    """ Display counts of gender """
    try:
        print('Counts of user gender: ')
        print(df['Gender'].value_counts())
    except:
        print('There is no gender data available for Washington.')

    """ Display earliest, most recent, and most common year of birth """
    try:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest birth year is ', int(min_birth_year))
        print('The most recent birth year is ', int(max_birth_year))
        print('The most common birth year is ', int(common_birth_year))
    except:
        print('There is no birth year data available for Washington.')

    print("\nThis took %s seconds." % (round(time.time() - start_time, 4)))
    print('-'*40)


def display_data(df):
    """Displays 5 rows of data at a time based on user input."""

    display = input('Would you like to display the first 5 rows of data? Enter yes or no. ').lower()
    if display != 'yes':
        print("Okay, we won't display any data.")
    if display == 'yes':
        df = df.reset_index()
        start_row = 0
        while True:
            print(df.loc[start_row])
            print(df.loc[start_row + 1])
            print(df.loc[start_row + 2])
            print(df.loc[start_row + 3])
            print(df.loc[start_row + 4])
            more_data = input('Would you like to display the next 5 rows of data? Enter yes or no. ').lower()
            if more_data != 'yes':
                break
            start_row += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to explore additional data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
