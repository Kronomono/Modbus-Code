#ModbusMasterClientWidget.py
import tkinter as tk
from tkinter import messagebox, ttk
from GraphWindow import GraphWindow
from ModbusClient import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
import struct
from pymodbus.constants import Endian
import unicodedata
import time


class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        # Initialize the widget with a root window and a Modbus client
        self.root = root
        self.modbus_client = modbus_client
        self.connection_button = None
        self.retrieve_button = None
        self.graph_button = None

        # Create a frame to hold the table and the scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the table
        self.table = ttk.Treeview(self.root, columns=("Address", "Type", "Registry"), show='headings')
        self.table.heading("Address", text="Address")
        self.table.heading("Type", text="Type")
        self.table.heading("Registry", text="Registry")
        self.table.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the scrollbar to the table
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.table.yview)

        # Create the data type dropdown
        self.data_type_var = tk.StringVar(self.root)
        self.data_type_options = ['holding', 'Float 32 bit', 'ASCII 16 bit', 'Epoch 32 bit', 'Binary 16 bit',
                                  'Signed Int 16 bit', 'Unsigned Int 16 bit', 'Boolean', 'Byte', 'Signed Int 32 bit',
                                  'Unsigned Int 32 bit']

        self.data_type_var.set(self.data_type_options[0])
        self.data_type_dropdown = tk.OptionMenu(self.root, self.data_type_var, *self.data_type_options)
        self.data_type_dropdown.place(relx=0.15, rely=0.08, anchor=tk.NW)
        self.unit_entry = self.create_unit_entry()  # Store the unit_entry widget
        self.address_entry = self.create_address_entry()
        self.count_entry = self.create_count_entry()

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
        address_entry = tk.Label(self.root, text="Enter starting address #")
        address_entry.place(relx=0.23, rely=0.03, anchor=tk.CENTER)
        # Create an address entry field and place it in the window
        address_entry = tk.Entry(self.root, width=10)
        address_entry.config(bg="white", fg="black")
        address_entry.place(relx=0.2, rely=0.05, anchor=tk.NW)
        return address_entry
    def create_unit_entry(self):
        # Create a unit entry field and place it in the window
        unit_entry = tk.Entry(self.root, width=10)
        unit_entry_label = tk.Label(self.root, text="Enter unit #")
        unit_entry_label.place(relx=0.38, rely=0.03, anchor=tk.CENTER)
        unit_entry.place(relx=0.35, rely=0.05, anchor=tk.NW)
        return unit_entry
    def create_count_entry(self):
        # create a count entry field and place in window
        count_entry_label = tk.Label(self.root, text="Enter # of addresses to read")
        count_entry = tk.Entry(self.root,width=10)

        # placements
        count_entry_label.place(relx=0.55, rely=0.03, anchor=tk.CENTER)
        count_entry.place(relx=0.5, rely=0.05, anchor=tk.NW)
        return count_entry

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
            dialog.geometry("400x400")  # Set the width and height of the dialog window
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

    def show_graph(self):
        # Display the graph window
        if hasattr(self, 'data'):
            self.graph_window = GraphWindow(self.root)
            self.graph_window.plot_data(self.data)
        else:
            print("No data available. Please retrieve data first.")
            messagebox.showerror("Error", "No data available. Please retrieve data first.")

    def retrieve_data(self):
        # Retrieve data from the Modbus server
        try:
            # Assuming you are reading holding registers starting from address 0 and reading 10 registers
            address = int(self.address_entry.get())
            unit = int(self.unit_entry.get())
            count = int(self.count_entry.get())

            result = self.modbus_client.client.read_holding_registers(address, count, unit=unit)
            if not result.isError():
                # Clear the table
                self.table.delete(*self.table.get_children())

                # Read and process the data based on the selected type
                selected_type = self.data_type_var.get()

                # Add the data to the table
                for i, value in enumerate(result.registers):
                    if selected_type == "Float 32 bit":
                        # Group the registers in pairs of two for float values
                        if i % 2 == 0:
                            decoded_value = \
                            struct.unpack('>f', struct.pack('>I', (value << 16) | result.registers[i + 1]))[0]
                            self.table.insert('', 'end', values=(address + i, selected_type, decoded_value))
                    elif selected_type == "Signed Int 32 bit":
                        # Group the registers in pairs of two for signed int values
                        if i % 2 == 0:
                            decoded_value = \
                            struct.unpack('>l', struct.pack('>l', (value << 16) | result.registers[i + 1]))[0]
                            self.table.insert('', 'end', values=(address + i, selected_type, decoded_value))
                    elif selected_type == "Unsigned Int 32 bit":
                        # Group the registers in pairs of two for unsigned int values
                        if i % 2 == 0:
                            decoded_value = \
                            struct.unpack('>L', struct.pack('>L', (value << 16) | result.registers[i + 1]))[0]
                            self.table.insert('', 'end', values=(address + i, selected_type, decoded_value))
                    else:
                        # Translate the value based on the selected data type
                        translated_value = self.translate_value(value)
                        self.table.insert('', 'end', values=(address + i, selected_type, translated_value))
            else:
                print("Failed to read data from Modbus server.")
                messagebox.showerror("Error", "Failed to read data from Modbus server.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")

    def translate_value(self, value):
        # Translate the value based on the selected data type
        data_type = self.data_type_var.get()

        if data_type == "holding":
            return value
        elif data_type == "Float 32 bit":
            # Assuming the value is a 32-bit float
            binary_data = struct.pack('>H', value)
            decoded_value = struct.unpack('>f', binary_data)[0]
            return decoded_value
        elif data_type == "ASCII 16 bit":
            # Assuming the value is a 16-bit value representing an ASCII character
            ascii_value = value & 0xFF
            decoded_value = chr(ascii_value)
            return decoded_value
        elif data_type == "Unsigned Int 16 bit":
            # Interpret as unsigned int
            return value
        elif data_type == "Signed Int 16 bit":
            # Interpret as signed int
            return struct.unpack('>h', struct.pack('>H', value))[0]
        elif data_type == "Epoch 32 bit":
            # Assuming the value is a 32-bit epoch timestamp
            binary_data = struct.pack('>I', value)
            decoded_value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(struct.unpack('>I', binary_data)[0]))
            return decoded_value
        elif data_type == "Binary 16 bit":
            # Assuming the value is a binary string
            binary_string = bin(value)[2:]  # Remove '0b' prefix
            return binary_string
        elif data_type == "Boolean":
            # Translate 0/1 to True/False
            if value == 0:
                return False
            elif value == 1:
                return True
            else:
                return 'Not a Boolean'
        elif data_type == "Byte":
            # Assuming the value is a byte (8 bits)
            byte_value = value & 0xFF
            return byte_value
        elif data_type == "Signed Int 32 bit":
            # Assuming the value is a 32-bit signed integer
            binary_data = struct.pack('>l', value)
            decoded_value = struct.unpack('>l', binary_data)[0]
            return decoded_value
        elif data_type == "Unsigned Int 32 bit":
            # Assuming the value is an unsigned 32-bit integer
            binary_data = struct.pack('>L', value)
            decoded_value = struct.unpack('>L', binary_data)[0]
            return decoded_value
        else:
            return value