# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 12:35:39 2023

@author: patri
"""

import wx
import logging


class UserSelectionFrame(wx.Frame):
    def __init__(self, parent, Orchestrator, title="Select or Add User"):
        """
        Initializes the UserSelectionFrame which allows selection or addition of users.

        Args:
            parent (wx.Window): Parent window.
            Orchestrator (Orchestrator): Orchestrator object.
            title (str, optional): Title for the frame.
        """
        super(UserSelectionFrame, self).__init__(parent, title=title, size=(300, 200))
        logging.info("Initializing UserSelectionFrame.")

        self.panel = wx.Panel(self)
        self.parent = parent
        self.Orchestrator = Orchestrator
        self.layout_widgets()
        self.Center()

    def layout_widgets(self):
        """Lays out the widgets in the frame."""
        logging.debug("Laying out widgets in UserSelectionFrame.")

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create static text to prompt user
        prompt = wx.StaticText(self.panel, label="Select an existing user or add a new one:")
        main_sizer.Add(prompt, 0, wx.ALL | wx.CENTER, 10)

        # ComboBox for users
        user_list = self.Orchestrator.get_users()
        user_list.append("")
        self.user_combobox = wx.ComboBox(self.panel, choices=user_list, style=wx.CB_READONLY)
        self.user_combobox.Bind(wx.EVT_COMBOBOX, self.on_user_select)
        main_sizer.Add(self.user_combobox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Input box for new user
        new_user_label = wx.StaticText(self.panel, label="Or enter new user name:")
        self.new_user_textctrl = wx.TextCtrl(self.panel)
        self.new_user_textctrl.Bind(wx.EVT_TEXT, self.on_text_entry)
        main_sizer.Add(new_user_label, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(self.new_user_textctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Buttons
        self.btn_ok = wx.Button(self.panel, label="OK")
        self.btn_cancel = wx.Button(self.panel, label="Cancel")

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.btn_ok, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.btn_cancel, 0, 0, 0)

        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)

        # Bind events
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.panel.SetSizer(main_sizer)
        self.Show()

    def on_user_select(self, event):
        """Handles event when a user is selected from the dropdown.

        Args:
            event (wx.Event): The event object.
        """
        logging.debug("Combobox Set.")
        # Clear the TextCtrl for new user names to signal that data from the selected, existing user is now active.
        self.new_user_textctrl.SetValue("")
        event.Skip()

    def on_text_entry(self, event):
        """Handles event when text is entered.

        Args:
            event (wx.Event): The event object.
        """
        logging.debug("Textctrl set.")
        # Reset the user combobox value to empty when text is entered into the new_user_textctrl to signal that a new user will be created.
        if self.new_user_textctrl.GetValue() != "":
            self.user_combobox.SetValue("")
        event.Skip()

    def on_ok(self, event):
        """Handles the OK button event.

        Args:
            event (wx.Event): The event object.
        """
        logging.debug("OK button pressed.")
        selected_user = self.user_combobox.GetValue()
        new_user = self.new_user_textctrl.GetValue()

        # We can rely on the fact that only one of the widgets is filled with a user.
        # Depending on which widget we load existing data or creat a new user.
        if selected_user:
            logging.info(f"User selected: {selected_user}.")
            self.Orchestrator.load_user_data(selected_user)
            self.parent.Show()
            self.Destroy()
        elif new_user:
            logging.info(f"New user added: {new_user}.")
            self.Orchestrator.create_new_user(new_user)
            self.parent.Show()
            self.Destroy()
        else:
            logging.warning("No user selected or entered.")
            wx.MessageBox("Please select a user or enter a new user name.", "Warning", wx.OK | wx.ICON_WARNING)

    def on_cancel(self, event):
        """Handles the Cancel button event, shutting down the frame.

        Args:
            event (wx.Event): The event object.
        """
        logging.debug("Cancel button pressed. Closing down.")
        self.Destroy()
        self.parent.Destroy()
