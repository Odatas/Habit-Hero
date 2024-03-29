import wx
import wx.adv

from datetime import datetime


class AddHabitFrame(wx.Frame):
    """
    A GUI frame for adding or editing a habit using wxPython.

    This frame allows the user to input details for a new habit or edit an existing one.
    It includes fields for the habit's name, goal, frequency, strictness, and start date.
    If an existing habit is being edited, the frame is initialized with the habit's current details.

    Parameters:
        parent (wx.Window): The parent window.
        Orchestrator (Orchestrator): An instance of the Orchestrator class.
        habit (Habit, optional): An existing habit to be edited. Defaults to None.
        title (str, optional): The title of the frame. Defaults to "Add New Habit".
    """

    def __init__(self, parent, Orchestrator, habit=None, title="Add New Habit"):
        super(AddHabitFrame, self).__init__(parent, title=title, size=(500, 400))
        panel = wx.Panel(self)
        self.habit = habit
        self.Orchestrator = Orchestrator

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer = main_sizer

        # Name
        self.name_label = wx.StaticText(panel, label="Habit Name:")
        self.name_text = wx.TextCtrl(panel)
        main_sizer.Add(self.name_label, 0, wx.ALL, 5)
        main_sizer.Add(self.name_text, 0, wx.ALL | wx.EXPAND, 5)

        # Goal
        self.goal_label = wx.StaticText(panel, label="Goal:")
        self.goal_text = wx.TextCtrl(panel)
        main_sizer.Add(self.goal_label, 0, wx.ALL, 5)
        main_sizer.Add(self.goal_text, 0, wx.ALL | wx.EXPAND, 5)

        # Frequency
        self.frequency_label = wx.StaticText(panel, label="Frequency:")
        choices = ['Daily', 'Weekly', 'Monthly', 'Every Monday', 'Every Tuesday', 'Every Wednesday',
                   'Every Thursday', 'Every Friday', 'Every Saturday', 'Every Sunday', 'Every X Days']
        self.frequency_choice = wx.Choice(panel, choices=choices)
        self.frequency_choice.Select(0)
        self.frequency_choice.Bind(wx.EVT_CHOICE, self.on_frequency_choice)
        main_sizer.Add(self.frequency_label, 0, wx.ALL, 5)
        main_sizer.Add(self.frequency_choice, 0, wx.ALL | wx.EXPAND, 5)

        # Days entry and Strict checkbox (hidden by default)
        self.days_strict_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.days_label = wx.StaticText(panel, label="Enter number of days:")
        self.days_text = wx.TextCtrl(panel)
        self.strict_checkbox = wx.CheckBox(panel, label='Strict')
        self.strict_checkbox.SetToolTip(
            "By checking this checkbox, the habit must be performed exactly on the due date. Performing it earlier will not count.")

        self.days_strict_sizer.Add(self.days_label, 0, wx.ALL, 5)
        self.days_strict_sizer.Add(self.days_text, 0, wx.ALL, 5)
        self.days_strict_sizer.Add(self.strict_checkbox, 0, wx.ALL, 5)

        self.days_label.Show(False)
        self.days_text.Show(False)
        self.strict_checkbox.Show(False)

        main_sizer.Add(self.days_strict_sizer, 0, wx.EXPAND)

        # Start Date
        self.start_date_label = wx.StaticText(panel, label="First Performed:")
        self.start_date_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN)
        main_sizer.Add(self.start_date_label, 0, wx.ALL, 5)
        main_sizer.Add(self.start_date_picker, 0, wx.ALL | wx.EXPAND, 5)

        # If we have a habit then we initialize the "Save" button instead of "Add Habit"
        # and load the existing Data into the GUI.
        if self.habit:
            save_btn = wx.Button(panel, label="Save")
            save_btn.Bind(wx.EVT_BUTTON, self.on_save)
            main_sizer.Add(save_btn, 0, wx.ALL | wx.CENTER, 5)

            self.name_text.SetValue(self.habit.name)
            self.goal_text.SetValue(self.habit.goal)
            self.frequency_choice.SetStringSelection(self.habit.frequency)
            self.strict_checkbox.SetValue(self.habit.strict)

            date_obj = datetime.strptime(self.habit.start_date, "%Y-%m-%d").date()
            self.start_date_picker.SetValue(wx.DateTime(date_obj.day, date_obj.month - 1, date_obj.year))
        else:
            submit_btn = wx.Button(panel, label="Add Habit")
            submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
            main_sizer.Add(submit_btn, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(main_sizer)

        self.Show()

    def on_save(self, event=None):
        """
        Handles the saving of an edited habit.

        Gathers the habit details from the input fields, updates the habit, and saves it
        using the Orchestrator. Also, refreshes the main menu list and closes the frame.

        Parameters:
            event (wx.Event, optional): The event object. Defaults to None.
        """

        new_name = self.name_text.GetValue()
        new_goal = self.goal_text.GetValue()
        new_frequency = self.frequency_choice.GetString(self.frequency_choice.GetSelection())
        self.habit.edit_habit(new_name, new_goal, new_frequency)
        self.habit.next_due_date = self.habit.calculate_next_due_date()
        self.Orchestrator.save_data()
        self.Orchestrator.refresh_main_menu_list()
        self.Close()

    def on_frequency_choice(self, event):
        """
        Event handler for selecting a frequency option.

        Shows or hides the visibility of the 'Every X Days' related fields.

        Parameters:
            event (wx.Event): The event object.
        """

        selection = self.frequency_choice.GetString(self.frequency_choice.GetSelection())
        if selection == 'Every X Days':
            self.days_label.Show(True)
            self.days_text.Show(True)
            self.strict_checkbox.Show(True)
        else:
            self.days_label.Show(False)
            self.days_text.Show(False)
            self.strict_checkbox.Show(False)

        self.main_sizer.Layout()

    def on_submit(self, event):
        """
        Handles the submission of a new habit.

        Validates and gathers the input data, creates a new habit through the Orchestrator,
        and closes the frame.

        Parameters:
            event (wx.Event): The event object.

        """

        name = self.name_text.GetValue()
        goal = self.goal_text.GetValue()

        # Get the indexx of the choiche and then the choice as string from the index.
        frequency = self.frequency_choice.GetString(self.frequency_choice.GetSelection())
        strict = self.strict_checkbox.GetValue()

        # DatepickerCtrl needs to be set into specific format to match the format of the habit class.
        # TODO for spicific frequencys we need to set the date according to the frequency.
        start_date_wx = self.start_date_picker.GetValue()
        start_date = start_date_wx.FormatISODate()

        # Check if required fields are filled
        if not name:
            wx.MessageBox("Please enter a name for the habit.", "Error", wx.OK | wx.ICON_ERROR)
            return
        if not frequency:
            wx.MessageBox("Please select a frequency.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # For the option "Every X Days" we show a textctrl and need to make sure if that the entry is a number
        # However for the habit class we need the field to be a string. Madness!
        if frequency == 'Every X Days':
            days = self.days_text.GetValue()
            if not days.isdigit():
                wx.MessageBox("Please enter a valid number for 'Every X Days'.", "Error", wx.OK | wx.ICON_ERROR)
                return
            frequency = f'Every {days} Days'

        # The Orchestrator will also refresh the GUI
        if self.Orchestrator:
            self.Orchestrator.create_new_habit(name, goal, frequency, start_date=start_date, strict=strict)

        self.Close()


#
if __name__ == "__main__":
    app = wx.App(False)
    frame = AddHabitFrame(None, None)
    app.MainLoop()
