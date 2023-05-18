import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from ModbusClient import ModbusClient

class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        self.root = root
        self.modbus_client = modbus_client
        self.connection_button = None
        self.retrieve_button = None

    def create_widgets(self):
        self.create_connection_button()
        self.create_retrieve_button()

    def create_connection_button(self):
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def create_retrieve_button(self):
        self.retrieve_button = tk.Button(self.root, text="Retrieve Data", command=self.retrieve_data)
        self.retrieve_button.place(relx=0.05, rely=0.08, anchor=tk.NW)

    def show_connection_dialog(self):
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
                host = host_entry.get()
                port = port_entry.get()

                print("Retrieved host from dialog:", host)
                print("Retrieved port from dialog:", port)

                if host and port:
                    self.modbus_client.update_host_port(host, int(port))
                    if self.modbus_client.connect():
                        self.connection_button["text"] = "Disconnect"
                    dialog.destroy()

            connect_button = tk.Button(dialog, text="Connect", command=connect)
            connect_button.pack()

            dialog.transient(self.root)
            dialog.grab_set()
            self.root.wait_window(dialog)

    def toggle_connection(self):
        if self.connection_button["text"] == "Connect":
            self.show_connection_dialog()
        else:
            self.disconnect_modbus()

    def connect_modbus(self):
        if self.modbus_client.client.host and self.modbus_client.client.port:
            # Connect to the Modbus slave
            connection_status = self.modbus_client.connect()
            if connection_status:
                print("Modbus connection established.")
            else:
                self.connection_button["text"] = "Connect"

    def disconnect_modbus(self):
        # Close the Modbus client connection
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"

    def retrieve_data(self):
        # Check if connection is established
        if self.connection_button["text"] == "Disconnect":
            # Perform the data retrieval operation
            self.modbus_client.read_holding_registers(address=0, count=10)
        else:
            print("No active Modbus connection. Please connect first.")


