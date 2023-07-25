#ModBusProtocolDiagnostics.py
import tkinter as tk
from tkinter import messagebox, ttk
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator



class ModBusProtocolDiagnostics:
    def __init__(self, root, modbus_client,modbus_protocol_connection):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.names = Names()
        self.ModBusProtocolConnection = modbus_protocol_connection
        self.widgetTemp = WidgetTemplateCreator(self.root)
        #create a flag so that info is only imported to the tables once
        self.called = False

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        # Create a second frame to hold the table and the scrollbar
        self.frame = tk.Frame(self.main_frame)

        self.frame.place(relx=0.01, rely=0.3, anchor="w", relwidth=0.65, relheight=0.3)
        # Create the table
        self.table = ttk.Treeview(self.frame,columns=("#","Event", "Occurred"),show='headings')
        self.table.heading("#", text="#")
        self.table.heading("Event", text="Event")
        self.table.heading("Occurred", text="Occurred")


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


        # Create a third frame to hold the second table and the scrollbar
        self.frame2 = tk.Frame(self.main_frame)

        self.frame2.place(relx=0.01, rely=0.65, anchor="w", relwidth=0.65, relheight=0.3)
        # Create the second table
        self.table2 = ttk.Treeview(self.frame2, columns=("Error Type", "Current Total", "Historic Total"), show='headings')
        self.table2.heading("Error Type", text="Error Type")
        self.table2.heading("Current Total", text="Current Total")
        self.table2.heading("Historic Total", text="Historic Total")

        # Create scroll bar for the second table
        scrollbar2 = tk.Scrollbar(self.frame2)
        # Link the scrollbar to the second table
        self.table2.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.configure(command=self.table2.yview)

        # Use grid instead of pack for placement of the second table
        self.table2.grid(row=0, column=0, sticky="nsew")
        scrollbar2.grid(row=0, column=1, sticky="ns")

        # Configure the grid to expand properly for the second table
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)

        # Set the column widths for the second table
        self.table2.column("Error Type", width=100)
        self.table2.column("Current Total", width=100)
        self.table2.column("Historic Total", width=100)


    def create_widgets(self):
        # Create the widgets/ gui
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)
        self.clear_data_button = self.widgetTemp.create_button("Clear Data", 0.25, 0.9, 10, 2, 15,self.clear_data)
        self.generate_service_report_button = self.widgetTemp.create_button("Generate Service\nReport", 0.65, 0.92, 10, 2, 15, self.clear_data)
        self.view_edit_service_note_button = self.widgetTemp.create_button("View/Edit Service\n Notes", 0.85, 0.92, 10,2, 15, self.clear_data)

        #call manage ui
        self.manage_UI()

    def clear_data(self):
        # clear the table, delete information in table
        print('clear data')
        self.table.delete(*self.table.get_children())
        self.table2.delete(*self.table2.get_children())
        # set flag back to false
        self.called = False

    def manage_widgets_visibility(self, *args):
        # get variable from connection tab
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()

        # create widgets list
        self.widgets_index = []

        # add entries and labels to widget list
        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))
        # if version is x3, show widgets
        if selected_version == 'X3':
            self.frame.place(relx=0.01, rely=0.3, anchor="w", relwidth=0.65, relheight=0.3)
            self.frame2.place(relx=0.01, rely=0.65, anchor="w", relwidth=0.65, relheight=0.3)
            self.widgetTemp.placeOrHide(self.clear_data_button, 0.25, 0.9, False)
            self.widgetTemp.placeOrHide(self.generate_service_report_button, 0.65, 0.92, False)
            self.widgetTemp.placeOrHide(self.view_edit_service_note_button, 0.85, 0.92, False)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        # if not then hide them
        else:
            self.widgetTemp.placeOrHide(self.frame, 0.01, 0.3, True)
            self.widgetTemp.placeOrHide(self.frame2, 0.01, 0.65, True)
            self.widgetTemp.placeOrHide(self.clear_data_button, 0.25, 0.9, True)
            self.widgetTemp.placeOrHide(self.generate_service_report_button, 0.65, 0.92, True)
            self.widgetTemp.placeOrHide(self.view_edit_service_note_button, 0.85, 0.92, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        # entry list, var name, coordinates
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),

                        ("accumulator_warning_pressure_entry", (0.85, 0.2)),
                        ("accumulator_recharge_timeout_entry", (0.85, 0.25)),
                        ("delta_pressure_output_warning_entry", (0.85, 0.3)),
                        ("delta_pressure_output_alarm_entry", (0.85, 0.35)),
                        ("last_error_entry", (0.85, 0.55)),
                           ]
        # for loop for entries
        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)

        # label list, var name, display text coordinates
        self.label_index=[
           ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
            ("operational_status_label",("Operational Status",0.14,0.07)),

            ("accumulator_warning_pressure_label", ("Accumulator Warning Pressure", 0.68, 0.2)),
            ("accumulator_recharge_timeout_label", ("Accumulator Recharge Timeout", 0.68, 0.25)),
            ("delta_pressure_output_warning_label", ("Delta Pressure Output Warning", 0.68, 0.3)),
            ("delta_pressure_output_alarm_label", ("Delta Pressure Output Alarm", 0.68, 0.35)),
            ("last_error_label", ("Last Error", 0.68, 0.55)),

                       ]
        # for loop for creating labels
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

    def clear_entries(self,raw_values):

        # clear entries for loop
        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Make the entry widget writable
            entry.config(state='normal')
            # Clear the existing text in the entry widget
            entry.delete(0, 'end')

        # set entries
        self.set_entries(raw_values)

        # for loop to set the entries back to read only
        for var_name, _ in self.entry_index:
            entry = getattr(self, var_name)
            entry.config(state='readonly')
    def set_entries(self, raw_values):
        # map correct values to entries
        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))
        self.operational_status_entry.insert(0, self.modbus_client.translate_value(self.names.get_status_name(raw_values[15])))

        self.accumulator_recharge_timeout_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[163]))
        self.accumulator_warning_pressure_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[164]))
        self.delta_pressure_output_warning_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[171]))
        self.delta_pressure_output_alarm_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[170]))

        self.last_error_entry.insert(0, self.modbus_client.translate_value(self.names.get_error_name(raw_values[14])))



    def set_table(self,raw_values):
        # import data into table

        # Fault time stamps
        self.table.delete(*self.table.get_children())
        for i in range(329, 368, 4):
            row_number = (i - 329) // 4 + 1
            self.table.insert("", "end", values=(str(row_number), self.names.get_name(i),
                                                 self.modbus_client.translate_value("Epoch 64 bit time", raw_values[i - 1],
                                                                                    raw_values[i], raw_values[i + 1],
                                                                                    raw_values[i + 2])))
        # model_change_time_stamp
        for i in range(379, 418, 4):
            row_number = (i - 379) // 4 + 1
            self.table.insert("", "end", values=(str(row_number), self.names.get_name(i),
                                                 self.modbus_client.translate_value("Epoch 64 bit time", raw_values[i - 1],
                                                                                    raw_values[i], raw_values[i + 1],
                                                                                    raw_values[i + 2])))
        # whole bottom table order goes var name, current, lifetime


        for i in range(419, 489):
            self.table2.insert("", "end", values=(
            self.names.get_name(i), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[i - 1]),
            self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[i + 69])))