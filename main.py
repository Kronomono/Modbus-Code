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
def on_window_close():
    modbus_client.close()
    root.destroy()

root = tk.Tk()  # Root instance for your Tkinter application
root.geometry("1080x768")  # Size of the tkinter window
root.configure(bg="gray")  # Background color of the tkinter window
root.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind the function to the window close event

# Create a Frame for the notebook
notebook_frame = ttk.Frame(root)
notebook_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Create a custom style for the notebook and set the tab position to 's' (south)
style = ttk.Style()
style.configure("TNotebook", tabposition="s")

notebook = ttk.Notebook(notebook_frame, style="TNotebook")  # Create the notebook (tabbed window)

# This is a list of the options that the user can select from when choosing what type of data to write to the modbus.
options = ["Float", "Signed 16-bit", "Unsigned 16-bit", "Boolean", "ASCII", "Byte", "Epoch"]

# Create an instance of the Modbus client with initial empty settings
modbus_client = ModbusClient("", 0)

# Create the tabs and add them to the notebook
tab1 = Tab1(notebook, options, modbus_client)  # Pass any necessary arguments to your tab classes
tab2 = Tab2(notebook, options, modbus_client)

# Add the frames to the notebook with their respective labels
notebook.add(tab1.frame, text='Write Registry')
notebook.add(tab2.frame, text='Data Display')

notebook.pack(fill=tk.BOTH, expand=True)  # Add the notebook to the notebook frame

root.mainloop()  # This is the main event loop for the tkinter application.
#Task to do
# all integrated be