#ModBusProtocolPST.py
import tkinter as tk
from tkinter import messagebox, ttk
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator



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
        # Create the widgets/ gui elements
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        # call manage_UI
        self.manage_UI()

    def manage_widgets_visibility(self, *args):
        # get variable from connect screen
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()

        # create list of widgets
        self.widgets_index = []

        # add label and entries to the index
        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))

        # if X3 is selected, show the gui
        if selected_version == 'X3':
            self.frame.place(relx=0.01, rely=0.5, anchor="w", relwidth=0.65, relheight=0.6)
            self.widgetTemp.placeOrHide(self.export_to_excel_button, 0.15, 0.8, False)
            self.widgetTemp.placeOrHide(self.clear_pst_data_button, 0.3, 0.8, False)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        # if hide gui
        else:
            self.widgetTemp.placeOrHide(self.frame,0.01,0.5,True)
            self.widgetTemp.placeOrHide(self.export_to_excel_button, 0.15, 0.8, True)
            self.widgetTemp.placeOrHide(self.clear_pst_data_button, 0.3, 0.8, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        # index of entries, var name, coordinates
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                           ("pst_trigger_entry", (0.79, 0.2)),
                           ("signal_deviation_entry",(0.79,0.3)),
                           ("auto_schedule_entry",(0.79,0.35)),
                           ("time_entry",(0.79,0.6)),
                           ("off_point_entry",(0.79,0.65)),
                           ("target_entry",(0.79,0.7)),
                           ("increment_entry",(0.79,0.8)),
                           ("maximum_target_entry",(0.79,0.85)),
                           ("last_pst_event_entry",(0.3,0.92))

                           ]
        # for loop for entries
        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)

        # lable index with var name, display text, coordinates
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
        # for loop of index entries
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

        #create buttons
        self.export_to_excel_button = self.widgetTemp.create_button("Export to Excel", 0.15,0.8,10,2,15,self.export_to_excel)
        self.clear_pst_data_button = self.widgetTemp.create_button("Clear PST Data", 0.3, 0.8, 10, 2, 15,self.clear_pst_data)
    def export_to_excel(self):
        # temp function for export to excel
        print('export excel')
    def clear_pst_data(self):
        # temp function for clear_pst_data
        print('clear pst data')


    def clear_entries(self,raw_values):
        #clear entries

        self.raw_data = raw_values

        #clear the entries
        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Make the entry widget writable
            entry.config(state='normal')
            # Clear the existing text in the entry widget
            entry.delete(0, 'end')

        # set the entries
        self.set_entries(raw_values)

        # set back the entries to read only
        for var_name, _ in self.entry_index:
            entry = getattr(self, var_name)
            entry.config(state='readonly')
    def set_entries(self, raw_values):
        #map out the entries to the correct values
        #Pst mode contact power
        if self.modbus_client.translate_value("Boolean",raw_values[201]) == "True":
            self.pst_trigger_entry.insert(0, "Contact Pwer")
            self.time_entry.insert(0, self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[173]))
            self.off_point_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[155], raw_values[156]), 3))
            self.target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[157], raw_values[158]), 3))
            self.increment_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[149], raw_values[150]), 3))
            self.maximum_target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[159], raw_values[160]), 3))
            self.last_pst_event_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[11]))


        #Pst signal deviation
        if self.modbus_client.translate_value("Boolean", raw_values[202]) == "True":
            self.pst_trigger_entry.insert(0,"Signal Deviation")
            self.signal_deviation_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[153], raw_values[154]), 3))
            self.time_entry.insert(0, self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[173]))
            self.off_point_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[155], raw_values[156]), 3))
            self.target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[157], raw_values[158]), 3))
            self.increment_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[149], raw_values[150]), 3))
            self.maximum_target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[159], raw_values[160]), 3))
            self.last_pst_event_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[11]))

        #Pst mode scheduled/auto
        if self.modbus_client.translate_value("Boolean", raw_values[203]) == "True":
            self.auto_schedule_entry.insert(0,self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[172]))
            self.pst_trigger_entry.insert(0, "Auto")
            # stop duplicate entry stuff
            if self.time_entry.get() != self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[173]):
                self.time_entry.delete(0, 'end')
                self.time_entry.insert(0, self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[173]))

            if self.off_point_entry.get() != round(self.modbus_client.translate_value("Float 32 bit", raw_values[155], raw_values[156]), 3):
                self.off_point_entry.delete(0, 'end')
                self.off_point_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[155], raw_values[156]), 3))

            if self.target_entry.get() != round(self.modbus_client.translate_value("Float 32 bit", raw_values[157], raw_values[158]), 3):
                self.target_entry.delete(0, 'end')
                self.target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[157], raw_values[158]), 3))

            if self.increment_entry.get() != round(self.modbus_client.translate_value("Float 32 bit", raw_values[149], raw_values[150]), 3):
                self.increment_entry.delete(0, 'end')
                self.increment_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[149], raw_values[150]), 3))

            if self.maximum_target_entry.get() != round(self.modbus_client.translate_value("Float 32 bit", raw_values[159], raw_values[160]), 3):
                self.maximum_target_entry.delete(0, 'end')
                self.maximum_target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[159], raw_values[160]), 3))

            if self.last_pst_event_entry.get() != self.modbus_client.translate_value("Byte", raw_values[11]):
                self.last_pst_event_entry.delete(0, 'end')
                self.last_pst_event_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[11]))


        #Pst mode contact unpowered

        if self.modbus_client.translate_value("Boolean", raw_values[204]) == "True":
            self.pst_trigger_entry.insert(0, "Contact Unpwer")
            self.time_entry.insert(0, self.modbus_client.translate_value("Unsigned 16 bit int", raw_values[173]))
            self.off_point_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[155], raw_values[156]), 3))
            self.target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[157], raw_values[158]), 3))
            self.increment_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[149], raw_values[150]), 3))
            self.maximum_target_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[159], raw_values[160]), 3))
            self.last_pst_event_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[11]))



        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))
        #self.operational_status_entry.insert(0, self.modbus_client.translate_value(self.names.get_status_name(raw_values[15])))
        self.operational_status_entry.insert(0, self.names.get_status_name(self.modbus_client.translate_value("Byte",raw_values[15])))















