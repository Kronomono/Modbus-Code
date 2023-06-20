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
            "Position Low", 0.25, 0.27, 0.25, 0.3, 12, True, preFilledText=None
        )
        self.primary_feedback_position_high_label, self.primary_feedback_position_high_entry = self.widgetTemp.create_label_and_entry(
            "Position high", 0.05, 0.37, 0.05, 0.4, 12, True, preFilledText=None
        )
        self.redundant_feedback_position_high_label, self.redundant_feedback_position_high_entry = self.widgetTemp.create_label_and_entry(
            "Position high", 0.25, 0.37, 0.25, 0.4, 12, True, preFilledText=None
        )





