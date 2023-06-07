#main.py
import tkinter as tk
from tkinter import ttk
from Widgets import Widgets
from ModbusClient import ModbusClient
from ModbusMasterClientWidget import ModbusMasterClientWidget
from Tab1 import Tab1  # Import the classes for the tabs
from Tab2 import Tab2
import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)


root = tk.Tk()  # Root instance for your Tkinter application
root.geometry("1080x768")  # Size of the tkinter window
root.configure(bg="white")  # Background color of the tkinter window

notebook = ttk.Notebook(root)  # Create the notebook (tabbed window)

# This is a list of the options that the user can select from when choosing what type of data to write to the modbus.
options = ["Float", "Signed 16-bit", "Unsigned 16-bit", "Boolean", "ASCII", "Byte", "Epoch"]

# Create an instance of the Modbus client with initial empty settings
modbus_client = ModbusClient("", 0)

# Create the tabs and add them to the notebook
tab1 = Tab1(notebook, options, modbus_client)  # Pass any necessary arguments to your tab classes
tab2 = Tab2(notebook, options, modbus_client)

notebook.add(tab1.frame, text='Registry')  # Add the frames to the notebook with their respective labels
notebook.add(tab2.frame, text='Data Testing')

notebook.pack(fill=tk.BOTH, expand=True)  # Add the notebook to the root window

root.mainloop()  # This is the main event loop for the tkinter application.

#Task to do
# Create a work mode where the only writable registries are a Boolean and a float at memory address
# Boolean 40569
# Float MS2B 40570
# Float LS2B 40571
# When typing addresses subtract 40001
# Make so table reads off like excel sheet
# Have drop down menu with options to display whole table, or justa table pertaining to a different type
# all integrated besides epochs and input
# confusing epochs

#problems
# py mod bus only allows up to 125 registries per request. Hard to display
# need to display multiple types in different formats while keeping track of everything