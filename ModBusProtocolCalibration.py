#ModBusProtocolCalibration.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator


class ModBusProtocolCalibration:
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
        self.manage_UI()

    def manage_widgets_visibility(self, *args):
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        selected_protocol = self.ModBusProtocolConnection.protocol_type_var.get()

    def manage_UI(self, *args):
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                        ("primary_feedback_position_low_entry",(0.05,0.3)),
                        ("redundant_feedback_position_low_entry",(0.35,0.3)),
                        ("primary_feedback_position_high_entry",(0.05,0.4)),
                        ("redundant_feedback_position_high_entry",(0.35,0.4)),
                        ("driven_device_mechanical_travel_entry",(0.19,0.48)),
                        ("signal_low_entry",(0.05,0.77)),
                        ("signal_high_entry",(0.2,0.77)),
                        ("current_cs_input_entry",(0.125, 0.85)),
                        ("primary_entry",(0.4, 0.75)),
                        ("redundant_entry",(0.4, 0.78,)),
                        ("transmitter_low_entry",(0.73, 0.85)),
                        ("transmitter_high_entry",(0.84, 0.85))]

        for var_name, index in self.entry_index:
            entry = self.widgetTemp.create_entry(*index, 12, True, preFilledText=None)
            setattr(self, var_name, entry)

        self.label_index=[("analog_input_label",("Analog input",0.03,0.7)),
                       ("feedback_values_label",("Feedback Values",0.35,0.7)),
                       ("primary_feedback_label",("Primary Feedback",0.04,0.23)),
                       ("redundant_feedback_label",("Redundant Feedback",0.33,0.23)),
                       ("stroke_limits_label",("Stroke Limits",0.03,0.18)),
                       ("primary_feedback_label",("Using Primary Feedback",0.35,0.84)),
                       ("factory_calibration_label",("Factory Calibration",0.77,0.79)),
                       ("mA1_label",("mA",0.12,0.77)),
                       ("mA2_label",("mA",0.27,0.77)),
                       ("mA3_label",("mA",0.2,0.85)),
                       ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                       ("operational_status_label",("Operational Status",0.14,0.07)),
                       ("primary_feedback_position_low_label",("Position Low",0.05,0.27)),
                       ("redundant_feedback_position_low_label",("Position Low",0.35,0.27)),
                       ("primary_feedback_position_high_label",("Position High",0.05,0.37)),
                       ("redundant_feedback_position_high_label",("Position High",0.35,0.37)),
                       ("driven_device_mechanical_travel_label",("Driven Device Mechanical Travel",0.02,0.48)),
                       ("signal_low_label",("Signal Low", 0.05,0.74)),
                       ("signal_high_label",("Signal High",0.2,0.74)),
                       ("current_cs_input_label",("Current CS Input", 0.115, 0.82)),
                       ("primary_label",("Primary",0.35,0.75)),
                       ("redundant_label",("Redundant",0.34,0.78)),
                       ("transmitter_low_label",("Transmitter Low",0.72,0.82)),
                       ("transmitter_high_label",("Transmitter High",0.83,0.82))]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)







