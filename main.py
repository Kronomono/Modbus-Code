import tkinter as tk
from Widgets import Widgets
from ModbusClient import ModbusClient
from ModbusMasterClientWidget import ModbusMasterClientWidget
import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)


root = tk.Tk()
root.geometry("768x768")
root.configure(bg="white")

options = ["Float", "Signed 16-bit", "Unsigned 16-bit", "Boolean", "ASCII", "Byte", "Epoch"]

modbus_client = ModbusClient("", 0)  # Create an instance of the Modbus client with initial empty settings

widgets = Widgets(root, options)
widgets.create_widgets()

modbus_widget = ModbusMasterClientWidget(root, modbus_client)
modbus_widget.create_widgets()

root.mainloop()
