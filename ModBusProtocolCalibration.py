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
        self.analog_input_label = tk.Label(self.root, text="Analog input")
        self.widgetTemp.placeOrHide(self.analog_input_label, 0.03, 0.7, False)

        self.feedback_values_label = tk.Label(self.root, text="Feedback Values")
        self.widgetTemp.placeOrHide(self.feedback_values_label, 0.35, 0.7, False)

        self.primary_feedback_label = tk.Label(self.root, text="Primary Feedback")
        self.widgetTemp.placeOrHide(self.primary_feedback_label,0.04, 0.23, False)

        self.redundant_feedback_label = tk.Label(self.root, text="Redundant Feedback")
        self.widgetTemp.placeOrHide(self.redundant_feedback_label, 0.33, 0.23, False)

        self.stroke_limts_label = tk.Label(self.root,text="Stroke Limits")
        self.widgetTemp.placeOrHide(self.stroke_limts_label,0.03,0.18,False)

        self.primary_feedback_label = tk.Label(self.root, text="Using Primary Feedback")
        self.widgetTemp.placeOrHide(self.primary_feedback_label, 0.35, 0.84, False)

        self.factory_calibration_label = tk.Label(self.root, text="Factory Calibration")
        self.widgetTemp.placeOrHide(self.factory_calibration_label, 0.77, 0.79, False)

        self.current_operational_mode_label, self.current_operational_mode_entry = self.widgetTemp.create_label_and_entry(
            "Current Operational Mode", 0, 0.07, 0.01, 0.1, 12, True, preFilledText=None
        )
        self.operational_status_label, self.operational_status_entry = self.widgetTemp.create_label_and_entry(
            "Operational Status", 0.14, 0.07, 0.15, 0.1, 12, True, preFilledText=None
        )
        self.primary_feedback_position_low_label,self.primary_feedback_position_low_entry = self.widgetTemp.create_label_and_entry(
            "Position Low",0.05,0.27,0.05,0.3,12,True,preFilledText=None
        )
        self.redundant_feedback_position_low_label, self.redundant_feedback_position_low_entry = self.widgetTemp.create_label_and_entry(
            "Position Low", 0.35, 0.27, 0.35, 0.3, 12, True, preFilledText=None
        )
        self.primary_feedback_position_high_label, self.primary_feedback_position_high_entry = self.widgetTemp.create_label_and_entry(
            "Position High", 0.05, 0.37, 0.05, 0.4, 12, True, preFilledText=None
        )
        self.redundant_feedback_position_high_label, self.redundant_feedback_position_high_entry = self.widgetTemp.create_label_and_entry(
            "Position High", 0.35, 0.37, 0.35, 0.4, 12, True, preFilledText=None
        )
        self.driven_device_mechanical_travel_label,self.driven_device_mechanical_travel_entry = self.widgetTemp.create_label_and_entry(
            "Driven Device Mechanical Travel",0.02,0.48,0.19,0.48,12,True, preFilledText=None
        )
        self.signal_low_label,self.signal_low_entry = self.widgetTemp.create_label_and_entry("Signal Low", 0.05,0.74,0.05,0.77,12,True,preFilledText=None)

        self.signal_high_label, self.signal_high_entry = self.widgetTemp.create_label_and_entry("Signal High", 0.2, 0.74,0.2, 0.77, 12, True,preFilledText=None)

        self.current_cs_input_label, self.current_cs_input_entry = self.widgetTemp.create_label_and_entry(
            "Current CS Input", 0.115,0.82, 0.125, 0.85, 12,True,preFilledText=None
        )
        self.primary_label, self.primary_entry = self.widgetTemp.create_label_and_entry(
            "Primary", 0.35, 0.75, 0.4, 0.75, 12, True, preFilledText=None
        )
        self.redundant_label, self.redundant_entry = self.widgetTemp.create_label_and_entry(
            "Redundant", 0.34, 0.78, 0.4, 0.78, 12, True, preFilledText=None
        )
        self.transmitter_low_label, self.transmitter_low_entry = self.widgetTemp.create_label_and_entry(
            "Transmitter Low", 0.72, 0.82, 0.73, 0.85, 12, True, preFilledText=None
        )
        self.transmitter_high_label, self.transmitter_high_entry = self.widgetTemp.create_label_and_entry(
            "Transmitter High", 0.83, 0.82, 0.84, 0.85, 12, True, preFilledText=None
        )







