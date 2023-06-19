#ModBusProtocolConnection.py
import tkinter as tk
from tkinter import messagebox,ttk
from WidgetTemplateCreator import  WidgetTemplateCreator
from ModBusProtocolStatus import  ModBusProtocolStatus
class ModBusProtocolConnection:
    def __init__(self, root, modbus_client):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.widgetTemp = WidgetTemplateCreator
        self.modbus_status = ModBusProtocolStatus



        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
    def create_widgets(self):
        self.connection_button = self.widgetTemp.create_button(self,"Connect",0.22,0.35,14,2,10,self.toggle_connection)

        self.widgetTemp.add_image(self,"Images/rexa logo.png", 300, 50, 0.5, 0)
        self.widgetTemp.add_image(self,"Images/ActBox.png", 150, 150, 0.1, 0.15)

        self.host_label = tk.Label(self.root, text="Host IP Address:")
        self.host_entry = self.widgetTemp.create_entry(self,0.22,0.45,20,False,"192.168.1.100")

        self.port_label = tk.Label(self.root, text="Modbus Port:")
        self.port_entry =  self.widgetTemp.create_entry(self,0.22,0.55,20,False,"2011")

        self.unit_label = tk.Label(self.root, text="Unit:")
        self.unit_entry =  self.widgetTemp.create_entry(self,0.22,0.65,20,False,"10")

        self.protocol_type_var, self.protocol_entry_label, self.protocol_type_dropdown = self.widgetTemp.create_dropdown_menu(self,
            "Protocol",0.38, ['Modbus TCP', 'Ethernet/IP'], 'Modbus TCP', 0.35, 0.30, self.manage_entries_and_version
        )
        self.rexa_version_type_var, self.rexa_version_entry_label, self.rexa_version_type_dropdown = self.widgetTemp.create_dropdown_menu(self,
            "Rexa Version", 0.77, ['X3', 'NextGen'], 'X3', 0.75, 0.10, self.manage_entries_and_version
        )
        #call at end
        self.manage_entries_and_version()


    def manage_entries_and_version(self, *args):
        selected_version = self.rexa_version_type_var.get()
        selected_protocol = self.protocol_type_var.get()
        if selected_version == 'X3':
            self.widgetTemp.placeOrHide(self,self.connection_button, 0.22, 0.35, False)
            self.widgetTemp.placeOrHide(self,self.protocol_entry_label, 0.38, 0.30, False)
            self.widgetTemp.placeOrHide(self,self.protocol_type_dropdown, 0.35, 0.35, False)
            self.widgetTemp.placeOrHide(self,self.host_label, 0.22, 0.45, False)
            self.widgetTemp.placeOrHide(self,self.host_entry, 0.38, 0.45, False)
            self.widgetTemp.placeOrHide(self,self.port_label, 0.22, 0.55, False)
            self.widgetTemp.placeOrHide(self,self.port_entry, 0.38, 0.55, False)

            if selected_protocol == 'Modbus TCP':
                self.widgetTemp.placeOrHide(self,self.unit_label, 0.22, 0.65, False)
                self.widgetTemp.placeOrHide(self,self.unit_entry, 0.38, 0.65, False)
            else:
                self.widgetTemp.placeOrHide(self,self.unit_label, 0.22, 0.65, True)
                self.widgetTemp.placeOrHide(self,self.unit_entry, 0.38, 0.65, True)
        else:
            self.widgetTemp.placeOrHide(self,self.connection_button, 0.22, 0.35, True)
            self.widgetTemp.placeOrHide(self,self.protocol_entry_label, 0.38, 0.30, True)
            self.widgetTemp.placeOrHide(self,self.protocol_type_dropdown, 0.35, 0.35, True)
            self.widgetTemp.placeOrHide(self,self.host_label, 0.22, 0.45, True)
            self.widgetTemp.placeOrHide(self,self.host_entry, 0.38, 0.45, True)
            self.widgetTemp.placeOrHide(self,self.port_label, 0.22, 0.55, True)
            self.widgetTemp.placeOrHide(self,self.port_entry, 0.38, 0.55, True)
            self.widgetTemp.placeOrHide(self,self.unit_label, 0.22, 0.65, True)
            self.widgetTemp.placeOrHide(self,self.unit_entry, 0.38, 0.65, True)

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

    def disconnect_modbus(self,*args):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"
