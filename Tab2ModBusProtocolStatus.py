import tkinter as tk
from ModBusProtocolStatus import ModBusProtocolStatus

class Tab2ModBusProtocolStatus:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection, modbus_protocol_calibration):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolStatus_widget = ModBusProtocolStatus(self.frame, modbus_client, modbus_protocol_connection,modbus_protocol_calibration)
        self.ModBusProtocolStatus_widget.create_widgets()


