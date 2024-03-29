import logging
from datetime import datetime, timedelta


def average_duration_between_dates(dates):
    """
    Calculates the average duration between consecutive dates in a list of dates.

    Parameters:
        dates (list): List of dates in 'YYYY-MM-DD' format.

    Returns:
        float: Average duration in days.
    """
    if not dates or len(dates) < 2:
        return 0
    # Convert strings to datetime objects and sort the dates
    sorted_dates = sorted([datetime.strptime(date, "%Y-%m-%d") for date in dates])
    # Calculate the number of days between consecutive dates
    durations = [(sorted_dates[i] - sorted_dates[i - 1]).days for i in range(1, len(sorted_dates))]

    # Return the average duration, rounded to the nearest whole number
    return round(sum(durations) / len(durations))


def count_performed_in_month(dates, month, year):
    """
    Count the number of times the habit was performed in a specific month.

    Parameters:
        dates (list): List of dates in 'YYYY-MM-DD' format.
        month (int): The month to filter by (1-12).
        year (int): The year to filter by.

    Returns:
        int: The count of dates that fall in the specified month and year.
    """
    return len([date for date in dates if datetime.strptime(date, "%Y-%m-%d").month == month and datetime.strptime(date, "%Y-%m-%d").year == year])


def longest_break_between_dates(dates):
    """
    Finds the longest break (in days) between two consecutive dates in a list of dates.

    Parameters:
        dates (list): List of dates in 'YYYY-MM-DD' format.

    Returns:
        int: The longest break in days.
    """
    if not dates or len(dates) < 2:
        return 0
    sorted_dates = sorted([datetime.strptime(date, "%Y-%m-%d") for date in dates])
    breaks = [(sorted_dates[i] - sorted_dates[i - 1]).days for i in range(1, len(sorted_dates))]
    return max(breaks) if breaks else 0


def days_until_date(target_date_str: str) -> int:
    """
    Returns the number of days until or since the given target date.

    Parameters:
        target_date_str (str): Target date as a string in "YYYY-MM-DD" format.

    Returns:
        int: Number of days until target date. Positive if the target date is in the future, negative if it is in the past.
    """
    try:
        # Convert the string date to a datetime object
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        logging.error(f"Invalid date format: {target_date_str}. Expected format is YYYY-MM-DD.")
        raise e

    # Calculate the difference between target date and current date
    today = datetime.now().date()
    difference = target_date - today
    logging.debug(f"Days until {target_date_str}: {difference.days}")

    # Return the difference in days as an integer
    return difference.days


def find_longest_streak(date_logs: list[str], frequency: str) -> int:
    """
    Calculate the longest consecutive streak from a list of dates based on a given frequency.

    Parameters:
        date_logs (list of str): List of dates in "YYYY-MM-DD" format sorted in ascending order.
        frequency (str): Expected frequency of habit; "Daily", "Weekly", "Monthly", or a digit as a string.

    Returns:
        int: Longest streak of consecutive dates according to the specified frequency.
    """
    longest_streak = 1
    current_streak = 1
    streak_broken = 0

    for i in range(1, len(date_logs)):
        prev_date = datetime.strptime(date_logs[i-1], "%Y-%m-%d")
        curr_date = datetime.strptime(date_logs[i], "%Y-%m-%d")

        if verify_frequency_in_range(curr_date, prev_date, frequency):
            current_streak += 1
        else:

            streak_broken += 1
            current_streak = 1

        longest_streak = max(longest_streak, current_streak, 1)

    return longest_streak, streak_broken


def calculate_consistency_rate(date_logs: list[str], frequency: str):
    """
    Calculate the consistency rate of a habit. Consistentcy Rate is defiend by percented of successfull iterations.

    Parameters:
        date_logs (list[str]): List of dates in "YYYY-MM-DD" format.
        frequency (str): Expected frequency of habit; "Daily", "Weekly", "Monthly", or a digit as a string.

    Returns:
        float: The consistency rate as a percentage.
    """
    longest_streak, times_streak_broken = find_longest_streak(date_logs, frequency)
    total_days_tracked = len(date_logs)

    if total_days_tracked == 0:
        return 0.0

    if total_days_tracked == 1:
        return 100.0

    # Assuming a streak is valid only if it's longer than 1 day
    valid_streak_days = sum(1 for _ in range(times_streak_broken, total_days_tracked) if longest_streak > 1)
    successful_days = valid_streak_days
    consistency_rate = (successful_days / total_days_tracked) * 100 if total_days_tracked > 0 else 0
    return consistency_rate


def next_habit_due(last_performed_str: str, frequency: str) -> str:
    """
    Checks if the habit is overdue based on the last performed date and frequency.

    Parameters:
        last_performed_str (str): Last date the habit was performed, in 'YYYY-MM-DD' format.
        frequency (str): Expected frequency of the habit; can be "Daily", "Weekly", "Monthly", or a digit as a string representing days.
        today_str (str): Optional. The date to check, in 'YYYY-MM-DD' format. Defaults to the current date.

    Returns:
        bool: True if the habit is overdue, False otherwise.
    """
    logging.debug("Analyzer.next_habit_due called")
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    last_performed = datetime.strptime(last_performed_str, "%Y-%m-%d")

    logging.debug(f"Analyzer.next_habit_due frequency {frequency}")

    # Based on the frequency we need to do different things.
    if frequency == 'Daily':
        due_date = last_performed + timedelta(days=1)

    elif frequency == "Weekly" or frequency == "Monthly":
        if frequency == "Weekly":
            check_range = 15
        else:
            check_range = 63  # Max days of two consecutiv months. Happening for juli and dcember and the onth after.
        last_true = None
        # To find the next due date we will iterate through all possible dates until we find the first one that doesnt fit.
        # The one before is our new due date.
        for i in range(check_range):
            possible_due_date = last_performed + timedelta(days=i)
            debug_string = f"possible_due_date {str(possible_due_date)}, last performed: {str(last_performed)}"
            logging.debug(debug_string)
            if verify_frequency_in_range(possible_due_date, last_performed, frequency):
                last_true = possible_due_date
            else:
                due_date = last_true
                break
    # Every x days
    elif "Days" in frequency:
        number_frequency = int(frequency.split(" ")[1])
        due_date = last_performed + timedelta(days=number_frequency)

    # Every Weekday. Maybe using a table to switch from frequceny string to an id would have been smarter.
    elif "Days" not in frequency and "Every" in frequency:
        weekday = frequency.split(" ")[1]
        for i in range(1, 8):
            due_date = last_performed + timedelta(days=i)
            logging.debug(f"Analyezer.next_habit_due weekday {due_date.strftime('%A')}")
            if weekday == due_date.strftime('%A'):
                return due_date.strftime("%Y-%m-%d")
        logging.error("Analyezer.next_habit_due 8 days were checked but due_date was not found.")
    else:
        raise ValueError("No matching frequency found.")
        return None

    logging.debug("Returning " + due_date.strftime("%Y-%m-%d"))
    return due_date.strftime("%Y-%m-%d")


def verify_frequency_in_range(curr_date: datetime, prev_date: datetime, frequency: str, strict: bool = False) -> bool:
    """
    Verify if the timespan between two date matches the given frequency.

    Parameters:
        curr_date (datetime): The current date.
        prev_date (datetime): The previous date.
        frequency (str): The desired frequency (e.g., 'Daily', 'Weekly', 'Monthly', '3 Days', 'Every Monday').
        strict (bool): Whether the frequency verification should be strict or not. Doesnt apply to all cases.

    Returns:
        bool: True if the two dates are in the desired range, False otherwise.
    """
    logging.debug("Analyzer.verify_frequency_in_range called")
    # Daily is easy.
    if frequency == "Daily":
        logging.debug("Analyzer.verify_frequency_in_range Frequency Daily")
        delta_days = (curr_date - prev_date).days
        if abs(delta_days) == 1:
            return True
        else:
            return False

    # Check if both week numbers are one apart.
    elif frequency == "Weekly":
        logging.debug("Analyzer.verify_frequency_in_range Frequency Weekly")
        _, curr_week, _ = curr_date.isocalendar()
        _, prev_week, _ = prev_date.isocalendar()
        # Some years have 52 weeks and some 53.
        # For years with 53 weeks user wont get penelized for not loggig an action in the last week.
        # <= 1 because doing it twice in the same week should not provide a negative
        if curr_week - prev_week <= 1 or (curr_week == 1 and (prev_week == 52 or prev_week == 53)):
            return True
        else:
            return False

    # Callculate the ammount of months since year 0 and see if the difference is one
    elif frequency == "Monthly":
        logging.debug("Analyzer.verify_frequency_in_range Frequency Monthly")
        curr_month = curr_date.month
        curr_year = curr_date.year
        prev_month = prev_date.month
        prev_year = prev_date.year
        total_curr_months = curr_year * 12 + curr_month
        total_prev_months = prev_year * 12 + prev_month

        delta_months = total_curr_months - total_prev_months

        if delta_months <= 1:
            return True
        else:
            return False

    # Every x days.
    # Get delta of days and see if they match the frequency number.
    # Strict means it needs to be exactly X days.
    elif "Days" in frequency:
        logging.debug("Frequency every x days")
        number_frequency = int(frequency.split(" ")[1])
        if strict is None:
            logging.error("Strict has no value.")
            raise ValueError("Strict Value missing.")
        delta_days = (curr_date - prev_date).days
        if strict:
            return delta_days == number_frequency
        else:
            return delta_days <= number_frequency

    # Weekday.
    elif "Days" not in frequency and "Every" in frequency:
        logging.debug("Frequenccy Weekday")
        weekday = frequency.split(" ")[1]
        today = datetime.today().strftime('%A')
        if (curr_date - prev_date).days > 7:
            return False
        return today == weekday

    else:
        logging.error("Frequency Value Error")
        raise ValueError("No matching frequency found.")
