import tkinter as tk
from ModBusProtocolStatus import ModBusProtocolStatus

class Tab2ModBusProtocolStatus:
    def __init__(self, notebook, options, modbus_client, modbus_protocol_connection, modbus_protocol_calibration,modbus_protocol_configuration, modbus_protocol_pst,modbus_protocol_diagnostics,current_tab):
        self.frame = tk.Frame(notebook)
        self.current_tab = current_tab
        self.ModBusProtocolStatus_widget = ModBusProtocolStatus(self.frame, modbus_client, modbus_protocol_connection,modbus_protocol_calibration,modbus_protocol_configuration,modbus_protocol_pst,modbus_protocol_diagnostics,current_tab)
        self.ModBusProtocolStatus_widget.create_widgets()


