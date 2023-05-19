#Tab2.py
import tkinter as tk
from ModbusMasterClientWidget import ModbusMasterClientWidget

class Tab2:
    def __init__(self, notebook, options, modbus_client):
        self.frame = tk.Frame(notebook)
        self.modbus_widget = ModbusMasterClientWidget(self.frame, modbus_client)
        self.modbus_widget.create_widgets()
