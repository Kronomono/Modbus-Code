import tkinter as tk
from ModBusProtocolConfiguration import ModBusProtocolConfiguration

class Tab4ModBusProtocolConfiguration:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolConfiguration_widget = ModBusProtocolConfiguration(self.frame, modbus_client, modbus_protocol_connection)
        self.ModBusProtocolConfiguration_widget.create_widgets()


