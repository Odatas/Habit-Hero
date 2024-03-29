# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:30:26 2023

@author: patri
"""

from habit import Habit
from datetime import datetime
import Analyzer
import wx.lib.agw.aui as aui
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('WXAgg')


class AnalyzeGUI(wx.Frame):

    def __init__(self, habit, parent=None, id=wx.ID_ANY, title="Habit Analysis",
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

        super(AnalyzeGUI, self).__init__(parent, id, title, pos, size, style)

        self.habit = habit

        # Create the notebook
        self.notebook = aui.AuiNotebook(self)
        self.SetSize((800, 600))

        self.streak = StreakAnalysisPanel(self)
        self.notebook.AddPage(self.streak, "Streak")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()

    def create_page(self, title, method):
        panel = wx.Panel(self.notebook, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        result = method()

        # Check if result is a wx.Panel (for graphical representations)
        if isinstance(result, wx.Panel):
            sizer.Add(result, 1, wx.EXPAND)
        else:  # Handle as text content
            st = wx.StaticText(panel, label=str(result))
            sizer.Add(st, 0, wx.ALL, 10)

        panel.SetSizer(sizer)
        self.notebook.AddPage(panel, title)  # This line adds the created panel to the notebook with the given title
        return panel

    def get_average_duration(self):
        avg_duration = Analyzer.average_duration_between_dates(self.habit.logs)
        return f"Average Duration: {avg_duration} days"

    def get_count_performed(self):
        today = datetime.now()
        count = Analyzer.count_performed_in_month(self.habit.logs, today.month, today.year)
        return f"Count Performed this month: {count} times"

    def get_longest_break(self):
        longest_break = Analyzer.longest_break_between_dates(self.habit.logs)
        return f"Longest Break: {longest_break} days"


class StreakAnalysisPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Layout
        self.layout = wx.BoxSizer(wx.VERTICAL)

        # Widgets

        self.habit_name = wx.StaticText(self, label=f"Habit: {self.parent.habit.name}")
        self.habit_goal = wx.StaticText(self, label=f"Goal: {self.parent.habit.goal}")
        self.days_since_start = wx.StaticText(self, label=f"Started habit {self.days_since()} days ago")
        self.current_streak_value = wx.StaticText(self, label=f"Current Streak: {self.get_current_streak()}")
        self.longest_streak_value = wx.StaticText(self, label=f"Longest streak: {self.calculate_longest_streak()}")
        self.streak_broken_value = wx.StaticText(self, label=f"Times streak was broken: {self.calculate_streak_broken()}")
        self.sconsistentcy_rate = wx.StaticText(self, label=f"Consistentcy rate: {self.calculate_consistentcy_rate()}%")

        # Add widgets to the layout
        self.layout.Add(self.habit_name, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.habit_goal, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.days_since_start, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.current_streak_value, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.longest_streak_value, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.streak_broken_value, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.sconsistentcy_rate, 0, wx.ALL | wx.EXPAND, 5)

        # Matplotlib Figure
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Add the matplotlib canvas to the layout
        self.layout.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.draw_timeline()

        # Set the sizer for the panel
        self.SetSizer(self.layout)

    def draw_timeline(self):
        # Sample list of dates for demonstration purposes
        dates = self.parent.habit.logs

        # Convert string dates to datetime objects
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        # Plot each date on the timeline
        self.axes.plot(date_objects, [1] * len(date_objects), '|', markersize=15)

        # Format the x-axis to show dates
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.figure.autofmt_xdate()

        # Hide the y-axis
        self.axes.get_yaxis().set_visible(False)

        # Redraw the canvas
        self.canvas.draw()

    def get_current_streak(self):
        return self.parent.habit.streak

    def calculate_longest_streak(self):
        longest_streak, _ = Analyzer.find_longest_streak(self.parent.habit.logs, self.parent.habit.frequency)
        return longest_streak

    def calculate_streak_broken(self):
        _, streak_broken = Analyzer.find_longest_streak(self.parent.habit.logs, self.parent.habit.frequency)
        return streak_broken

    def calculate_consistentcy_rate(self, rounding=2):
        consistentcy_rate = Analyzer.calculate_consistency_rate(self.parent.habit.logs, self.parent.habit.frequency)
        return round(consistentcy_rate, rounding)

    def days_since(self):
        """
        Calculate the number of days since a given date.

        Returns:
        int: The number of days since the given date.
        """
        given_date = datetime.strptime(self.parent.habit.logs[0], "%Y-%m-%d")
        current_date = datetime.now()
        difference = current_date - given_date
        return difference.days


if __name__ == "__main__":
    app = wx.App(False)
    frame = AnalyzeGUI(Habit("Meditation", "Inner Peace", "Daily", logs=["2023-08-11", "2023-08-12", "2023-08-14", "2023-08-30"]))
    frame.Show(True)
    app.MainLoop()
