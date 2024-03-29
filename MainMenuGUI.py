import wx
from datetime import datetime
from AddHabit import AddHabitFrame
from UserSelection import UserSelectionFrame
import logging
import Analyzer
import HabitAnalyzerGUI


class MainMenuGUIFrame(wx.Frame):

    def __init__(self, parent, title, Orchestrator):
        """Initialize the MainMenuGUIFrame with a given title and orchestrator."""
        super(MainMenuGUIFrame, self).__init__(parent, title=title, size=(800, 400))

        self.Orchestrator = Orchestrator
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # 1. Reihe: Text in Überschrift Größe "Habit Hero"
        header = wx.StaticText(panel, label="Habit Hero")
        header.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        box.Add(header, flag=wx.EXPAND | wx.ALL, border=10)

        # 2. Reihe: Today: <Aktuelles Datum>
        today = datetime.now().strftime('%Y-%m-%d')
        date_label = wx.StaticText(panel, label=f"Today: {today}")
        box.Add(date_label, flag=wx.EXPAND | wx.ALL, border=10)

        # 3. Reihe: List_Ctrl
        self.data_view = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.data_view.InsertColumn(0, "Habit")
        self.data_view.InsertColumn(1, "Frequency")
        self.data_view.InsertColumn(2, "Start Date")
        self.data_view.InsertColumn(3, "Last Date")
        self.data_view.InsertColumn(4, "Next Due Date")
        self.data_view.InsertColumn(5, "Days until Due")
        self.data_view.InsertColumn(6, "Streak")

        self.data_view.SetColumnWidth(0, 300)
        self.data_view.SetColumnWidth(2, 100)
        self.data_view.SetColumnWidth(3, 100)
        self.data_view.SetColumnWidth(4, 100)

        box.Add(self.data_view, 1, flag=wx.EXPAND | wx.ALL, border=10)  # Note the "1" here

        # 4. Reihe: Buttons
        button_box = wx.BoxSizer(wx.HORIZONTAL)

        perform_now_button = wx.Button(panel, label="Perform Now")
        perform_now_button.Bind(wx.EVT_BUTTON, self.on_perform)
        button_box.Add(perform_now_button, proportion=1)

        # Todo Add a button to select a date to perform.
        # perform_on_date = wx.Button(panel, label="Perform on Date")
        # perform_on_date_button.Bind(wx.EVT_Button,)

        new_button = wx.Button(panel, label="New Habit")
        new_button.Bind(wx.EVT_BUTTON, self.on_new)
        button_box.Add(new_button, proportion=1)

        edit_button = wx.Button(panel, label="Edit")
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        button_box.Add(edit_button, proportion=1)

        remove_button = wx.Button(panel, label="Remove")
        remove_button.Bind(wx.EVT_BUTTON, self.on_remove)
        button_box.Add(remove_button, proportion=1)

        analyze_button = wx.Button(panel, label="Analytics")
        analyze_button.Bind(wx.EVT_BUTTON, self.on_analyze)
        button_box.Add(analyze_button, proportion=1)

        box.Add(button_box, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(box)

        UserSelectionFrame(self, self.Orchestrator)

        self.Centre()
        # elf.Show(True)

    def add_habit_to_data_view(self, habit):
        """
        Adds a habit to the DataViewListCtrl.

        Parameters:
            habit (Habit): The habit object containing the details to be added.

        """
        # Extract the attributes from the habit object.
        name = habit.name
        frequency = habit.frequency
        start_date = habit.start_date
        last_perfomed = habit.get_last_performed()
        next_due_date = habit.next_due_date
        days_until_due = Analyzer.days_until_date(next_due_date)
        if days_until_due < 0:
            streak = 0
            habit.streak = 0
            self.Orchestrator.save_data()
        else:
            streak = habit.streak

        # Append a new row to the DataViewListCtrl.
        self.data_view.Append([name, frequency, start_date, last_perfomed, next_due_date, days_until_due, streak])

        self.data_view.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.data_view.SetColumnWidth(1, wx.LIST_AUTOSIZE)  # Assuming you have a second column
        self.data_view.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.data_view.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        self.data_view.SetColumnWidth(4, wx.LIST_AUTOSIZE)

    def on_analyze(self, event):
        selection = self.data_view.GetNextSelected(-1)
        if selection == -1:  # Check if no row is selected
            wx.MessageBox("Please select a habit to edit!", "Warning", wx.OK | wx.ICON_WARNING)
            return
        selected_habit = self.Orchestrator.get_habit_by_index(selection)
        HabitAnalyzerGUI.AnalyzeGUI(selected_habit, title=selected_habit.name)

    def on_new(self, event):
        AddHabitFrame(self, self.Orchestrator, title="Add new habbit")

    def on_edit(self, event):
        selection = self.data_view.GetNextSelected(-1)
        if selection == -1:  # Check if no row is selected
            wx.MessageBox("Please select a habit to edit!", "Warning", wx.OK | wx.ICON_WARNING)
            return
        AddHabitFrame(self, self.Orchestrator, habit=self.Orchestrator.habits[selection], title="Edit habbit")

    def on_remove(self, event):
        # Get the selected habit
        selection = self.data_view.GetNextSelected(-1)
        if selection == -1:  # Check if no row is selected
            wx.MessageBox("Please select a habit to remove!", "Warning", wx.OK | wx.ICON_WARNING)
            return

        # Confirm the removal with the user
        dlg = wx.MessageDialog(self, "Are you sure you want to remove this habit? You can't restore the data once it's deleted.",
                               "Confirm Deletion", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() == wx.ID_YES:

            self.data_view.DeleteItem(selection)
            self.Orchestrator.delete_habit(selection)

        dlg.Destroy()

    def on_perform(self, event):
        """Handles the Perform Now action."""
        logging.info("Perform Now button pressed.")
        # Get the selected habit
        selection = self.data_view.GetNextSelected(-1)
        if selection == -1:  # Check if no row is selected
            wx.MessageBox("Please select a habit to perform now!", "Warning", wx.OK | wx.ICON_WARNING)
            return

        logging.info(f"Performing habit at row: {selection}")
        self.Orchestrator.perform_habit_today(selection)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainMenuGUIFrame(None, "Habit Hero", None)
    app.MainLoop()
