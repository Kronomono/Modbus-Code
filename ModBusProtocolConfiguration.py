#ModBusProtocolConfiguration.py
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox, ttk
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator



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


    def create_widgets(self):
        # Create the widgets
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        #call manage_UI function to manage the UI
        self.manage_UI()

    def manage_widgets_visibility(self, *args):
        # get variable from connection tab
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        # create index list of widgets
        self.widgets_index = []

        #take lable index and entry index and combine them
        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))
                #if X3 option selected in connection tab show stuff
        if selected_version == 'X3':

            self.widgetTemp.placeOrHide(self.fail_safe_entry_2,0.19,0.35,False)
            self.widgetTemp.placeOrHide(self.minimum_modulating_entry_2,0.23,0.4,False)

            self.widgetTemp.placeOrHide(self.surge_bkpt_entry, 0.71, 0.3, False)
            self.widgetTemp.placeOrHide(self.surge_off_entry, 0.8, 0.3, False)
            self.widgetTemp.placeOrHide(self.surge_dir_entry, 0.9, 0.3, False)

            self.widgetTemp.placeOrHide(self.save_button,0.85,0.85,False)
            self.widgetTemp.placeOrHide(self.load_button,0.73,0.85,False)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        # otherwise hide it all
        else:
            #self.widgetTemp.placeOrHide(self.operational_mode_entry_label, 0.67, 0.0, True)
            #self.widgetTemp.placeOrHide(self.operational_mode_type_dropdown, 0.67, 0.03, True)

            self.widgetTemp.placeOrHide(self.fail_safe_entry_2, 0.19, 0.35, True)
            self.widgetTemp.placeOrHide(self.minimum_modulating_entry_2, 0.23, 0.4, True)

            self.widgetTemp.placeOrHide(self.surge_bkpt_entry,0.71,0.3,True)
            self.widgetTemp.placeOrHide(self.surge_off_entry, 0.8, 0.3, True)
            self.widgetTemp.placeOrHide(self.surge_dir_entry, 0.9, 0.3, True)

            self.widgetTemp.placeOrHide(self.save_button, 0.85, 0.85, True)
            self.widgetTemp.placeOrHide(self.load_button, 0.73, 0.85, True)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        # create save and load button
        self.save_button = self.widgetTemp.create_button("Save Configuration", 0.85,0.85, 10, 2,14,self.save_config)
        self.load_button = self.widgetTemp.create_button("Load Configuration", 0.73, 0.85, 10, 2, 14, self.load_config)
        # entry index with their variable names, and coordinates
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                           ("control_signal_entry",(0.1,0.2)),
                           ("power_on_entry",(0.1,0.25)),
                           ("ESD_trip_signal_entry",(0.1,0.3)),
                           ("fail_safe_entry_1",(0.1,0.35)),
                           ("bumpless_transfer_entry",(0.12,0.4)),
                           ("minimum_modulating_entry_1",(0.13,0.45)),
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
                           ("fail_direction_entry",(0.8,0.48)),
                           ("electronic_position_relay_1_entry", (0.85, 0.63)),
                           ("electronic_position_relay_2_entry", (0.85, 0.68)),
                           ("electronic_position_relay_3_entry", (0.85, 0.73)),   ]
        # create custom sized entries
        self.fail_safe_entry_2 = self.widgetTemp.create_entry(0.19, 0.35, 5, True, preFilledText=None)
        self.minimum_modulating_entry_2 = self.widgetTemp.create_entry(0.23,0.45,6,True,preFilledText=None)

        self.surge_bkpt_entry = self.widgetTemp.create_entry(0.71,0.3,5,True,preFilledText=None)
        self.surge_off_entry = self.widgetTemp.create_entry(0.8, 0.3, 5, True, preFilledText=None)
        self.surge_dir_entry = self.widgetTemp.create_entry(0.9, 0.3, 8, True, preFilledText=None)

        #for loop that create the entries from index
        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)

        # label index, with variable name, displayed text, and coordinates
        self.label_index=[
                       ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                       ("operational_status_label",("Operational Status",0.14,0.07)),
                        ("control_signal_label",("Control Signal",0.01,0.2)),
                        ("power_on_label", ("Power On ", 0.01, 0.25)),
            ("ESD_trip_signal_label",("ESD Trip Signal",0.01,0.3)),
            ("fail_safe_label", ("Fail Safe",0.01, 0.35)),
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
            ("electronic_position_relay_1_label",("Electronic Position Relay #1", 0.7, 0.63)),
            ("electronic_position_relay_2_label", ("Electronic Position Relay #2", 0.7, 0.68)),
            ("electronic_position_relay_3_label", ("Electronic Position Relay #3", 0.7, 0.73)),


            ("configuration_parameters_label",("Configuration Parameters",0.01,0.15)),
            ("speed_label", ("Speed", 0.33, 0.2)),
            ("historic_actuator_odometer_label",("Historic Actuator Odometer",0.1,0.73)),
            ("drives_label", ("Drives", 0.68, 0.15)),
            ("accumulator_systems_label", ("Accumulator Systems", 0.68, 0.335)),

            ("surge_bkpt_label_%", ("%", 0.76, 0.3)),
            ("surge_off_label_%", ("%", 0.85, 0.3)),
            ("surge_dir_label_%", ("%", 0.97, 0.3)),

            ("electronic_position_relay_#1_label_%", ("%", 0.94, 0.63)),
            ("electronic_position_relay_#2_label_%", ("%", 0.94, 0.68)),

            ("max_high_speed_label_%", ("%", 0.54, 0.35)),
            ("max_down_speed_label_%", ("%", 0.54, 0.4)),
            ("speed_break_point_label_%", ("%", 0.54, 0.45)),
            ("max_manual_speed_label_%", ("%", 0.54, 0.5)),

            ("deadband_%", ("%",0.63, 0.63)),

            ("failsafe_%", ("%", 0.23, 0.35)),
            ("minimum_modulating_%", ("%", 0.27, 0.45)),

                       ]
        # for loop for label creation
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

    #save data function
    def save_config(self):
        # create a ist
        raw_data = {}

        # get value of all entries and put them in list
        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Get the value in the entry
            entry_value = entry.get()
            # Add the entry name and value to the raw_data dictionary
            raw_data[var_name] = entry_value

        raw_data["fail_safe_entry_2"] = self.fail_safe_entry_2.get()
        raw_data["minimum_modulating_entry_2"] = self.minimum_modulating_entry_2.get()
        raw_data["surge_bkpt_entry"] = self.surge_bkpt_entry.get()
        raw_data["surge_off_entry"] = self.surge_off_entry.get()
        raw_data["surge_dir_entry"] = self.surge_dir_entry.get()

        # if there is anything in raw_data then save it to json file with varaible names
        if any(raw_data.values()):
            # Open a file dialog for the user to choose the directory to save the file
            file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=(("JSON files", "*.json"), ("All files", "*.*")))

            # If a file path was provided, write the raw_data to a JSON file at that path
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(raw_data, f, indent=4)
        else:
            messagebox.showerror("Error", "Data is empty. Cannot save the file.")

    def load_config(self):
        #temporary load config function
        print("load")

    def clear_entries(self,raw_values):
        # clears all the entries for configuration tab
        # manually  clearing because not in index due to size being different
        self.fail_safe_entry_2.config(state='normal')
        self.minimum_modulating_entry_2.config(state='normal')

        self.surge_bkpt_entry.config(state='normal')
        self.surge_off_entry.config(state='normal')
        self.surge_dir_entry.config(state='normal')

        # for loop going through every entry
        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Make the entry widget writable
            entry.config(state='normal')
            # Clear the existing text in the entry widget
            entry.delete(0, 'end')

        self.fail_safe_entry_2.delete(0, 'end')
        self.minimum_modulating_entry_2.delete(0, 'end')

        self.surge_bkpt_entry.delete(0, 'end')
        self.surge_off_entry.delete(0, 'end')
        self.surge_dir_entry.delete(0, 'end')

        # mapping entries by calling function
        self.set_entries(raw_values)


        # set all entries back to read only
        self.fail_safe_entry_2.config(state='readonly')
        self.minimum_modulating_entry_2.config(state='readonly')

        self.surge_bkpt_entry.config(state='readonly')
        self.surge_off_entry.config(state='readonly')
        self.surge_dir_entry.config(state='readonly')

        for var_name, _ in self.entry_index:
            entry = getattr(self, var_name)
            entry.config(state='readonly')
    def set_entries(self, raw_values):
        # maps out entries
        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))

        self.operational_status_entry.insert(0, self.names.get_status_name(self.modbus_client.translate_value("Byte",raw_values[15])))
        #self.operational_status_entry.insert(0, self.modbus_client.translate_value(self.names.get_status_name(raw_values[15])))
        self.ESD_trip_signal_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[174]))



        self.bumpless_transfer_entry.insert(0, self.modbus_client.translate_value("Boolean", raw_values[182]))
        self.minimum_modulating_entry_1.insert(0, self.modbus_client.translate_value("Boolean", raw_values[183]))
        self.solenoid_seat_entry.insert(0, self.modbus_client.translate_value("Boolean", raw_values[184]))
        self.electronic_position_relay_3_entry.insert(0, self.modbus_client.translate_value("Boolean", raw_values[197]))

        self.control_signal_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[0], raw_values[1]), 3))
        self.minimum_modulating_entry_2.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[131], raw_values[132]),3))
        self.cal_stroke_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[133], raw_values[134]),3))
        self.deadband_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[137], raw_values[138]), 3))
        self.electronic_position_relay_1_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[145], raw_values[146]), 3))
        self.electronic_position_relay_2_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[147], raw_values[148]), 3))

        self.max_high_speed_entry.insert(0,self.modbus_client.translate_value("Unsigned Int 8 bit", raw_values[168]))
        self.max_manual_speed_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 8 bit", raw_values[169]))

        self.gain_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[166]))
        self.recharge_pressure_entry.insert(0,self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[165]))


        self.motor_starts_1k_entry.insert(0, round(self.modbus_client.translate_value("Unsigned Int 32 bit", raw_values[562], raw_values[563]), 3))
        self.strokes_1k_entry.insert(0,round(self.modbus_client.translate_value("Unsigned Int 32 bit", raw_values[558], raw_values[559]),3))
        #self.accumulator_starts_1k_entry.insert(0,round(self.modbus_client.translate_value("Unsigned Int 32 bit", raw_values[562], raw_values[563]),3))

        # Failsafe logic and power on logic
        # off
        if raw_values[180] == False and raw_values[181] == False:
            self.fail_safe_entry_1.insert(0, "Off")
            self.fail_safe_entry_2.delete(0, 0)

        # in-place

        if raw_values[181] == True:
            #self.power_on_entry.insert(0, "Local")
            self.fail_safe_entry_1.insert(0, "In-place")
        print(raw_values[180])
        # Position / power up
        if raw_values[180] == True:
            #self.power_on_entry.insert(0, "Power-up Last")
            self.fail_safe_entry_1.insert(0, "Position")
            self.fail_safe_entry_2.insert(0, round(
                self.modbus_client.translate_value("Float 32 bit", raw_values[129], raw_values[130]), 3))

        #Two speed logic
        if self.modbus_client.translate_value("Boolean",raw_values[191]) == "True" and self.modbus_client.translate_value("Boolean", raw_values[192]) == "True":
            self.two_speed_entry.insert(0, "Up/Dn On and Breakpoint On")
            self.max_down_speed_entry.insert(0, self.modbus_client.translate_value("Unsigned 8 bit", raw_values[167]))
            self.speed_break_point_entry.insert(0, self.modbus_client.translate_value("Float 32 bit", raw_values[139],raw_values[140]))

        elif self.modbus_client.translate_value("Boolean", raw_values[192]) == "True":
            self.two_speed_entry.insert(0, "Breakpoint On")
            self.speed_break_point_entry.insert(0, self.modbus_client.translate_value("Float 32 bit", raw_values[139],
                                                                                      raw_values[140]))

        elif self.modbus_client.translate_value("Boolean", raw_values[191]) == "True":
            self.two_speed_entry.insert(0, "Up/Dn On")
            self.max_down_speed_entry.insert(0, self.modbus_client.translate_value("Unsigned 8 bit", raw_values[167]))


        #Booster motor pump logic
        if self.modbus_client.translate_value("Boolean", raw_values[186]) == "True":
            #self.booster_pump_entry.insert(0,"Motor Enabled") wrong register
            self.booster_pump_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[141], raw_values[142]), 3))


        #Direction logic
                #if surge is enabled
        if self.modbus_client.translate_value("Boolean",raw_values[193]) == "True":
            # if PL & PH enabled
            if self.modbus_client.translate_value("Boolean",raw_values[194]) == "True" and self.modbus_client.translate_value("Boolean",raw_values[195]) == "True":
                self.surge_dir_entry.insert(0,"PL & PH")
            #if PL only is enabled
            elif self.modbus_client.translate_value("Boolean",raw_values[194]) == "True":
                self.surge_dir_entry.insert(0, "PL")
            #if PH only is enabled
            elif self.modbus_client.translate_value("Boolean", raw_values[195]) == "True":
                    self.surge_dir_entry.insert(0, "PH")
            self.surge_bkpt_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[141], raw_values[142]), 3))
            self.surge_off_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[143], raw_values[144]), 3))

        #power fail logic
        # Accumulator
        if self.modbus_client.translate_value("Boolean",raw_values[187]) == "True":
            self.power_fail_entry.insert(0,"Accumulator")
            #fail direction
            if self.modbus_client.translate_value("Boolean",raw_values[189]) == "True" and self.modbus_client.translate_value("Boolean", raw_values[190]) == "True":
                self.fail_direction_entry.insert(0, "PL/PH")
            elif self.modbus_client.translate_value("Boolean",raw_values[189]) == "True":
                self.fail_direction_entry.insert(0,"PL")
            elif self.modbus_client.translate_value("Boolean", raw_values[190]) == "True":
                self.fail_direction_entry.insert(0, "PH")
        #In place
        if self.modbus_client.translate_value("Boolean",raw_values[188]) == "True":
            self.power_fail_entry.insert(0, "In place")
