# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 12:11:27 2023

@author: patri
"""

import json
import os
from habit import Habit
import logging


class SaveFileManager:
    """
    A manager to handle saving, loading, and managing user data related to habits.

    This class offers functionality to save and load user habit data to and from 
    a JSON-formatted save file. It also provides utility methods to retrieve a list 
    of all users present in the save file and load the entire data for diagnostic purposes.

    Attributes:
        savefile_path (str): The path to the file where user habit data is saved.
    """

    def __init__(self, savefile_path="habithero_savefile.json"):
        """
        Initializes the SaveFileManager object.

        If the savefile doesn't exist at the specified path, it creates an empty one.

        Args:
            savefile_path (str, optional): The path to the savefile. Defaults to "habithero_savefile.json".
        """
        self.savefile_path = savefile_path

        # Check for the existence of the savefile.
        # If it's not present, initialize an empty savefile to prevent issues during future operations.
        if not os.path.exists(self.savefile_path):
            try:
                with open(self.savefile_path, "w") as f:
                    json.dump({}, f)
                logging.info(f"Created an empty savefile at {self.savefile_path}")
            except Exception as e:
                logging.error(f"Error creating an empty savefile at {self.savefile_path}: {str(e)}")

    def save_data(self, user_name, habits_list):
        """
        Save habit data for a specified user.

        This method saves the habit data for a specified user. If the user already exists 
        in the save file, their data is overwritten. Otherwise, a new entry is created.

        Parameters:
        - user_name (str): Name of the user.
        - habits_list (list): List of Habit objects to be saved.

        Returns:
        None

        Raises:
        - IOError: If there's an issue writing to the save file.
        """

        try:
            # Load existing data to merge or overwrite
            data = self._load_all_data()

            # Convert habits to dictionary format for uniformity in saved data
            habits_dict_list = [habit.to_dict() for habit in habits_list]

            # Overwriting or adding new user data
            data[user_name] = habits_dict_list

            # Committing user data to file, choosing to overwrite for simplicity and avoiding partial updates
            with open(self.savefile_path, "w") as f:
                json.dump(data, f)

            logging.info(f"Data for user {user_name} has been successfully saved.")

        except Exception as e:
            logging.error(f"Error while saving data for user {user_name}: {str(e)}")

    def load_data(self, username):
        """
        Loads user data from the save file and converts it to Habit objects.

        Parameters:
            username (str): The name of the user whose data needs to be loaded.

        Returns:
            list: A list of Habit objects for the specified user, or an empty list if the user does not exist.
        """
        try:
            logging.debug("load_data Called")
            data = self._load_all_data()
            logging.debug("All data loaded")

            if username in data:
                logging.debug("Username was found")
                habits_dict_list = data[username]
                logging.debug("Habits where found")

                # Debugging; might be removed after ensuring data integrity
                for habit_dict in habits_dict_list:
                    logging.debug(f"Loaded habit data: {habit_dict}")

                # Convert each habit dictionary back to its object form
                habits_obj_list = [Habit.from_dict(habit_dict) for habit_dict in habits_dict_list]
                logging.info(f"Loaded data for user {username} successfully.")

                return habits_obj_list

            else:
                # This is only for not crashing th
                logging.warning(f"User {username} not found in the data.")
                return []

        except Exception as e:
            logging.error(f"Error while loading data for user {username}: {str(e)}")
            return []  # Return an empty list on error for consistency

    def get_all_users(self):
        """
        Retrieves all the usernames present in the savefile.

        Returns:
            list[str]: A list containing all the usernames, or an empty list if the savefile is empty or an error occurs.
        """
        try:
            data = self._load_all_data()

            # Extracting the usernames (keys) from the loaded data
            users = list(data.keys())
            logging.info(f"Retrieved {len(users)} users from the savefile.")

            return users
        except Exception as e:
            logging.error(f"Error while retrieving user list: {str(e)}")
            return []  # Return an empty list on error

    def _load_all_data(self):
        """
        Internal helper function to load the entire savefile.

        Returns:
            dict: The data from the savefile if loaded successfully, or an empty dictionary on error.
        """
        try:
            with open(self.savefile_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Since we creat the savefile while initiaing the class this should occure unles the user delets the savefile.
            logging.warning(f"Savefile {self.savefile_path} not found. An empty dictionary will be returned.")
            return {}
        except json.JSONDecodeError:
            # Should only occur if the user corrupts the savefile somehow.
            logging.error(f"Error decoding JSON from savefile {self.savefile_path}.")
            return {}
        except Exception as e:
            logging.error(f"Unexpected error while loading savefile {self.savefile_path}: {str(e)}")
            return {}

    def user_exists(self, username):
        """
        Checks if a user exists in the save file.

        Args:
            username (str): The name of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        data = self._load_all_data()
        if username in data:
            return True
        else:
            return False
