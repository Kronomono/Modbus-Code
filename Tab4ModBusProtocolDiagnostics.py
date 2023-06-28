import tkinter as tk
from ModBusProtocolDiagnostics import ModBusProtocolDiagnostics

class Tab4ModBusProtocolDiagnostics:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection):
        self.frame = tk.Frame(notebook)
        self.ModBusProtocolDiagnostics_widget = ModBusProtocolDiagnostics(self.frame, modbus_client, modbus_protocol_connection)
        self.ModBusProtocolDiagnostics_widget.create_widgets()


