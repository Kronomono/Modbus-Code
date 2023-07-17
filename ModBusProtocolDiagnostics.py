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
        # Create the Connect
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)
        self.clear_data_button = self.widgetTemp.create_button("Clear Data", 0.25, 0.9, 10, 2, 15,self.clear_data)
        self.generate_service_report_button = self.widgetTemp.create_button("Generate Service\nReport", 0.65, 0.92, 10, 2, 15, self.clear_data)
        self.view_edit_service_note_button = self.widgetTemp.create_button("View/Edit Service\n Notes", 0.85, 0.92, 10,2, 15, self.clear_data)

        self.manage_UI()

    def clear_data(self):
        print('clear data')

    def manage_widgets_visibility(self, *args):
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()


        self.widgets_index = []

        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))
        if selected_version == 'X3':
            self.frame.place(relx=0.01, rely=0.3, anchor="w", relwidth=0.65, relheight=0.3)
            self.frame2.place(relx=0.01, rely=0.65, anchor="w", relwidth=0.65, relheight=0.3)
            self.widgetTemp.placeOrHide(self.clear_data_button, 0.25, 0.9, False)
            self.widgetTemp.placeOrHide(self.generate_service_report_button, 0.65, 0.92, False)
            self.widgetTemp.placeOrHide(self.view_edit_service_note_button, 0.85, 0.92, False)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:
            self.widgetTemp.placeOrHide(self.frame, 0.01, 0.3, True)
            self.widgetTemp.placeOrHide(self.frame2, 0.01, 0.65, True)
            self.widgetTemp.placeOrHide(self.clear_data_button, 0.25, 0.9, True)
            self.widgetTemp.placeOrHide(self.generate_service_report_button, 0.65, 0.92, True)
            self.widgetTemp.placeOrHide(self.view_edit_service_note_button, 0.85, 0.92, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),

                        ("accumulator_warning_pressure_entry", (0.85, 0.2)),
                        ("accumulator_recharge_timeout_entry", (0.85, 0.25)),
                        ("delta_pressure_output_warning_entry", (0.85, 0.3)),
                        ("delta_pressure_output_alarm_entry", (0.85, 0.35)),
                        ("last_error_entry", (0.85, 0.55)),
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
            ("last_error_label", ("Last Error", 0.68, 0.55)),

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
        self.operational_status_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[15]))

        self.accumulator_recharge_timeout_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[163]))
        self.accumulator_warning_pressure_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[164]))
        self.delta_pressure_output_warning_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[171]))
        self.delta_pressure_output_alarm_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[170]))
        self.last_error_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[14]))

        self.fault_time_stamp_1 = self.modbus_client.translate_value("Epoch 64 bit",raw_values[328],raw_values[329],raw_values[330],raw_values[331])
        self.fault_time_stamp_2 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[332], raw_values[333],raw_values[334], raw_values[335])
        self.fault_time_stamp_3 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[336], raw_values[337],raw_values[338], raw_values[339])
        self.fault_time_stamp_4 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[340], raw_values[341],raw_values[342], raw_values[343])
        self.fault_time_stamp_5 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[344], raw_values[345],raw_values[346], raw_values[347])
        self.fault_time_stamp_6 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[348], raw_values[349],raw_values[350], raw_values[351])
        self.fault_time_stamp_7 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[352], raw_values[353],raw_values[354], raw_values[355])
        self.fault_time_stamp_8 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[356], raw_values[357],raw_values[358], raw_values[359])
        self.fault_time_stamp_9 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[360], raw_values[361],raw_values[362], raw_values[363])
        self.fault_time_stamp_10 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[364], raw_values[365],raw_values[366], raw_values[367])

        '''print(f"Epoch1 value", self.fault_time_stamp_1)
        print(f"Epoch2 value", self.fault_time_stamp_2)
        print(f"Epoch3 value", self.fault_time_stamp_3)
        print(f"Epoch4 value", self.fault_time_stamp_4)
        print(f"Epoch5 value", self.fault_time_stamp_5)
        print(f"Epoch6 value", self.fault_time_stamp_6)
        print(f"Epoch7 value", self.fault_time_stamp_7)
        print(f"Epoch8 value", self.fault_time_stamp_8)
        print(f"Epoch9 value", self.fault_time_stamp_9)
        print(f"Epoch10 value", self.fault_time_stamp_10)'''

        self.model_change_time_stamp_1 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[378], raw_values[379],raw_values[380], raw_values[381])
        self.model_change_time_stamp_2 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[382], raw_values[383],raw_values[384], raw_values[385])
        self.model_change_time_stamp_3 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[386], raw_values[387],raw_values[388], raw_values[389])
        self.model_change_time_stamp_4 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[390], raw_values[391],raw_values[392], raw_values[393])
        self.model_change_time_stamp_5 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[394], raw_values[395],raw_values[396], raw_values[397])
        self.model_change_time_stamp_6 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[398], raw_values[399],raw_values[400], raw_values[401])
        self.model_change_time_stamp_7 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[402], raw_values[403],raw_values[404], raw_values[405])
        self.model_change_time_stamp_8 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[406], raw_values[407],raw_values[408], raw_values[409])
        self.model_change_time_stamp_9 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[410], raw_values[411],raw_values[412], raw_values[413])
        self.model_change_time_stamp_10 = self.modbus_client.translate_value("Epoch 64 bit", raw_values[414], raw_values[415],raw_values[416], raw_values[417])

        '''   print(f"Model_Epoch1 value", self.model_change_time_stamp_1)
        print(f"Model_Epoch2 value", self.model_change_time_stamp_2)
        print(f"Model_Epoch3 value", self.model_change_time_stamp_3)
        print(f"Model_Epoch4 value", self.model_change_time_stamp_4)
        print(f"Model_Epoch5 value", self.model_change_time_stamp_5)
        print(f"Model_Epoch6 value", self.model_change_time_stamp_6)
        print(f"Model_Epoch7 value", self.model_change_time_stamp_7)
        print(f"Model_Epoch8 value", self.model_change_time_stamp_8)
        print(f"Model_Epoch9 value", self.model_change_time_stamp_9)
        print(f"Model_Epoch10 value", self.model_change_time_stamp_10)'''

        self.table2.insert("", "end", values=(self.names.get_name(419), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[418]), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[488])))
        self.table2.insert("", "end", values=(self.names.get_name(420), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[419]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[489])))
        self.table2.insert("", "end", values=(self.names.get_name(421), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[420]), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[490])))
        self.table2.insert("", "end", values=(self.names.get_name(422), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[421]), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[491])))
        self.table2.insert("", "end", values=(self.names.get_name(423), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[422]), self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[492])))
        self.table2.insert("", "end", values=(self.names.get_name(424), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[423]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[493])))
        self.table2.insert("", "end", values=(self.names.get_name(425), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[424]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[494])))
        self.table2.insert("", "end", values=(self.names.get_name(426), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[425]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[495])))
        self.table2.insert("", "end", values=(self.names.get_name(427), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[426]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[496])))
        self.table2.insert("", "end", values=(self.names.get_name(428), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[427]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[497])))
        self.table2.insert("", "end", values=(self.names.get_name(429), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[428]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[498])))
        self.table2.insert("", "end", values=(self.names.get_name(430), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[429]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[499])))
        self.table2.insert("", "end", values=(self.names.get_name(431), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[430]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[500])))
        self.table2.insert("", "end", values=(self.names.get_name(432), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[431]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[501])))
        self.table2.insert("", "end", values=(self.names.get_name(433), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[432]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[502])))
        self.table2.insert("", "end", values=(self.names.get_name(434), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[433]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[503])))
        self.table2.insert("", "end", values=(self.names.get_name(435), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[434]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[504])))
        self.table2.insert("", "end", values=(self.names.get_name(436), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[435]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[505])))
        self.table2.insert("", "end", values=(self.names.get_name(437), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[436]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[506])))
        self.table2.insert("", "end", values=(self.names.get_name(438), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[437]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[507])))
        self.table2.insert("", "end", values=(self.names.get_name(439), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[438]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[508])))
        self.table2.insert("", "end", values=(self.names.get_name(440), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[439]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[509])))
        self.table2.insert("", "end", values=(self.names.get_name(441), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[440]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[510])))
        self.table2.insert("", "end", values=(self.names.get_name(442), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[441]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[511])))
        self.table2.insert("", "end", values=(self.names.get_name(443), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[442]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[512])))
        self.table2.insert("", "end", values=(self.names.get_name(444), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[443]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[513])))
        self.table2.insert("", "end", values=(self.names.get_name(445), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[444]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[514])))
        self.table2.insert("", "end", values=(self.names.get_name(446), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[445]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[515])))
        self.table2.insert("", "end", values=(self.names.get_name(447), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[446]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[516])))
        self.table2.insert("", "end", values=(self.names.get_name(448), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[447]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[517])))
        self.table2.insert("", "end", values=(self.names.get_name(449), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[448]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[518])))
        self.table2.insert("", "end", values=(self.names.get_name(450), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[449]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[519])))
        self.table2.insert("", "end", values=(self.names.get_name(451), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[450]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[520])))
        self.table2.insert("", "end", values=(self.names.get_name(452), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[451]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[521])))
        self.table2.insert("", "end", values=(self.names.get_name(453), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[452]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[522])))
        self.table2.insert("", "end", values=(self.names.get_name(454), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[453]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[523])))
        self.table2.insert("", "end", values=(self.names.get_name(455), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[454]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[524])))
        self.table2.insert("", "end", values=(self.names.get_name(456), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[455]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[525])))
        self.table2.insert("", "end", values=(self.names.get_name(457), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[456]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[526])))
        self.table2.insert("", "end", values=(self.names.get_name(458), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[457]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[527])))
        self.table2.insert("", "end", values=(self.names.get_name(459), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[458]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[528])))
        self.table2.insert("", "end", values=(self.names.get_name(460), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[459]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[529])))
        self.table2.insert("", "end", values=(self.names.get_name(461), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[460]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[530])))
        self.table2.insert("", "end", values=(self.names.get_name(462), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[461]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[531])))
        self.table2.insert("", "end", values=(self.names.get_name(463), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[462]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[532])))
        self.table2.insert("", "end", values=(self.names.get_name(464), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[463]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[533])))
        self.table2.insert("", "end", values=(self.names.get_name(465), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[464]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[534])))
        self.table2.insert("", "end", values=(self.names.get_name(466), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[465]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[535])))
        self.table2.insert("", "end", values=(self.names.get_name(467), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[466]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[536])))
        self.table2.insert("", "end", values=(self.names.get_name(468), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[467]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[537])))
        self.table2.insert("", "end", values=(self.names.get_name(469), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[468]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[538])))
        self.table2.insert("", "end", values=(self.names.get_name(470), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[469]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[539])))
        self.table2.insert("", "end", values=(self.names.get_name(471), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[470]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[540])))
        self.table2.insert("", "end", values=(self.names.get_name(472), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[471]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[541])))
        self.table2.insert("", "end", values=(self.names.get_name(473), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[472]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[542])))
        self.table2.insert("", "end", values=(self.names.get_name(474), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[473]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[543])))
        self.table2.insert("", "end", values=(self.names.get_name(475), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[474]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[544])))
        self.table2.insert("", "end", values=(self.names.get_name(476), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[475]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[545])))
        self.table2.insert("", "end", values=(self.names.get_name(477), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[476]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[546])))
        self.table2.insert("", "end", values=(self.names.get_name(478), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[477]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[547])))
        self.table2.insert("", "end", values=(self.names.get_name(479), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[478]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[548])))
        self.table2.insert("", "end", values=(self.names.get_name(480), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[479]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[549])))
        self.table2.insert("", "end", values=(self.names.get_name(481), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[480]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[550])))
        self.table2.insert("", "end", values=(self.names.get_name(482), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[481]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[551])))
        self.table2.insert("", "end", values=(self.names.get_name(483), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[482]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[552])))
        self.table2.insert("", "end", values=(self.names.get_name(484), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[483]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[553])))
        self.table2.insert("", "end", values=(self.names.get_name(485), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[484]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[554])))
        self.table2.insert("", "end", values=(self.names.get_name(486), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[485]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[555])))
        self.table2.insert("", "end", values=(self.names.get_name(487), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[486]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[556])))
        self.table2.insert("", "end", values=(self.names.get_name(487), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[486]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[556])))
        self.table2.insert("", "end", values=(self.names.get_name(488), self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[487]),self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[557])))