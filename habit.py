from datetime import datetime
import Analyzer
import logging


class Habit:
    """
    A class to model and track user habits.

    This class provides methods to create, log, and track habits, including calculating streaks,
    determining the next due date, and editing habit details. It supports storing habit performance logs
    and checking them against the defined frequency to manage and track habit adherence.

    Parameters:
        name (str): Name of the habit.
        goal (str): Goal or description of the habit.
        frequency (str): Frequency of the habit.
        streak (int, optional): Current streak count. Defaults to 0.
        start_date (str, optional): The starting date of the habit. Defaults to the current date.
        strict (bool, optional): If True, the habit must be performed exactly on the due date. Defaults to False.
        logs (list of str, optional): Initial log entries. Defaults to an empty list.
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
        """
        Calculates the next due date for the habit based on the last performed date and its frequency.

        This method uses the Analyzer class to determine the next due date. It takes into account
        the habit's current frequency and the date it was last performed. 

        Returns:
            datetime.date: The calculated next due date for the habit.
        """

        return Analyzer.next_habit_due(self.get_last_performed(), self.frequency)

    def get_last_performed(self):
        """
        Retrieves the date when the habit was last performed.

        Returns:
            str: The date of the last performance of the habit.
        """

        return self.logs[-1]

    def calculate_streak(self):
        """
        Calculates the current streak of habit performance.

        This method computes the number of consecutive times the habit has been performed according to 
        the defined frequency. The streak is calculated based on the dates logged in 'self.logs', starting from 
        the most recent log entry and moving backwards in time. If the dates meet the frequency criteria 
        (as determined by the Analyzer's 'verify_frequency_in_range' method), the streak count increases.

        Returns:
            int: The number of times the habit has been consecutively performed as per its frequency.
        """

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

    def perform_habit_today(self):
        """
        Logs the habit as performed for the current day or a specified date and updates the streak count.

        This method records the performance of a habit on the current date.
        It first checks if the habit has already been logged for the given date. If not, and if the 'strict' mode is 
        enabled, it verifies whether the log date aligns with the 'next_due_date'. For a strict habit, logging is 
        only allowed on the due date. After logging, it calculates the new streak and updates the 'next_due_date'.

        Returns:
            tuple:
                - bool: True if the habit is successfully logged, False otherwise.
                - str: An error message if the logging is unsuccessful, otherwise an empty string.
        """

        logging.debug("habit.perform_habit_today called")
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
