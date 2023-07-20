import tkinter as tk
from tkinter import messagebox, ttk
from WidgetTemplateCreator import WidgetTemplateCreator
from ModBusProtocolStatus import ModBusProtocolStatus

class ModBusProtocolConnection:
    def __init__(self, root, modbus_client):
        # References to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.widgetTemp = WidgetTemplateCreator
        self.modbus_status = ModBusProtocolStatus

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

    def create_widgets(self):
        # Create the GUI widgets for the Modbus Protocol Connection tab

        # Create the Connect/Disconnect button
        self.connection_button = self.widgetTemp.create_button(self, "Connect", 0.22, 0.35, 14, 2, 10, self.toggle_connection)

        # Create the logo and box images
        self.logo = self.widgetTemp.add_image(self, "Images/rexa logo.png", 300, 50, 0.5, 0)
        self.box = self.widgetTemp.add_image(self, "Images/ActBox.png", 150, 150, 0.1, 0.15)

        # Create labels and entry fields for Host IP Address, Modbus Port, and Unit
        self.host_label = tk.Label(self.root, text="Host IP Address:")
        self.host_entry = self.widgetTemp.create_entry(self, 0.22, 0.45, 20, False, "192.168.1.100")
        self.port_label = tk.Label(self.root, text="Modbus Port:")
        self.port_entry = self.widgetTemp.create_entry(self, 0.22, 0.55, 20, False, "2011")
        self.unit_label = tk.Label(self.root, text="Unit:")
        self.unit_entry = self.widgetTemp.create_entry(self, 0.22, 0.65, 20, False, "10")

        # Create labels and entry fields for Model Character, Tag Character, Serial Number,
        # Software Version, and Display Version
        self.model_label = tk.Label(self.root, text="Model Character:")
        self.model_entry = self.widgetTemp.create_entry(self, 0.75, 0.3, 30, False, None)
        self.tag_label = tk.Label(self.root, text="Tag Character:")
        self.tag_entry = self.widgetTemp.create_entry(self, 0.75, 0.35, 40, False, None)
        self.serial_label = tk.Label(self.root, text="Serial Number:")
        self.serial_entry = self.widgetTemp.create_entry(self, 0.75, 0.4, 20, False, None)
        self.software_version_label = tk.Label(self.root, text="Serial Number:")
        self.software_version_entry = self.widgetTemp.create_entry(self, 0.75, 0.45, 20, False, None)
        self.display_version_label = tk.Label(self.root, text="Display Version:")
        self.display_version_entry = self.widgetTemp.create_entry(self, 0.75, 0.5, 20, False, None)

        # Configure the entry fields as read-only
        self.model_entry.configure(state="readonly")
        self.tag_entry.configure(state="readonly")
        self.serial_entry.configure(state="readonly")
        self.software_version_entry.configure(state="readonly")
        self.display_version_entry.configure(state="readonly")

        # Create a dropdown menu for Protocol type selection
        self.protocol_type_var, self.protocol_entry_label, self.protocol_type_dropdown = self.widgetTemp.create_dropdown_menu(
            self, "Protocol", 0.38, ['Modbus TCP', 'Ethernet/IP'], 'Modbus TCP', 0.35, 0.30, self.manage_entries_and_version
        )

        # Create a dropdown menu for Rexa Version selection
        self.rexa_version_type_var, self.rexa_version_entry_label, self.rexa_version_type_dropdown = self.widgetTemp.create_dropdown_menu(
            self, "Rexa Version", 0.77, ['X3', 'NextGen'], 'X3', 0.75, 0.10, self.manage_entries_and_version
        )

        # Call the manage_entries_and_version method to show/hide appropriate fields based on selected versions
        self.manage_entries_and_version()

    def manage_entries_and_version(self, *args):
        # Show/hide appropriate fields based on selected versions
        selected_version = self.rexa_version_type_var.get()
        selected_protocol = self.protocol_type_var.get()

        if selected_version == 'X3':
            #show elements
            self.widgetTemp.placeOrHide(self, self.connection_button, 0.22, 0.35, False)
            self.widgetTemp.placeOrHide(self, self.protocol_entry_label, 0.38, 0.30, False)
            self.widgetTemp.placeOrHide(self, self.protocol_type_dropdown, 0.35, 0.35, False)
            self.widgetTemp.placeOrHide(self, self.host_label, 0.22, 0.45, False)
            self.widgetTemp.placeOrHide(self, self.host_entry, 0.38, 0.45, False)
            self.widgetTemp.placeOrHide(self, self.port_label, 0.22, 0.55, False)
            self.widgetTemp.placeOrHide(self, self.port_entry, 0.38, 0.55, False)
            self.box.place(relx=0.1, rely=0.15, anchor=tk.N)
            self.widgetTemp.placeOrHide(self, self.model_label, 0.65, 0.3, False)
            self.widgetTemp.placeOrHide(self, self.model_entry, 0.75, 0.3, False)
            self.widgetTemp.placeOrHide(self, self.tag_label, 0.65, 0.35, False)
            self.widgetTemp.placeOrHide(self, self.tag_entry, 0.75, 0.35, False)
            self.widgetTemp.placeOrHide(self, self.serial_label, 0.65, 0.4, False)
            self.widgetTemp.placeOrHide(self, self.serial_entry, 0.75, 0.4, False)
            self.widgetTemp.placeOrHide(self, self.software_version_label, 0.65, 0.45, False)
            self.widgetTemp.placeOrHide(self, self.software_version_entry, 0.75, 0.45, False)
            self.widgetTemp.placeOrHide(self, self.display_version_label, 0.65, 0.5, False)
            self.widgetTemp.placeOrHide(self, self.display_version_entry, 0.75, 0.5, False)

            if selected_protocol == 'Modbus TCP':
                self.widgetTemp.placeOrHide(self, self.unit_label, 0.22, 0.65, False)
                self.widgetTemp.placeOrHide(self, self.unit_entry, 0.38, 0.65, False)
            else:
                self.widgetTemp.placeOrHide(self, self.unit_label, 0.22, 0.65, True)
                self.widgetTemp.placeOrHide(self, self.unit_entry, 0.38, 0.65, True)
        else:
            # Show hide elements
            self.widgetTemp.placeOrHide(self, self.connection_button, 0.22, 0.35, True)
            self.widgetTemp.placeOrHide(self, self.protocol_entry_label, 0.38, 0.30, True)
            self.widgetTemp.placeOrHide(self, self.protocol_type_dropdown, 0.35, 0.35, True)
            self.widgetTemp.placeOrHide(self, self.host_label, 0.22, 0.45, True)
            self.widgetTemp.placeOrHide(self, self.host_entry, 0.38, 0.45, True)
            self.widgetTemp.placeOrHide(self, self.port_label, 0.22, 0.55, True)
            self.widgetTemp.placeOrHide(self, self.port_entry, 0.38, 0.55, True)
            self.widgetTemp.placeOrHide(self, self.unit_label, 0.22, 0.65, True)
            self.widgetTemp.placeOrHide(self, self.unit_entry, 0.38, 0.65, True)
            self.box.place_forget()

            self.widgetTemp.placeOrHide(self, self.model_label, 0.65, 0.3, True)
            self.widgetTemp.placeOrHide(self, self.model_entry, 0.75, 0.3, True)
            self.widgetTemp.placeOrHide(self, self.tag_label, 0.65, 0.35, True)
            self.widgetTemp.placeOrHide(self, self.tag_entry, 0.75, 0.35, True)
            self.widgetTemp.placeOrHide(self, self.serial_label, 0.65, 0.4, True)
            self.widgetTemp.placeOrHide(self, self.serial_entry, 0.75, 0.4, True)
            self.widgetTemp.placeOrHide(self, self.software_version_label, 0.65, 0.45, True)
            self.widgetTemp.placeOrHide(self, self.software_version_entry, 0.75, 0.45, True)
            self.widgetTemp.placeOrHide(self, self.display_version_label, 0.65, 0.5, True)
            self.widgetTemp.placeOrHide(self, self.display_version_entry, 0.75, 0.5, True)

    def toggle_connection(self, *args):
        # Toggle the Modbus connection based on the current state
        if self.connection_button["text"] == "Connect":
            self.connect_modbus()
        else:
            self.disconnect_modbus()

    def connect_modbus(self):
        # Retrieve the host, port, and unit from the entries
        host = self.host_entry.get()
        port = self.port_entry.get()
        unit = self.unit_entry.get()

        print(f"Retrieved host from dialog: {host}")
        print(f"Retrieved port from dialog: {port}")
        print(f"Retrieved unit from dialog: {unit}")

        if host and port and unit:
            # Check if the port and unit are ints
            if port.isdigit() and unit.isdigit():
                self.modbus_client.update_host_port(host, int(port), int(unit))
                if self.modbus_client.connect():
                    self.connection_button["text"] = "Disconnect"
                    messagebox.showinfo("Connected", "Connection successful")
                else:
                    messagebox.showerror("Error", "Failed to establish Modbus connection.")
            else:
                messagebox.showerror("Error", "Invalid port or unit. Please enter a valid number.")
        else:
            messagebox.showerror("Error", "Please enter the host IP address, port, and unit.")

    def disconnect_modbus(self, *args):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"
