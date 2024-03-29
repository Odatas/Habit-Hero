from MainMenuGUI import MainMenuGUIFrame
from saveFileManager import SaveFileManager
from habit import Habit
import wx
import logging


class Orchestrator:
    """
    Manages the overall functionality of the habit tracking application.

    This class is responsible for initializing and managing the main components of the application, 
    including handling habits, user data, and the graphical user interface.

    The Orchestrator class interacts with the SaveFileManager for data persistence and provides 
    methods to manage habits and user data.
    """

    def __init__(self):
        """
        Initializes the Orchestrator, setting up the list of habits, FileManager, and starting the GUI loop.
        """
        logging.info("Initializing Orchestrator.")
        self.habits = []
        self.SaveFileManager = SaveFileManager()
        self.UserName = ""

        # Launching the wx App to handle GUI operations
        self.app = wx.App(False)
        self.main_menu = MainMenuGUIFrame(None, "Habit Hero", self)
        self.app.MainLoop()

    def set_username(self, Username):
        """
        Sets the username for the current session.

        Parameters:
            Username (str): The desired username.
        """
        logging.info(f"Setting username to {Username}.")
        self.Username = Username

    def delete_habit(self, index):
        """
        Deletes a habit based on its index in the list.

        Parameters:
            index (int): The index of the habit to be deleted.
        """

        logging.info(f"Deleting habit at index {index}.")
        del self.habits[index]
        self.update_data()

    def get_users(self):
        """
        Fetches all users from the SaveFileManager.

        Returns:
            list: A list of all user names.
        """

        logging.info("Fetching all users.")
        return self.SaveFileManager.get_all_users()

    def create_new_user(self, user):
        """
        Creates a new user and saves an empty data set for them.

        Parameters:
            user (str): The name of the new user.
        """

        logging.info(f"Creating new user: {user}.")
        self.UserName = user
        self.SaveFileManager.save_data(user, [])

    def load_user_data(self, user):
        """
        Loads the data associated with a given user.

        Parameters:
            user (str): The name of the user whose data is to be loaded.
        """
        logging.debug("Called load_user_data")
        logging.info(f"Loading data for user: {user}.")
        self.UserName = user
        self.habits = self.SaveFileManager.load_data(user)
        self.refresh_main_menu_list()

    def save_data(self):
        """
        Saves the current data of habits for the user.
        """
        logging.info(f"Saving data for user: {self.UserName}.")
        try:
            self.SaveFileManager.save_data(self.UserName, self.habits)
            logging.info(f"Data saved successfully for user: {self.UserName}")
        except Exception as e:
            logging.error(f"Error occurred while saving data for user: {self.UserName}. Error: {str(e)}")

    def create_new_habit(self, name, goal, frequency, start_date=None, strict=False):
        """
        Creates a new habit and adds it to the list of habits.

        Parameters:
            name (str): The name of the habit.
            goal (str): The goal or description of the habit.
            frequency (str): How often the habit should be performed.
            start_date (str, optional): The start date of the habit.
            strict (bool, optional): Whether the habit should be strictly adhered to its frequency.

        Returns:
            Habit: The created Habit object.
        """
        logging.info(f"Creating new habit: {name}. Goal: {goal}. Frequency: {frequency}. Start Date: {start_date}. Strict: {strict}.")
        new_habit = Habit(name=name, goal=goal, frequency=frequency, start_date=start_date, strict=strict)
        self.habits.append(new_habit)
        self.update_data()

    def refresh_main_menu_list(self):
        """
        Refreshes the ListCtrl in MainMenuGUI by deleting all entries and repopulating with data from self.habits.
        """
        logging.info("Refreshing main menu list.")
        self.main_menu.data_view.DeleteAllItems()
        for habit in self.habits:
            self.main_menu.add_habit_to_data_view(habit)

    def perform_habit_today(self, index):
        """
        Marks a habit as performed for the current day based on its index.

        Parameters:
            index (int): The index of the habit to be marked as performed.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure, and an error message if applicable.
        """
        result, errortext = self.habits[index].perform_habit_today()
        if not result:
            wx.MessageBox(errortext, "Warning", wx.OK | wx.ICON_WARNING)
        else:
            self.update_data()

    def update_data(self):
        """
        Saves the current data and refreshes the main menu list with updated habit information.
        """
        self.save_data()
        self.refresh_main_menu_list()

    def get_habit_by_index(self, index):
        """
        Retrieves a habit object by its index in the list.

        Parameters:
            index (int): The index of the habit.

        Returns:
            Habit: The habit object at the specified index.
        """
        return self.habits[index]


def set_up_logging():
    """
    Sets up logging configuration for the application.

    Logging is directed to both a file ('app.log') and the console.
    """
    logging_level = logging.INFO
    logger = logging.getLogger()
    logger.setLevel(logging_level)  # Set root logger level

    # This ensures we don't re-add handlers in case this method is called multiple times
    if not logger.hasHandlers():
        # Directing logs to a file for persistence
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging_level)

        # Sending logs to console to have immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)

        # Formatting logs to provide a timestamp, severity, and the log message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


if __name__ == "__main__":
    # Setting up logging ensures logs are captured from the very start
    set_up_logging()

    # Launch the Orchestrator. Using a try-finally ensures that even if an error occurs,
    # the logging system shuts down gracefully.
    try:
        Orchestrator()
    finally:
        logging.shutdown()
