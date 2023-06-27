#ModBusProtocolCalibration.py
import tkinter as tk
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



    def create_widgets(self):
        # Create the Connect
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        self.operational_mode_type_var, self.operational_mode_entry_label, self.operational_mode_type_dropdown = self.widgetTemp.create_dropdown_menu2(
            "Operational Mode", 0.67, ['Auto Mode', 'Set Up Mode', 'Manual Mode'], 'Auto Mode', 0.67, 0.0, self.something()
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

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:
            self.widgetTemp.placeOrHide(self.operational_mode_entry_label, 0.67, 0.0, True)
            self.widgetTemp.placeOrHide(self.operational_mode_type_dropdown, 0.67, 0.03, True)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        print("manage_UI called")
        print(f"In manage_UI, self is {self}")
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                           ("control_signal_entry",(0.1,0.2)),
                           ("power_on_entry",(0.1,0.25)),
                           ("ESD_trip_signal_entry",(0.1,0.3)),
                           ("false_safe_entry_1",(0.1,0.35)),
                           ("bumpless_transfer_entry",(0.12,0.4)),
                           ("minimum_modulating_entry_1",(0.12,0.45)),
                           ("solendnoid_seat_entry",(0.1,0.5)),
                           ("cal_stroke_entry",(0.1,0.55)),

                           ("two_speed_entry",(0.45,0.25)),
                           ("max_high_speed_entry",(0.45,0.35)),
                           ("max_down_speed_entry",(0.45,0.4)),
                           ("speed_break_point_entry",(0.45,0.45)),
                           ("max_manual_speed_entry",(0.45,0.5))
                        ]
        self.fail_safe_entry_2 = self.widgetTemp.create_entry(0.19, 0.35, 5, True, preFilledText=None)
        self.minimum_modulating_entry_2 = self.widgetTemp.create_entry(0.21,0.4,5,True,preFilledText=None)
        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 14, True, preFilledText=None)
            setattr(self, var_name, entry)


        self.label_index=[
                       ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                       ("operational_status_label",("Operational Status",0.14,0.07)),
                        ("control_signal_label",("Control Signal",0.01,0.2)),
                        ("power_on_label", ("Power On ", 0.01, 0.25)),
            ("ESD_trip_signal_label",("ESD Trip Signal",0.01,0.3)),
            ("false_safe_label", ("Fail Safe",0.01, 0.35)),
            ("bumpless_transfer_label",("Bumpless Transfer",0.01,0.4)),
            ("minimum_modulating_label", ("Minimum Modulating", 0.01, 0.45)),
            ("solenoid_seat_label",("Solenoid Seat",0.01,0.5)),
            ("cal_stroke_label",("Cal Stroke",0.01,0.55)),

            ("two_speed_label",("Two speed",0.38,0.25)),
            ("max_high_speed_label",("Max High Speed",0.35,0.35)),
            ("max_down_speed_label",("Max Down Speed",0.35,0.4)),
            ("speed_break_point_label",("Speed Break Point",0.35,0.45)),
            ("max_manual_speed_label",("Max Manual Speed", 0.35,0.5))


                       ]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)
    def clear_entries(self,raw_values):
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
