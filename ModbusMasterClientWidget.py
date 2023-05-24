#ModbusMasterClientWidget.py
import tkinter as tk
from tkinter import messagebox, ttk
from GraphWindow import GraphWindow
import string
from tkinter import simpledialog
from ModbusClient import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
import struct
from pymodbus.constants import Endian
import unicodedata


class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        # Initialize the widget with a root window and a Modbus client
        self.root = root
        self.modbus_client = modbus_client
        self.connection_button = None
        self.retrieve_button = None
        self.graph_button = None
        # Create the table
        self.table = ttk.Treeview(self.root, columns=("Address", "Type", "Registry"), show='headings')
        self.table.heading("Address", text="Address")
        self.table.heading("Type", text="Type")
        self.table.heading("Registry", text="Registry")
        self.table.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Create the data type dropdown
        self.data_type_var = tk.StringVar(self.root)
        self.data_type_options = ['holding', 'Float', 'ASCII', 'Epoch']
        self.data_type_var.set(self.data_type_options[0])
        self.data_type_dropdown = tk.OptionMenu(self.root, self.data_type_var, *self.data_type_options)
        self.data_type_dropdown.place(relx=0.15, rely=0.08, anchor=tk.NW)
        self.unit_entry = self.create_unit_entry()  # Store the unit_entry widget
        self.address_entry = self.create_address_entry()

    def create_widgets(self):
        # Create the Connect, Retrieve Data, and Show Graph buttons
        self.create_connection_button()
        self.create_retrieve_button()
        self.create_graph_button()



    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def create_address_entry(self):
        address_entry = tk.Label(self.root, text="Enter address #")
        address_entry.place(relx=0.23, rely=0.03, anchor=tk.CENTER)
        # Create an address entry field and place it in the window
        address_entry = tk.Entry(self.root, width=10)
        address_entry.config(bg="white", fg="black")
        address_entry.place(relx=0.2, rely=0.05, anchor=tk.NW)
        return address_entry
    def create_unit_entry(self):
        # Create an address entry field and place it in the window
        unit_entry = tk.Entry(self.root, width=10)
        unit_entry_label = tk.Label(self.root, text="Enter unit #")
        unit_entry_label.place(relx=0.43, rely=0.03, anchor=tk.CENTER)

        unit_entry.place(relx=0.4, rely=0.05, anchor=tk.NW)
        return unit_entry

    def create_retrieve_button(self):
        # Create the Retrieve Data button and place it in the window
        self.retrieve_button = tk.Button(self.root, text="Retrieve Data", command=self.retrieve_data)
        self.retrieve_button.place(relx=0.05, rely=0.08, anchor=tk.NW)

    def create_graph_button(self):
        # Create the Show Graph button and place it in the window
        self.graph_button = tk.Button(self.root, text="Show Graph", command=self.show_graph)
        self.graph_button.place(relx=0.05, rely=0.11, anchor=tk.NW)

    def show_connection_dialog(self):
        # Create and display a new connection dialog window
        if self.connection_button["text"] == "Connect":
            dialog = tk.Toplevel(self.root)
            dialog.title("Modbus Connection Settings")

            host_label = tk.Label(dialog, text="Host IP Address:")
            host_label.pack()
            host_entry = tk.Entry(dialog)
            host_entry.pack()

            port_label = tk.Label(dialog, text="Modbus Port:")
            port_label.pack()
            port_entry = tk.Entry(dialog)
            port_entry.pack()

            def connect():
                # Retrieve the host and port from the dialog
                host = host_entry.get()
                port = port_entry.get()

                print(f"Retrieved host from dialog: {host}")
                print(f"Retrieved port from dialog: {port}")

                if host and port:
                    # Check if the port enter is an int
                    if port.isdigit():
                        self.modbus_client.update_host_port(host, int(port))
                        if self.modbus_client.connect():
                            self.connection_button["text"] = "Disconnect"
                            messagebox.showinfo("Connected", "Connection successful")
                        else:
                            messagebox.showerror("Error", "Failed to establish Modbus connection.")
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid port. Please enter a valid number.")
                else:
                    messagebox.showerror("Error", "Please enter both the host IP address and port.")

            connect_button = tk.Button(dialog, text="Connect", command=connect)
            connect_button.pack()


            dialog.transient(self.root)
            dialog.title("Modbus Connection Settings")
            dialog.geometry("400x200")  # Set the width and height of the dialog window
            dialog.grab_set()
            self.root.wait_window(dialog)


    def toggle_connection(self):
        # Toggle the Modbus connection based on the current state
        if self.connection_button["text"] == "Connect":
            self.show_connection_dialog()
        else:
            self.disconnect_modbus()

    def disconnect_modbus(self):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"

    def retrieve_data(self):
        # Retrieve data from the Modbus server if a connection is established
        if self.connection_button["text"] == "Disconnect":
            data_type = self.data_type_var.get()
            unit = int(self.unit_entry.get())  # Get the unit value from the unit_entry widget'''
            #set count to 572 readings when connected to device
            address = int(self.address_entry.get())
            #Try make address 1 when connecting to device or 10
            self.data = self.modbus_client.read_holding_registers(address=address, count=572, data_type=data_type)

            # If data is None (in case of error), show an error message
            if self.data is None:
                print("No data received. Please check your connection or the server.")
                messagebox.showerror("Error", "No data received. Please check your connection or the server.")

                return

            # Clear the old data from the table
            for i in self.table.get_children():
                self.table.delete(i)

            # Insert the new data into the table
            if data_type == 'ASCII':
                for index, value_str in enumerate(self.data):
                    # Check if the string is printable
                    if all(32 <= ord(c) <= 126 for c in value_str):
                        self.table.insert("", tk.END, values=(index, data_type, value_str))
                    else:
                        self.table.insert("", tk.END, values=(index, data_type, "[Non-ASCII Character]"))

            # Add this else block to handle other data types
            else:
                for index, value in enumerate(self.data):
                    self.table.insert("", tk.END, values=(index, data_type, value))

            messagebox.showinfo("Data Retrieved", "Data successfully retrieved.")
        else:
            print("No active Modbus connection. Please connect first.")
            messagebox.showerror("Error", "No active Modbus connection. Please connect first.")


    def show_graph(self):
        # Display the graph window
        if hasattr(self, 'data'):
            self.graph_window = GraphWindow(self.root)
            self.graph_window.plot_data(self.data)
        else:
            print("No data available. Please retrieve data first.")
            messagebox.showerror("Error", "No data available. Please retrieve data first.")
