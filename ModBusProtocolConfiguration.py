#ModBusProtocolCalibration.py
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator
from ModBusProtocolStatus import ModBusProtocolStatus


class ModBusProtocolConfiguration:
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
        self.raw_data = {}

    def create_widgets(self):
        # Create the Connect
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        self.operational_mode_type_var, self.operational_mode_entry_label, self.operational_mode_type_dropdown = self.widgetTemp.create_dropdown_menu2(
            "Operational Mode", 0.67, ['Auto Mode', 'Set Up Mode', 'Manual Mode'], 'Auto Mode', 0.67, 0.0, self.something
            )

        self.manage_UI()

    def something(self,*args):
        print("something")

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
            self.widgetTemp.placeOrHide(self.operational_mode_entry_label,0.67,0.0,False)
            self.widgetTemp.placeOrHide(self.operational_mode_type_dropdown, 0.67, 0.03, False)

            self.widgetTemp.placeOrHide(self.fail_safe_entry_2,0.19,0.35,False)
            self.widgetTemp.placeOrHide(self.minimum_modulating_entry_2,0.21,0.4,False)

            self.widgetTemp.placeOrHide(self.surge_bkpt_entry, 0.71, 0.3, False)
            self.widgetTemp.placeOrHide(self.surge_off_entry, 0.8, 0.3, False)
            self.widgetTemp.placeOrHide(self.surge_dir_entry, 0.9, 0.3, False)

            self.widgetTemp.placeOrHide(self.save_button,0.85,0.85,False)
            self.widgetTemp.placeOrHide(self.load_button,0.73,0.85,False)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:
            self.widgetTemp.placeOrHide(self.operational_mode_entry_label, 0.67, 0.0, True)
            self.widgetTemp.placeOrHide(self.operational_mode_type_dropdown, 0.67, 0.03, True)

            self.widgetTemp.placeOrHide(self.fail_safe_entry_2, 0.19, 0.35, True)
            self.widgetTemp.placeOrHide(self.minimum_modulating_entry_2, 0.21, 0.4, True)

            self.widgetTemp.placeOrHide(self.surge_bkpt_entry,0.71,0.3,True)
            self.widgetTemp.placeOrHide(self.surge_off_entry, 0.8, 0.3, True)
            self.widgetTemp.placeOrHide(self.surge_dir_entry, 0.9, 0.3, True)

            self.widgetTemp.placeOrHide(self.save_button, 0.85, 0.85, True)
            self.widgetTemp.placeOrHide(self.load_button, 0.73, 0.85, True)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        self.save_button = self.widgetTemp.create_button("Save Configuration", 0.85,0.85, 10, 2,14,self.save_config)
        self.load_button = self.widgetTemp.create_button("Load Configuration", 0.73, 0.85, 10, 2, 14, self.load_config)
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                           ("control_signal_entry",(0.1,0.2)),
                           ("power_on_entry",(0.1,0.25)),
                           ("ESD_trip_signal_entry",(0.1,0.3)),
                           ("failsafe_entry_1",(0.1,0.35)),
                           ("bumpless_transfer_entry",(0.12,0.4)),
                           ("minimum_modulating_entry_1",(0.12,0.45)),
                           ("solenoid_seat_entry",(0.1,0.5)),
                           ("cal_stroke_entry",(0.1,0.55)),

                           ("two_speed_entry",(0.45,0.25)),
                           ("max_high_speed_entry",(0.45,0.35)),
                           ("max_down_speed_entry",(0.45,0.4)),
                           ("speed_break_point_entry",(0.45,0.45)),
                           ("max_manual_speed_entry",(0.45,0.5)),

                           ("gain_entry",(0.38,0.63)),
                           ("deadband_entry", (0.53, 0.63)),

                           ("motor_starts_1k_entry", (0.15, 0.84)),
                           ("booster_starts_1k_entry", (0.25, 0.84)),
                           ("accumulator_starts_1k_entry", (0.35, 0.84)),
                           ("strokes_1k_entry", (0.45, 0.84)),
                           ("total_auto_time_entry", (0.55, 0.84)),

                           ("booster_pump_entry",(0.75,0.2)),
                           ("recharge_pressure_entry",(0.8,0.38)),
                           ("power_fail_entry", (0.8, 0.43)),
                           ("fail_direction",(0.8,0.48)),
                           ("electronic_position_relay_#1_entry", (0.85, 0.63)),
                           ("electronic_position_relay_#2_entry", (0.85, 0.68)),
                           ("electronic_position_relay_#3_entry", (0.85, 0.73)),   ]
        self.fail_safe_entry_2 = self.widgetTemp.create_entry(0.19, 0.35, 5, True, preFilledText=None)
        self.minimum_modulating_entry_2 = self.widgetTemp.create_entry(0.21,0.4,5,True,preFilledText=None)

        self.surge_bkpt_entry = self.widgetTemp.create_entry(0.71,0.3,5,True,preFilledText=None)
        self.surge_off_entry = self.widgetTemp.create_entry(0.8, 0.3, 5, True, preFilledText=None)
        self.surge_dir_entry = self.widgetTemp.create_entry(0.9, 0.3, 5, True, preFilledText=None)

        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)


        self.label_index=[
                       ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                       ("operational_status_label",("Operational Status",0.14,0.07)),
                        ("control_signal_label",("Control Signal",0.01,0.2)),
                        ("power_on_label", ("Power On ", 0.01, 0.25)),
            ("ESD_trip_signal_label",("ESD Trip Signal",0.01,0.3)),
            ("failsafe_label", ("Fail Safe",0.01, 0.35)),
            ("bumpless_transfer_label",("Bumpless Transfer",0.01,0.4)),
            ("minimum_modulating_label", ("Minimum Modulating", 0.01, 0.45)),
            ("solenoid_seat_label",("Solenoid Seat",0.01,0.5)),
            ("cal_stroke_label",("Cal Stroke",0.01,0.55)),

            ("two_speed_label",("Two speed",0.38,0.25)),
            ("max_high_speed_label",("Max High Speed",0.35,0.35)),
            ("max_down_speed_label",("Max Down Speed",0.35,0.4)),
            ("speed_break_point_label",("Speed Break Point",0.35,0.45)),
            ("max_manual_speed_label",("Max Manual Speed", 0.35,0.5)),

            ("gain_label",("Gain",0.35,0.58)),
            ("deadband_label", ("Deadband", 0.5, 0.58)),

            ("motor_starts_1k_label", ("Motor Starts \n(1k)", 0.155, 0.78)),
            ("booster_starts_1k_label", ("Booster Starts \n(1k)", 0.25, 0.78)),
            ("accumulator_starts_1k_label", ("Accumulator Starts \n(1k)", 0.335, 0.78)),
            ("strokes_1k_label", ("Strokes \n(1k)", 0.47, 0.78)),
            ("total_auto_time_label", ("Total Auto Time \n(Hours)", 0.545, 0.78)),

            ("booster_pump_label",("Booster \n Pump",0.7,0.2)),
            ("surge_bkpt_label",("Surge Bkpt",0.7,0.27)),
            ("surge_off_label", ("Surge Off", 0.79, 0.27)),
            ("surge_dir_label", ("Surge Dir", 0.89, 0.27)),

            ("recharge_pressure_label",("Recharge Pressure",0.7,0.38)),
            ("power_fail_label", ("Power Fail", 0.7, 0.43)),
            ("fail_direction_label", ("Fail Direction", 0.7, 0.48)),

            ("relay_control_label", ("Relay Control", 0.7, 0.58)),
            ("electronic_position_relay_#1_label",("Electronic Position Relay #1", 0.7, 0.63)),
            ("electronic_position_relay_#2_label", ("Electronic Position Relay #2", 0.7, 0.68)),
            ("electronic_position_relay_#3_label", ("Electronic Position Relay #3", 0.7, 0.73)),


            ("configuration_parameters_label",("Configuration Parameters",0.01,0.15)),
            ("speed_label", ("Speed", 0.33, 0.2)),
            ("historic_actuator_odometer_label",("Historic Actuator Odometer",0.1,0.73)),
            ("drives_label", ("Drives", 0.68, 0.15)),
            ("accumulator_systems_label", ("Accumulator Systems", 0.68, 0.335)),

            ("surge_bkpt_label_%", ("%", 0.76, 0.3)),
            ("surge_off_label_%", ("%", 0.85, 0.3)),
            ("surge_dir_label_%", ("%", 0.95, 0.3)),

            ("electronic_position_relay_#1_label_%", ("%", 0.94, 0.63)),
            ("electronic_position_relay_#2_label_%", ("%", 0.94, 0.68)),

            ("max_high_speed_label_%", ("%", 0.54, 0.35)),
            ("max_down_speed_label_%", ("%", 0.54, 0.4)),
            ("speed_break_point_label_%", ("%", 0.54, 0.45)),
            ("max_manual_speed_label_%", ("%", 0.54, 0.5)),

            ("deadband_%", ("%",0.63, 0.63)),

            ("failsafe_%", ("%", 0.23, 0.35)),
            ("bumpless_transfer_%", ("%", 0.25, 0.4)),

                       ]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

    def save_config(self):
        raw_data = self.raw_data
        # Open a file dialog for the user to choose the directory to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))

        # If a file path was provided, write the raw_values to a JSON file at that path
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(raw_data, f, indent=4)


    def load_config(self):
        print("load")
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

        self.failsafe_entry_1.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[129], raw_values[130]),3))

        self.minimum_modulating_entry_1.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[131], raw_values[132]),3))

        self.cal_stroke_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[133], raw_values[134]),3))

        self.speed_break_point_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[139], raw_values[140]), 3))

        self.max_high_speed_entry.insert(0,self.modbus_client.translate_value("Unsigned Int 8 bit", raw_values[168]))
        self.max_down_speed_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 8 bit", raw_values[167]))
        self.max_manual_speed_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 8 bit", raw_values[169]))

        self.gain_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[166]))

        self.deadband_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[137], raw_values[138]), 3))

        self.surge_bkpt_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[141], raw_values[142]), 3))
        self.surge_off_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[143], raw_values[144]), 3))

        self.recharge_pressure_entry.insert(0,self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[165]))

        self.strokes_1k_entry.insert(0,round(self.modbus_client.translate_value("Unsigned Int 32 bit", raw_values[558], raw_values[559]),3))
        self.accumulator_starts_1k_entry.insert(0,round(self.modbus_client.translate_value("Unsigned Int 32 bit", raw_values[562], raw_values[563]),3))
