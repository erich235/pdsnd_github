import time
from datetime import datetime
import pandas as pd
import numpy as np

# Set option to display 100 columns to make sure that entire dataset is displayed when showing raw data
pd.set_option('display.max_columns', 100)

# Did not use this dictionary. Felt that creating something to look at possible data files would be more
# flexible in a real world senario (i.e. Wouldn't require change to code to make work for aditional cities added at a later date)
# This will require that new cities have "_" instead of spaces in file name
#CITY_DATA = { 'chicago': 'chicago.csv',
#              'new york city': 'new_york_city.csv',
#              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (list) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (list) possible days - list of days in the week
        (list) possible months - list of months in a year
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    # Ask for all cities that the user wants to find data for.
    while True:
        cities = input("List cities to pull data from(separate with commas):").split(",")
        
        # Set up lists and condition flag to sort data into and direct decision making
        good_cities = []
        bad_cities = []
        retry_flag = False
        
        # Loop through each city to check if it exists
        for city in cities:
             # Make sure data is formated correctly
            city = city.replace(" ", "_")
            
            # Correct for extra spaces in list
            i = 0
            while  city[i] == "_":
                i += 1
            city = city[i:]

            # Load data into dataframe
            # Error Handle if city data not found
            try:
                df = pd.read_csv(city.lower() + ".csv")
                good_cities.append(city)
            except:
                bad_cities.append(city)
                continue

            # Ask user to update info if given bad data
        if bad_cities != []:
            option = input('Cities {} cannot be found. c = Continue without them, r = Retry entry, e = exit:'.format(bad_cities))
            
            # Give user choices of how to proceed. 
            while True:
                if option == 'c' or option == 'r' or option == 'e':
                    break
                else:
                    option = input("Please enter correct responce of c,r,or e:")
                
            if option == 'c':
                cities = good_cities
            elif option == 'r':
                retry_flag = True
            elif option == 'e':
                exit()
            else:
               break
        
        # Check retry flag to see if user want to re-do input
        if retry_flag == True:
            retry_flag = False
            continue
        else:
            break
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("How would you like to filter the data? (all, january, february, ... , june):").lower()
    
    # Check input
    while True:
        possible_months = ["all","january","february","march","april","may","june","july","august","september","october","november","december"]
        if month in possible_months:
            if month != "all":
                month = possible_months.index(month)
            break
        else:
            month = input("Please enter correct input of all,january,february,march,april,may,june,july,august,september,october,november,december:")
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to look at? (all,monday,tuesday, ... sunday):").lower()
    
    # Check input
    while True:
        possible_days = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        if day in possible_days:
            if day != "all":
                day = possible_days.index(day)
            break
        else:
            day = input("please enter correct input of all,monday,tuesday,wednesday,thursday,friday,saturday, or sunday:")

    print('-'*40)
    return cities, month, day, possible_days, possible_months

def show_raw_data(df,raw_data_yes_no):
    """ Displays the first 5 rows of raw data until user says "no".
    
    arg:
    (df) df - dataframe of data
    (bool) raw_data_yes_no - Flag for when the user no longer wants to see raw data
    """

    while True:
        if raw_data_yes_no == True:
            break
        else:
            ask_yes_no = input("Would you like to see the first 5 rows of raw data?(y/n): ")
            if ask_yes_no == "y":
                print(df.head(5))
                raw_data_yes_no = False
                break
            elif ask_yes_no == "n":
                raw_data_yes_no = True
                break
            else:
                print('Please enter either y for yes or n for no.')

    return raw_data_yes_no
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
    # Read csv file and change starttime to data_time format
    raw_data = pd.read_csv(city.lower() + ".csv")
    raw_data['Start Time'] = pd.to_datetime(raw_data['Start Time'])
    
    # Apply filters if requested
    if month != "all" and day != "all":
        df_intermitent = raw_data[(raw_data['Start Time'].dt.month == month)]
        df = df_intermitent[(df_intermitent['Start Time'].dt.day == day)]
    elif month != "all":
        df = raw_data[(raw_data['Start Time'].dt.month == month)]
    elif day != "all":
        df = raw_data[(raw_data['Start Time'].dt.day == day)]
    else: 
        df = raw_data
                  
    return df

def time_stats(df,month,day,possible_days, possible_months, raw_data_yes_no):
    """Displays statistics on the most frequent times of travel.
    
    arg:
    (dataframe) df - data to work with
    (str) month - month to filter on
    (str) day - day to filter on
    (list) possible_days - days of the week
    (list) possible_months - months in the year
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # Skip if filtered by month
    if month != "all":
        most_com_month = "n/a"
    else:
        most_com_month = possible_months[int(df['Start Time'].dt.month.mode())]
    
    # Display results
    print("Most common month: {}".format(most_com_month))

    # TO DO: display the most common day of week
    # Skip if filtered by day of week
    if day != "all":
        most_com_day = "n/a"
    else:
        most_com_day = possible_days[int(df['Start Time'].dt.dayofweek.mode())]

    # Display results
    print("Most common day: {}".format(most_com_day))
                      
    # TO DO: display the most common start hour
    # Create list of whole number start hours
    times_of_day = ['n/a','1:00am','2:00am','3:00am','4:00am','5:00am','6:00am','7:00am','8:00am','9:00am','10:00am','11:00am','12:00am'
                    '1:00pm','2:00pm','3:00pm','4:00pm','5:00pm','6:00pm','7:00pm','8:00pm','9:00pm','10:00pm','11:00pm','12:00pm']
    
    # Find most common start hour
    most_com_start_hour = times_of_day[int(df['Start Time'].dt.hour.mode())]
    
    # Display results
    print("Most common start hour: {}".format(most_com_start_hour))
    
    
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    yes_no = show_raw_data(df,raw_data_yes_no)
    return yes_no
    print('-'*40)


def station_stats(df,raw_data_yes_no):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = str(df['Start Station'].mode()[0])
    print('Most popular start station: ' + pop_start_station)

    # TO DO: display most commonly used end station
    pop_end_station = str(df['End Station'].mode()[0])
    print('Most popular end station: ' + pop_end_station)
                      
    # TO DO: display most frequent combination of start station and end station trip
    df['combo_station'] = df['Start Station'] + ',' + df['End Station']
    # Had trouble getting string to not truncate, had to create list and then split into pieces to get it to work 
    pop_combo_station = str(df['combo_station'].mode()[0]).split(',')
    print('Most popular trip: ' + str(pop_combo_station[0]) + ' to ' + str((pop_combo_station[1])))
                      
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    yes_no = show_raw_data(df,raw_data_yes_no)
    return yes_no
    print('-'*40)

def hour_min_sec(seconds):
    """ Converts seconds into hours - min - sec 
    
    Arg:
    (int) seconds - number of seconds to convert
    
    Returns:
    (list) [hours, mins, sec] - List of conveted time to hours, min, secs.
    """
    
    # Truncate all calcs to integer values. Find remainder of previous step for current step.
    hours = int(seconds / 3600)
    mins = int((seconds - (hours * 3600)) / 60)
    sec = int((seconds - (hours * 3600) - (mins * 60)))
   
    return [hours, mins, sec]
                      
def trip_duration_stats(df,raw_data_yes_no):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = hour_min_sec(df['Trip Duration'].sum())
    print('Total time of bike use: {} hours {} minutes {} seconds'.format(total_time[0], total_time[1], total_time[2]))
                      
    # TO DO: display mean travel time
    average_duration = hour_min_sec(df['Trip Duration'].mean())   
    print('Average trip duration: {} hours {} minutes {} seconds'.format(average_duration[0], average_duration[1], average_duration[2]))

    # Display shortest and longest travel times
    min_trip = hour_min_sec(df['Trip Duration'].min())
    max_trip = hour_min_sec(df['Trip Duration'].max())
    print('Shortest trip duration: {} hours {} minutes {} seconds'.format(min_trip[0], min_trip[1], min_trip[2]))
    print('Longest trip duration: {} hours {} minutes {} seconds'.format(max_trip[0], max_trip[1], max_trip[2]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    yes_no = show_raw_data(df,raw_data_yes_no)
    return yes_no
    print('-'*40)


def user_stats(df,raw_data_yes_no):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('Display of user types:')
    print(user_count)

    # TO DO: Display counts of gender
    # Error handle for when data not given
    try:
        gender_count = df['Gender'].value_counts()
    except:
        gender_count = "No gender information to display"
    print('\nDisplay of user gender count')
    print(gender_count)
     
    # TO DO: Display earliest, most recent, and most common year of birth
    # Error handle for when data not given
    try:
        year = datetime.now().year
        oldest_birthyear = int(df['Birth Year'].min())
        youngest_birthyear = int(df['Birth Year'].max())
        most_common_birthyear = int(df['Birth Year'].mode())
        oldest_user_age = int(year) - oldest_birthyear
        youngest_user_age = int(year) - youngest_birthyear
        most_common_age = int(year) -  most_common_birthyear
        print('The oldest user is {} years old and was born in {} '.format(oldest_user_age, oldest_birthyear))
        print('The youngest user in {} years old and was born in {} '.format(youngest_user_age, youngest_birthyear))
        print('The average user is {} years old and is born in {} '.format(most_common_age, most_common_birthyear))
    except:
        print('No birthday data to display')
                     
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    yes_no = show_raw_data(df,raw_data_yes_no)
    return yes_no
    print('-'*40)


def main():
    """ Find statistical data for bike share date from csv files. Bike share data 
        broken up into individual files by city.
        Cities with spaces need to be formated with "_" instead of the spaces. 
    """
    
    while True:
        cities, month, day, possible_days, possible_months = get_filters()
        for city in cities:
            # Set flag to check for raw data to false (i.e. ask user for raw data info)
            raw_data_yes_no = False
            
            print(('-' * 20) + city + ' results' + ('-' * 20))
            # Make sure data is formated correctly
            city = city.replace(" ", "_")
            
            # Correct for spaces in list
            i = 0
            while city[i] == "_":
                i += 1
            city = city[i:]
                
            df = load_data(city, month, day)

            raw_data_yes_no = time_stats(df,month,day,possible_days,possible_months,raw_data_yes_no)
            raw_data_yes_no = station_stats(df,raw_data_yes_no)
            raw_data_yes_no = trip_duration_stats(df,raw_data_yes_no)
            raw_data_yes_no = user_stats(df,raw_data_yes_no)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
