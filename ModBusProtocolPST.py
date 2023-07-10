#ModBusProtocolPST.py
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator
from ModBusProtocolStatus import ModBusProtocolStatus


class ModBusProtocolPST:
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

        self.frame.place(relx=0.01, rely=0.5, anchor="w", relwidth=0.65, relheight=0.6)
        # Create the table
        self.table = ttk.Treeview(self.frame,
                                  columns=("Event", "Status", "Trigger", "Total Elapsed Time", "Target", "Occurred"),
                                  show='headings')
        self.table.heading("Event", text="Event")
        self.table.heading("Status", text="Status")
        self.table.heading("Trigger", text="Trigger")
        self.table.heading("Total Elapsed Time", text="Total Elapsed Time")
        self.table.heading("Target", text="Target")
        self.table.heading("Occurred", text="Occured")

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

        # Distribute the column widths equally
        total_width = self.table.winfo_width()
        n_columns = len(self.table["columns"])
        for column in self.table["columns"]:
            self.table.column(column, width=int(total_width / n_columns))


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
            self.frame.place(relx=0.01, rely=0.5, anchor="w", relwidth=0.65, relheight=0.6)
            self.widgetTemp.placeOrHide(self.export_to_excel_button, 0.15, 0.8, False)
            self.widgetTemp.placeOrHide(self.clear_pst_data_button, 0.3, 0.8, False)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:
            self.widgetTemp.placeOrHide(self.frame,0.01,0.5,True)
            self.widgetTemp.placeOrHide(self.export_to_excel_button, 0.15, 0.8, True)
            self.widgetTemp.placeOrHide(self.clear_pst_data_button, 0.3, 0.8, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),

                           ("signal_deviation_entry",(0.79,0.3)),
                           ("auto_schedule_entry",(0.79,0.35)),
                           ("time_entry",(0.79,0.6)),
                           ("off_point_entry",(0.79,0.65)),
                           ("target_entry",(0.79,0.7)),
                           ("increment_entry",(0.79,0.8)),
                           ("maximum_target_entry",(0.79,0.85)),
                           ("last_pst_event_entry",(0.3,0.92))

                           ]

        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)


        self.label_index=[
            ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
            ("operational_status_label",("Operational Status",0.14,0.07)),

            ("pst_trigger_label", ("PST Trigger:", 0.70, 0.2)),
            ("signal_deviation_label",("Signal Deviation",0.70,0.3)),
            ("auto_schedule_label", ("Auto Schedule", 0.70, 0.35)),

            ("time_label", ("Time", 0.70, 0.6)),
            ("off_point_label", ("Off Point", 0.70, 0.65)),
            ("target_label", ("Target", 0.70, 0.7)),
            ("increment_label",("Increment",0.7,0.8)),
            ("maximum_target_label", ("Maximum Target", 0.7, 0.85)),
            ("last_pst_event_label",("Last Pst Event", 0.2, 0.92))
                       ]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)
        self.export_to_excel_button = self.widgetTemp.create_button("Export to Excel", 0.15,0.8,10,2,15,self.export_to_excel)
        self.clear_pst_data_button = self.widgetTemp.create_button("Clear PST Data", 0.3, 0.8, 10, 2, 15,self.clear_pst_data)
    def export_to_excel(self):
        print('export excel')
    def clear_pst_data(self):
        print('clear pst data')


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


