'''
Project Overview

The project will make use of Python to explore data related to bike share systems 
for three major cities in the United States—Chicago, New York City, and Washington. 
The following code will be used to import the data and answer interesting questions about it by computing descriptive statistics. 
Also scripts will take in raw input to create an interactive experience in the terminal to present these statistics.

'''


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
    
    # Get user input for city (chicago, new york city, washington)
    city_list = ['chicago', 'new york city', 'washington']    
        
    city = input('Please enter a city chicago, new york city or washington').strip().lower()
    if city in city_list:
        print('We will calculate statistics of bikeshare data for '+ city)
    else:
        while city not in city_list:
            city = input('Please enter a valid city').strip().lower()

    # Get user input for month (all, january, february, ... , june)
    months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        
    month = input("Please enter a month from january to june or 'all' for all months").strip().lower()
    if month in months_list:
        print('Summary statistics will be displayed for the month of '+ month)
    else:
        while month not in months_list:
            month = input('Please enter a valid month').strip().lower()        
    

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    day = input("Please enter a day from monday to sunday or 'all' for all days").strip().lower()
    if day in day_of_week:
        print('Summary statistics will be displayed for '+ day)
    else:
        while day not in day_of_week:
            day = input('Please enter a valid day').strip().lower()

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # Display rows of data to the user
    index = 0    
    while index <= len(df):
        rows = input('Enter yes or no if you want to see 5 rows of the '+ city + ' dataset?').strip().lower()
        if rows == 'yes':
           print(df[index:index+5])
           index += 5
        else:
            break

    
    # Creating important columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['start end trip'] = df['Start Station'] + ' and ' + df['End Station']
    
    # Replacing NaN values
    df['User Type'] = df['User Type'].fillna(df['User Type'].mode()[0])
    
    if city != 'washington':
        df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])
        df['Birth Year'] = df['Birth Year'].fillna(df['Birth Year'].mode()[0])
    
    # Filtering by month    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]
    
    # Filtering by day    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('The most common month is {}'.format(df['month'].mode()[0]))

    # Display the most common day of week
    print('The most common day of the week is {}'.format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    print('The most common start hour is {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    print('The most frequent combination of start and end station is {}'.format(df['start end trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is {}'.format(df['Trip Duration'].sum()))

    # Display mean travel time
    print('The total travel time is {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of the user types are \n', df['User Type'].value_counts(),'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('The counts of gender are \n', df['Gender'].value_counts(),'\n')
    else:
        print('There is no gender counts for washington')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
    
        print('The earliest year of birth is ', earliest)
        print('The most recent year of birth is ', recent)
        print('The common year of birth is ', common)
    else:
        print('There are no birth year statitics for washington')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
