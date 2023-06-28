import tkinter as tk
from ModBusProtocolCalibration import ModBusProtocolCalibration

class Tab5ModBusProtocolCalibration:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolCalibration_widget = ModBusProtocolCalibration(self.frame, modbus_client, modbus_protocol_connection)
        self.ModBusProtocolCalibration_widget.create_widgets()


