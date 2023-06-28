import tkinter as tk
from ModBusProtocolPST import ModBusProtocolPST

class Tab3ModBusProtocolPST:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolPST_widget = ModBusProtocolPST(self.frame, modbus_client, modbus_protocol_connection)
        self.ModBusProtocolPST_widget.create_widgets()


