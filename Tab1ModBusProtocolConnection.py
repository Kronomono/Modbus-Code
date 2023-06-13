import tkinter as tk
from ModBusProtocolConnection import ModBusProtocolConnection

class Tab1ModBusProtocolConnection:
    def __init__(self, notebook, options, modbus_client):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolConnection_widget = ModBusProtocolConnection(self.frame, modbus_client)
        self.ModBusProtocolConnection_widget.create_widgets()


