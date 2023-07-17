import tkinter as tk
from tkinter import ttk
from ModbusClient import ModbusClient
from DataTableBeta import  DataTableBeta
from WriteRegistryBeta import WriteRegistryBeta
from Tab1ModBusProtocolConnection import Tab1ModBusProtocolConnection
from Tab2ModBusProtocolStatus import Tab2ModBusProtocolStatus
from Tab5ModBusProtocolCalibration import Tab5ModBusProtocolCalibration
from Tab6ModBusProtocolConfiguration import Tab6ModBusProtocolConfiguration
from Tab3ModBusProtocolPST import Tab3ModBusProtocolPST
from Tab4ModBusProtocolDiagnostics import Tab4ModBusProtocolDiagnostics

import atexit


def on_exit():
    modbus_client.close()




root = tk.Tk()  # Root instance for your Tkinter application
root.geometry("1080x768")  # Size of the tkinter window
root.configure(bg="gray")  # Background color of the tkinter window
root.title("Rexa ModbusTCP GUI")  # Set the window title
root.iconbitmap("Images\Rexa tiny logo.ico")
atexit.register(on_exit)
#root.protocol("WM_DELETE_WINDOW", on_exit)

# Create a Frame for the notebook
notebook_frame = ttk.Frame(root)
notebook_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Create a custom style for the notebook and set the tab position to 's' (south)
style = ttk.Style()
style.configure("TNotebook", tabposition="s")
style.configure("TNotebook.Tab", padding=[60, 10])  # Adjust the padding values as desired
notebook = ttk.Notebook(notebook_frame, style="TNotebook")  # Create the notebook (tabbed window)

# This is a list of the options that the user can select from when choosing what type of data to write to the modbus.
options = ["Float", "Signed 16-bit", "Unsigned 16-bit", "Boolean", "ASCII", "Byte"]

# Create an instance of the Modbus client with initial empty settings
modbus_client = ModbusClient("", 0)

# Create the tabs and add them to the notebook
tab1 = Tab1ModBusProtocolConnection(notebook, options, modbus_client)
tab5 = Tab5ModBusProtocolCalibration(notebook, options, modbus_client, tab1.ModBusProtocolConnection_widget)
tab6 = Tab6ModBusProtocolConfiguration(notebook, options, modbus_client, tab1.ModBusProtocolConnection_widget)
tab3 = Tab3ModBusProtocolPST(notebook, options, modbus_client, tab1.ModBusProtocolConnection_widget)
tab4 = Tab4ModBusProtocolDiagnostics(notebook, options, modbus_client, tab1.ModBusProtocolConnection_widget)

tab2 = Tab2ModBusProtocolStatus(notebook, options, modbus_client, tab1.ModBusProtocolConnection_widget,tab5.ModBusProtocolCalibration_widget, tab6.ModBusProtocolConfiguration_widget,tab3.ModBusProtocolPST_widget,tab4.ModBusProtocolDiagnostics_widget)

tab7 = DataTableBeta(notebook, options, modbus_client)
tab8 = WriteRegistryBeta(notebook, options, modbus_client)  # Pass any necessary arguments to your tab classes

# Add the frames to the notebook with their respective labels
notebook.add(tab1.frame, text='Connection')
notebook.add(tab2.frame, text='Status')
notebook.add(tab3.frame, text='PST')
notebook.add(tab4.frame, text='Diagnostics')
notebook.add(tab5.frame, text='Calibration')
notebook.add(tab6.frame, text='Configuration')
notebook.add(tab7.frame, text='Data Table')
notebook.add(tab8.frame, text='Writing Registry')

notebook.pack(fill=tk.BOTH, expand=True)  # Add the notebook to the notebook frame




root.mainloop()  # This is the main event loop for the tkinter application.
#Task to do
# make it so table only imports once rather than always updating
# make it so it only updates on the live tab and everything else is static