#ModBusProtocolConnection.py
import tkinter as tk
from tkinter import messagebox,ttk
from PIL import Image, ImageTk
class ModBusProtocolConnection:
    def __init__(self, root, modbus_client):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
    def create_widgets(self):

        self.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.add_image("Images/ActBox.png", 150, 150, 0.1, 0.15)

        self.connection_button = self.create_button("Connect",0.22,0.35,14,2,10,self.toggle_connection)
        self.create_connection_entries()

        self.protocol_type_var, self.protocol_entry_label, self.protocol_type_dropdown = self.create_dropdown_menu(
            "Protocol",0.38, ['Modbus TCP', 'Ethernet/IP'], 'Modbus TCP', 0.35, 0.30, self.manage_entries_and_version
        )
        self.rexa_version_type_var, self.rexa_version_entry_label, self.rexa_version_type_dropdown = self.create_dropdown_menu(
            "Rexa Version", 0.77, ['X3', 'NextGen'], 'X3', 0.75, 0.10, self.manage_entries_and_version
        )
        #call at end
        self.manage_entries_and_version()

    def create_button(self, text, relx, rely,font_size,button_height,button_width, command):
        button = tk.Button(self.root, text=text, command=command)
        button.config(font=('Arial', font_size), height=button_height, width=button_width)
        button.place(relx=relx, rely=rely, anchor=tk.NW)
        return button

    def placeOrHide(self, widget, relx, rely, hide):
        if hide == False:
            widget.place(relx=relx, rely=rely, anchor=tk.NW)
        else:
            widget.place_forget()

    def create_connection_entries(self):
        # Create and display the connection entries in the main window
        self.host_label = tk.Label(self.root, text="Host IP Address:")
        self.host_entry = tk.Entry(self.root)

        self.port_label = tk.Label(self.root, text="Modbus Port:")
        self.port_entry = tk.Entry(self.root)

        self.unit_label = tk.Label(self.root, text="Unit:")
        self.unit_entry = tk.Entry(self.root)

    def create_dropdown_menu(self, label_text, label_textX, options, default_option, relx, rely, trace_function):
        # Create a label
        entry_label = tk.Label(self.root, text=label_text)
        entry_label.config(font=('Arial', 14))
        entry_label.place(relx=label_textX, rely=rely, anchor=tk.NW)

        # Create a variable to hold the selected option
        type_var = tk.StringVar(self.main_frame)
        type_var.set(default_option)

        # Create the dropdown menu
        type_dropdown = tk.OptionMenu(self.main_frame, type_var, *options)
        type_dropdown.config(font=('Arial', 14), height=2, width=10)  # Update font and height
        type_dropdown.place(relx=relx, rely=rely + 0.05, anchor=tk.NW)

        # Add a trace to the variable
        type_var.trace('w', trace_function)

        return type_var, entry_label, type_dropdown
    def add_image(self,fileName,Wimage,Himage,Xpos,Ypos):
        # Load the image
        image = Image.open(fileName)
        image = image.resize((Wimage, Himage))  # Resize the image as needed

        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        image_label = tk.Label(self.root, image=photo)
        image_label.image = photo  # Store a reference to the PhotoImage to prevent it from being garbage collected
        image_label.place(relx=Xpos, rely=Ypos, anchor=tk.N)
    def manage_entries_and_version(self, *args):
        selected_version = self.rexa_version_type_var.get()
        selected_protocol = self.protocol_type_var.get()

        if selected_version == 'X3':
            self.placeOrHide(self.connection_button, 0.22, 0.35, False)
            self.placeOrHide(self.protocol_entry_label, 0.38, 0.30, False)
            self.placeOrHide(self.protocol_type_dropdown, 0.35, 0.35, False)
            self.placeOrHide(self.host_label, 0.22, 0.45, False)
            self.placeOrHide(self.host_entry, 0.38, 0.45, False)
            self.placeOrHide(self.port_label, 0.22, 0.55, False)
            self.placeOrHide(self.port_entry, 0.38, 0.55, False)
            if selected_protocol == 'Modbus TCP':
                self.placeOrHide(self.unit_label, 0.22, 0.65, False)
                self.placeOrHide(self.unit_entry, 0.38, 0.65, False)
            else:
                self.placeOrHide(self.unit_label, 0.22, 0.65, True)
                self.placeOrHide(self.unit_entry, 0.38, 0.65, True)
        else:
            self.placeOrHide(self.connection_button, 0.22, 0.35, True)
            self.placeOrHide(self.protocol_entry_label, 0.38, 0.30, True)
            self.placeOrHide(self.protocol_type_dropdown, 0.35, 0.35, True)
            self.placeOrHide(self.host_label, 0.22, 0.45, True)
            self.placeOrHide(self.host_entry, 0.38, 0.45, True)
            self.placeOrHide(self.port_label, 0.22, 0.55, True)
            self.placeOrHide(self.port_entry, 0.38, 0.55, True)
            self.placeOrHide(self.unit_label, 0.22, 0.65, True)
            self.placeOrHide(self.unit_entry, 0.38, 0.65, True)

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

