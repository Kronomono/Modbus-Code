#ModBusProtocolDiagnostics.py
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator
from ModBusProtocolStatus import ModBusProtocolStatus


class ModBusProtocolDiagnostics:
    def __init__(self, root, modbus_client,modbus_protocol_connection):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.names = Names()
        self.ModBusProtocolConnection = modbus_protocol_connection
        self.widgetTemp = WidgetTemplateCreator(self.root)

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        # Create a second frame to hold the table and the scrollbar
        self.frame = tk.Frame(self.main_frame)

        self.frame.place(relx=0.01, rely=0.3, anchor="w", relwidth=0.65, relheight=0.3)
        # Create the table
        self.table = ttk.Treeview(self.frame,columns=("#","Event", "Occurred", "Cleared"),show='headings')
        self.table.heading("#", text="#")
        self.table.heading("Event", text="Event")
        self.table.heading("Occurred", text="Occurred")
        self.table.heading("Cleared", text="Cleared")

        # Create scroll bar
        scrollbar = tk.Scrollbar(self.frame)
        # Link the scrollbar to the table
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.table.yview)

        # Use grid instead of pack for placement
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the grid to expand properly
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Set the column widths
        self.table.column("#", width=50)
        self.table.column("Event", width=100)
        self.table.column("Occurred", width=100)
        self.table.column("Cleared", width=100)



    def create_widgets(self):
        # Create the Connect
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)


        self.manage_UI()

    def manage_widgets_visibility(self, *args):
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        selected_protocol = self.ModBusProtocolConnection.protocol_type_var.get()

        self.widgets_index = []

        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))
        if selected_version == 'X3':

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),

                        ("accumulator_warning_pressure_entry", (0.85, 0.2)),
                        ("accumulator_recharge_timeout_entry", (0.85, 0.25)),
                        ("delta_pressure_output_warning_entry", (0.85, 0.3)),
                        ("delta_pressure_output_alarm_entry", (0.85, 0.35)),

                           ]

        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)


        self.label_index=[
           ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
            ("operational_status_label",("Operational Status",0.14,0.07)),

            ("accumulator_warning_pressure_label", ("Accumulator Warning Pressure", 0.68, 0.2)),
            ("accumulator_recharge_timeout_label", ("Accumulator Recharge Timeout", 0.68, 0.25)),
            ("delta_pressure_output_warning_label", ("Delta Pressure Output Warning", 0.68, 0.3)),
            ("delta_pressure_output_alarm_label", ("Delta Pressure Output Alarm", 0.68, 0.35)),


                       ]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

    def clear_entries(self,raw_values):
        self.raw_data = raw_values


        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Make the entry widget writable
            entry.config(state='normal')
            # Clear the existing text in the entry widget
            entry.delete(0, 'end')

        self.set_entries(raw_values)


        for var_name, _ in self.entry_index:
            entry = getattr(self, var_name)
            entry.config(state='readonly')
    def set_entries(self, raw_values):
        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))


