# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 20:34:07 2024

@author: patri
"""

import unittest

from datetime import datetime, timedelta

from Analyzer import longest_break_between_dates
from Analyzer import count_performed_in_month
from Analyzer import average_duration_between_dates
from Analyzer import days_until_date
from Analyzer import find_longest_streak
from Analyzer import calculate_consistency_rate
from Analyzer import next_habit_due
from Analyzer import verify_frequency_in_range


class TestAverageDurationBetweenDates(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(average_duration_between_dates([]), 0)

    def test_single_date(self):
        self.assertEqual(average_duration_between_dates(["2024-03-11"]), 0)

    def test_multiple_dates(self):
        dates = ["2024-03-11", "2024-03-15", "2024-03-20"]
        self.assertEqual(average_duration_between_dates(dates), 4)

    def test_unsorted_dates(self):
        dates = ["2024-03-20", "2024-03-11", "2024-03-15"]
        self.assertEqual(average_duration_between_dates(dates), 4)

    def test_same_dates(self):
        dates = ["2024-03-11", "2024-03-11", "2024-03-11"]
        self.assertEqual(average_duration_between_dates(dates), 0)

    def test_large_date_range(self):
        dates = ["2020-01-01", "2023-01-01", "2024-01-01"]
        self.assertEqual(average_duration_between_dates(dates), 730)  # 3 years, average 730 days per year


class TestCountPerformedInMonth(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(count_performed_in_month([], 1, 2024), 0)

    def test_no_match_dates(self):
        dates = ["2023-12-31", "2024-02-01"]
        self.assertEqual(count_performed_in_month(dates, 1, 2024), 0)

    def test_all_match_dates(self):
        dates = ["2024-01-01", "2024-01-15", "2024-01-31"]
        self.assertEqual(count_performed_in_month(dates, 1, 2024), 3)

    def test_some_match_dates(self):
        dates = ["2024-01-01", "2023-01-15", "2024-02-01"]
        self.assertEqual(count_performed_in_month(dates, 1, 2024), 1)

    def test_end_of_year(self):
        dates = ["2023-12-31", "2024-01-01"]
        self.assertEqual(count_performed_in_month(dates, 12, 2023), 1)

    def test_beginning_of_year(self):
        dates = ["2023-12-31", "2024-01-01"]
        self.assertEqual(count_performed_in_month(dates, 1, 2024), 1)


class TestLongestBreakBetweenDates(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(longest_break_between_dates([]), 0)

    def test_single_date(self):
        self.assertEqual(longest_break_between_dates(["2024-03-11"]), 0)

    def test_multiple_dates(self):
        dates = ["2024-03-11", "2024-03-15", "2024-03-25"]
        self.assertEqual(longest_break_between_dates(dates), 10)

    def test_unsorted_dates(self):
        dates = ["2024-03-25", "2024-03-11", "2024-03-15"]
        self.assertEqual(longest_break_between_dates(dates), 10)

    def test_no_break(self):
        dates = ["2024-03-11", "2024-03-12", "2024-03-13"]
        self.assertEqual(longest_break_between_dates(dates), 1)

    def test_large_breaks(self):
        dates = ["2020-01-01", "2022-01-01", "2023-01-01"]
        self.assertEqual(longest_break_between_dates(dates), 731)  # Leap year included


class TestDaysUntilDate(unittest.TestCase):

    def test_future_date(self):
        future_date = datetime.now().date() + timedelta(days=5)
        self.assertEqual(days_until_date(future_date.strftime("%Y-%m-%d")), 5)

    def test_past_date(self):
        past_date = datetime.now().date() - timedelta(days=5)
        self.assertEqual(days_until_date(past_date.strftime("%Y-%m-%d")), -5)

    def test_current_date(self):
        current_date = datetime.now().date()
        self.assertEqual(days_until_date(current_date.strftime("%Y-%m-%d")), 0)

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            days_until_date("invalid-date")


class TestFindLongestStreak(unittest.TestCase):

    def test_daily_frequency(self):
        dates = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-05"]
        longest_streak, breaks = find_longest_streak(dates, "Daily")
        self.assertEqual(longest_streak, 3)
        self.assertEqual(breaks, 1)

    def test_weekly_frequency(self):
        dates = ["2024-01-01", "2024-01-08", "2024-01-15", "2024-01-29"]
        longest_streak, breaks = find_longest_streak(dates, "Weekly")
        self.assertEqual(longest_streak, 3)
        self.assertEqual(breaks, 1)

    def test_monthly_frequency(self):
        dates = ["2024-01-01", "2024-02-01", "2024-03-01", "2024-05-01"]
        longest_streak, breaks = find_longest_streak(dates, "Monthly")
        self.assertEqual(longest_streak, 3)
        self.assertEqual(breaks, 1)

    def test_numeric_frequency(self):
        dates = ["2024-01-01", "2024-01-03", "2024-01-08", "2024-01-09"]
        longest_streak, breaks = find_longest_streak(dates, "Every 2 Days")
        self.assertEqual(longest_streak, 2)
        self.assertEqual(breaks, 1)

    def test_empty_dates_list(self):
        longest_streak, breaks = find_longest_streak([], "Daily")
        self.assertEqual(longest_streak, 1)
        self.assertEqual(breaks, 0)

    def test_single_date(self):
        longest_streak, breaks = find_longest_streak(["2024-01-01"], "Daily")
        self.assertEqual(longest_streak, 1)
        self.assertEqual(breaks, 0)

    def test_invalid_frequency(self):
        with self.assertRaises(ValueError):
            find_longest_streak(["2024-01-01", "2024-01-02"], "Annually")


class TestCalculateConsistencyRate(unittest.TestCase):

    def test_normal_case_daily(self):
        dates = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-05"]
        rate = calculate_consistency_rate(dates, "Daily")
        self.assertEqual(rate, 75.0)  # 3 successful days, 1 break

    def test_normal_case_weekly(self):
        dates = ["2024-01-01", "2024-01-08", "2024-01-15", "2024-01-22", "2024-02-05"]
        rate = calculate_consistency_rate(dates, "Weekly")
        self.assertEqual(rate, 80.0)  # 4 successful weeks, 1 break

    def test_empty_dates_list(self):
        rate = calculate_consistency_rate([], "Daily")
        self.assertEqual(rate, 0.0)

    def test_single_date(self):
        rate = calculate_consistency_rate(["2024-01-01"], "Daily")
        self.assertEqual(rate, 100.0)  # 1 day tracked, no break

    def test_all_broken_streaks(self):
        dates = ["2024-01-01", "2024-01-05", "2024-01-10"]
        rate = calculate_consistency_rate(dates, "Daily")
        self.assertEqual(rate, 0.0)  # All days are breaks


class TestNextHabitDue(unittest.TestCase):

    def setUp(self):
        self.today = datetime.now().strftime("%Y-%m-%d")

    def test_daily_frequency(self):
        last_performed = "2024-01-01"
        frequency = "Daily"
        expected_due_date = "2024-01-02"
        self.assertEqual(next_habit_due(last_performed, frequency), expected_due_date)

    def test_weekly_frequency(self):
        last_performed = "2024-01-01"
        frequency = "Weekly"
        expected_due_date = "2024-01-14"
        self.assertEqual(next_habit_due(last_performed, frequency), expected_due_date)

    def test_monthly_frequency(self):
        last_performed = "2024-01-01"
        frequency = "Monthly"
        expected_due_date = "2024-02-29"  # Last day of the next months. Leap year in 2024.
        self.assertEqual(next_habit_due(last_performed, frequency), expected_due_date)

    def test_specific_days_frequency(self):
        last_performed = "2024-01-01"
        frequency = "Every 3 Days"
        expected_due_date = "2024-01-04"
        self.assertEqual(next_habit_due(last_performed, frequency), expected_due_date)

    def test_weekday_frequency(self):
        last_performed = "2024-01-01"  # Assuming this is a Tuesday
        frequency = "Every Monday"
        expected_due_date = "2024-01-08"  # The following Monday
        self.assertEqual(next_habit_due(last_performed, frequency), expected_due_date)

    def test_invalid_frequency(self):
        last_performed = "2024-01-01"
        frequency = "Annually"
        with self.assertRaises(ValueError):
            next_habit_due(last_performed, frequency)


class TestFrequencyInRange(unittest.TestCase):

    def test_daily_frequency(self):
        # Test for Daily frequency
        self.assertTrue(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 22), "Daily"))
        self.assertFalse(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 21), "Daily"))

    def test_weekly_frequency(self):
        # Test for Weekly frequency
        self.assertTrue(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 16), "Weekly"))
        self.assertFalse(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 15), "Weekly"))

    def test_monthly_frequency(self):
        # Test for Monthly frequency
        self.assertTrue(verify_frequency_in_range(datetime(2024, 3, 1), datetime(2024, 2, 1), "Monthly"))
        self.assertFalse(verify_frequency_in_range(datetime(2024, 3, 1), datetime(2024, 1, 30), "Monthly"))

    def test_custom_day_frequency(self):
        # Test for every X days frequency
        self.assertTrue(verify_frequency_in_range(datetime(2024, 3, 20), datetime(2024, 3, 10), "Every 10 Days"))
        self.assertFalse(verify_frequency_in_range(datetime(2024, 3, 20), datetime(2024, 3, 9), "Every 10 Days"))

    def test_weekday_frequency(self):
        # Assuming today is Friday, 23rd March 2024
        self.assertTrue(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 16), "Every Friday"))
        self.assertFalse(verify_frequency_in_range(datetime(2024, 3, 23), datetime(2024, 3, 15), "Every Friday"))


if __name__ == '__main__':
    unittest.main()
