#main.py
import tkinter as tk
from Widgets import Widgets
from ModbusClient import ModbusClient
from ModbusMasterClientWidget import ModbusMasterClientWidget
#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

root = tk.Tk()  # Root instance for your Tkinter application
root.geometry("768x768")  # Size of the tkinter window
root.configure(bg="white")  # Background color of the tkinter window

# This is a list of the options that the user can select from when choosing what type of data to write to the modbus.
options = ["Float", "Signed 16-bit", "Unsigned 16-bit", "Boolean", "ASCII", "Byte", "Epoch"]

# Create an instance of the Modbus client with initial empty settings
modbus_client = ModbusClient("", 0)

# Create and place widgets related to the modbus client
widgets = Widgets(root, options,modbus_client)
widgets.create_widgets()

# Create and place widgets related to the modbus master client
modbus_widget = ModbusMasterClientWidget(root, modbus_client)
modbus_widget.create_widgets()

root.mainloop()  # This is the main event loop for the tkinter application.