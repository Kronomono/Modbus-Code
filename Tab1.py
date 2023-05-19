#Tab1.py
import tkinter as tk
from Widgets import Widgets

class Tab1:
    def __init__(self, notebook, options, modbus_client):
        self.frame = tk.Frame(notebook)
        self.widgets = Widgets(self.frame, options, modbus_client)
        self.widgets.create_widgets()

    def update(self):
        # Update the frame when a new address is added
        self.frame.update()
