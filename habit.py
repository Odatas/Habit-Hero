# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 10:11:35 2023

@author: patri
"""


from datetime import datetime, timedelta
import json
import re
import Analyzer
import logging


class Habit:
    """
    A class to model and track user habits.

    Attributes:
        name (str): The name of the habit.
        goal (str): A brief description or objective for pursuing this habit.
        frequency (str): How often the habit is to be performed. 'Daily', 'Weekly', 'Monthly', or a specific number.
        start_date (str): The starting date for tracking the habit, formatted as 'YYYY-MM-DD'.
                        Default is the current date if not provided.
        strict (bool): Flag to indicate if the habit tracking should strictly adhere to frequency.
                       Used for custom frequency like 'Every 2 days'.
        streak (int): The current length of consecutive days on which the habit has been performed.
        logs (list): A list of dates, each formatted as 'YYYY-MM-DD', that logs when the habit was performed.

    Class Methods:
        from_json(json_str: str) -> 'Habit': Instantiates a Habit object from a JSON string.

    Methods:
        to_json() -> str: Serializes the Habit object to a JSON string.
        perform_habit_today(today: str = None): Records the habit as performed for today or a specified date.
        perform_habit_on_date(date: str): Records the habit as performed on a specific date and sorts the logs.
        check_habit_due(today: str = None) -> bool: Determines if the habit is overdue based on frequency and last performed date.
        edit_habit(new_name: str = None, new_goal: str = None, new_frequency: str = None): Updates the habit's attributes.
        find_longest_streak() -> int: Calculates and returns the longest consecutive streak of performing the habit.
        display_info(): Prints out all the relevant information about the habit.

    """

    def __init__(self, name, goal, frequency, streak=0, start_date=None, strict=False, logs=None):
        value_string = f"Init: name: {name}, goal: {goal}, frequency: {frequency}, streak: {streak}, start_date: {start_date}, strict: {strict}, logs: {logs}"
        logging.debug(value_string)
        self.name = name  # The name of the habit
        self.strict = strict
        self.goal = goal  # The goal or description
        self.frequency = frequency  # Daily, Weekly (Once a week), Monthly, or a specific day like 'Monday'
        self.start_date = start_date if start_date else datetime.now().strftime("%Y-%m-%d")  # The date when the habit starts
        self.streak = 0  # The current streak for the habit
        self.logs = logs if logs else []  # A list to keep track of when the habit was performed
        if len(self.logs) < 1:
            self.logs.append(start_date)

        self.next_due_date = self.calculate_next_due_date()
        self.streak = self.calculate_streak()

    @classmethod
    def from_dict(cls, habit_dict):
        """Creates a Habit object from a dictionary."""
        return cls(**habit_dict)

    def to_dict(self):
        """Convert the Habit object to a dictionary."""
        habit_dict = {
            'name': self.name,
            'goal': self.goal,
            'frequency': self.frequency,
            'start_date': self.start_date,
            'streak': self.streak,
            'logs': self.logs
        }
        return habit_dict

    def calculate_next_due_date(self):
        return Analyzer.next_habit_due(self.get_last_performed(), self.frequency)

    def get_last_performed(self):
        return self.logs[-1]

    def calculate_streak(self, today_str=None):
        if len(self.logs) < 2:
            return 1
        else:
            streak = 1
            for i in reversed(range(len(self.logs)-1)):

                if Analyzer.verify_frequency_in_range(datetime.strptime(self.logs[i+1], '%Y-%m-%d'),
                                                      datetime.strptime(self.logs[i], '%Y-%m-%d'), self.frequency):
                    streak += 1
                else:
                    break
            return streak

    def perform_habit_today(self, today_str=None):
        """
        Logs the habit as performed for the current day or a specified date.

        Args:
            today_str (str): Optional. The date to log, in 'YYYY-MM-DD' format. Defaults to the current date.
        """
        logging.debug("habit.perform_habit_today called")
        if today_str:
            today = datetime.strptime(today_str, "%Y-%m-%d")
        else:
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
        self.calculate_streak()
        if today_str not in self.logs:
            if self.strict:
                logging.debug("Strict ist set.")
                if self.next_due_date != today_str:
                    logging.debug("Date is not right. Skipping the adding.")
                    return False, "Strict option is set. Today is not the right day to log this activity."
            self.logs.append(today_str)
            self.streak += 1
            self.next_due_date = Analyzer.next_habit_due(today_str, self.frequency)
            return True, ""
        else:
            logging.debug("Date is allready logged so we will skip it")
            return False, "This activity was allready logged today."

    def perform_habit_on_date(self, date):
        """Logs the habit for a specific date and sorts the logs list"""
        if date not in self.logs:
            self.logs.append(date)
            self.logs.sort()  # Sort the logs to maintain order

    def edit_habit(self, new_name=None, new_goal=None, new_frequency=None):
        """Edits the habit's name, goal, or frequency"""
        if new_name:
            self.name = new_name
        if new_goal:
            self.goal = new_goal
        if new_frequency:
            self.frequency = new_frequency

    def display_info(self):
        """Displays habit information"""
        print(f"Habit Name: {self.name}")
        print(f"Goal: {self.goal}")
        print(f"Frequency: {self.frequency}")
        print(f"Start Date: {self.start_date}")
        print(f"Current Streak: {self.streak} days")
