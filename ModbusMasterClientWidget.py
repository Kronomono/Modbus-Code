#ModbusMasterClientWidget.py
import tkinter as tk
from tkinter import messagebox
from GraphWindow import GraphWindow
from tkinter import simpledialog
from ModbusClient import ModbusClient

class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        # Initialize the widget with a root window and a Modbus client
        self.root = root
        self.modbus_client = modbus_client
        self.connection_button = None
        self.retrieve_button = None

    def create_widgets(self):
        # Create the Connect and Retrieve Data buttons
        self.create_connection_button()
        self.create_retrieve_button()

    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def create_retrieve_button(self):
        # Create the Retrieve Data button and place it in the window
        self.retrieve_button = tk.Button(self.root, text="Retrieve Data", command=self.retrieve_data)
        self.retrieve_button.place(relx=0.05, rely=0.08, anchor=tk.NW)

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
                # Retrieve the host and port from the dialog and attempt to connect
                host = host_entry.get()
                port = port_entry.get()

                print(f"Retrieved host from dialog: {host}")
                print(f"Retrieved port from dialog: {port}")

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
            data = self.modbus_client.read_holding_registers(address=0, count=10)
            self.graph_window = GraphWindow(self.root)
            self.graph_window.plot_data(data)
        else:
            print("No active Modbus connection. Please connect first.")
            messagebox.showerror("Error", "No active Modbus connection. Please connect first.")
