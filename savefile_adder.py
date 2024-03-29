# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:34:52 2024

@author: patri
"""

import json
import random
from datetime import datetime, timedelta


# Define the base list of habits with their respective frequencies
base_habits_list = [
    ("Drinking 8 glasses of water", "Daily"),
    ("Exercise for 30 minutes", "Daily"),
    ("Reading for leisure", "Daily"),
    ("Meditation", "Daily"),
    ("Maintaining a gratitude journal", "Daily"),
    ("Taking vitamins or supplements", "Daily"),
    ("Learning a new word", "Daily"),
    ("Practicing a musical instrument", "Daily"),
    ("Reviewing daily goals", "Daily"),
    ("Checking emails", "Daily"),
    ("Grocery shopping", "Weekly"),
    ("Cleaning the house", "Weekly"),
    ("Meal prepping", "Weekly"),
    ("Attending a hobby class", "Weekly"),
    ("Doing laundry", "Weekly"),
    ("Calling or visiting family", "Weekly"),
    ("Planning the upcoming week", "Weekly"),
    ("Reviewing weekly goals", "Weekly"),
    ("Deep cleaning a specific area of the house", "Monthly"),
    ("Budget review and planning", "Monthly"),
    ("Checking car maintenance", "Monthly"),
    ("Haircut or personal grooming session", "Monthly"),
    ("Meeting with a mentor or coach", "Monthly"),
    ("Volunteering or community service", "Monthly"),
    ("Bike ride in the park", "Every Monday"),
    ("Catching up on favorite TV shows", "Every Tuesday"),
    ("Yoga class", "Every Wednesday"),
    ("Book club meeting", "Every Thursday"),
    ("Night out with friends", "Every Friday"),
    ("Family game night", "Every Saturday"),
    ("Gardening or outdoor activities", "Every Sunday"),
    ("Writing a blog post", "Every Sunday")
]


# Function to generate random dates based on the frequency


def generate_dates(frequency, start_date, end_date):
    dates = []
    current_date = start_date

    while current_date <= end_date:
        if frequency == "Daily":
            # 90% chance for 1 day, 10% chance for 2 days delay
            delay = 2 if random.random() < 0.1 else 1
        elif frequency == "Weekly":
            # 90% chance for 7 days, 10% chance for 1 to 30 days delay
            delay = random.randint(1, 30) if random.random() < 0.1 else 7
        elif frequency == "Monthly":
            # 90% chance for 1 month, 10% chance for 20 to 100 days delay
            delay = random.randint(20, 100) if random.random() < 0.1 else 30
        else:  # Specific days like "Every Monday"
            # 90% chance for exact 7 days, 10% chance to skip this cycle
            delay = 0 if random.random() < 0.1 else 7

        if delay != 0:  # Only add date if delay is not 0
            dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=delay)

    return dates


# Function to create a new user with 5 random habits from the list


def create_new_user_with_habits(username, habits_list):
    new_user_habits = []
    start_date = datetime.now().date() - timedelta(days=300)  # starting point 3 months ago

    for _ in range(7):  # select 5 random habits
        habit_name, frequency = random.choice(base_habits_list)
        habit_dates = generate_dates(frequency, start_date, datetime.now().date())
        new_user_habits.append({
            "name": habit_name,
            "goal": "Goal for " + habit_name,
            "frequency": frequency,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "logs": habit_dates
        })

    return {username: new_user_habits}


# Read the existing data from the file
with open('habithero_savefile.json', 'r') as file:
    data = json.load(file)

# Create a new user with habits
new_user_data = create_new_user_with_habits("User_" + datetime.now().strftime('%Y%m%d%H%M%S'), base_habits_list)

# Update the data with the new user's information
data.update(new_user_data)

# Save the updated data back to a new file
new_savefile_path = 'habithero_savefile.json'
with open(new_savefile_path, 'w') as file:
    json.dump(data, file, indent=4)
