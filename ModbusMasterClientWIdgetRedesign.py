# ModBusProtocolConnection.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from PIL import Image, ImageTk


class ModBusProtocolConnection:
    def __init__(self, root, modbus_client):
        # references to other classes
        self.root = root
        self.modbus_client = modbus_client

        self.connection_button = None
        self.protocol_type_var.trace('w', self.entries_manager())

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

    def create_widgets(self):
        # Create the Connect
        self.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.add_image("Images/ActBox.png", 150, 150, 0.1, 0.15)
        self.create_connection_button()
        self.create_protocol_dropdown_menu()
        self.create_connection_entries()

    def create_protocol_dropdown_menu(self):
        # Drop down menu protocol
        self.protocol_entry_label = tk.Label(self.root, text="Protocol")
        self.protocol_entry_label.config(font=('Arial', 14))
        self.protocol_entry_label.place(relx=0.38, rely=0.30, anchor=tk.NW)
        self.protocol_type_var = tk.StringVar(self.main_frame)
        self.protocol_options = ['Modbus TCP', 'Ethernet/IP']
        self.protocol_type_var.set(self.protocol_options[0])
        self.protocol_type_dropdown = tk.OptionMenu(self.main_frame, self.protocol_type_var, *self.protocol_options)
        self.protocol_type_dropdown.config(font=('Arial', 14), height=2, width=10)  # Update font and height
        self.protocol_type_dropdown.place(relx=0.35, rely=0.35, anchor=tk.NW)
        # self.protocol_type_var.trace('w', self.print_selected_option)

    def add_image(self, fileName, Wimage, Himage, Xpos, Ypos):
        # Load the image
        image = Image.open(fileName)
        image = image.resize((Wimage, Himage))  # Resize the image as needed

        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        image_label = tk.Label(self.root, image=photo)
        image_label.image = photo  # Store a reference to the PhotoImage to prevent it from being garbage collected
        image_label.place(relx=Xpos, rely=Ypos, anchor=tk.N)

    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.config(font=('Arial', 14), height=2, width=10)  # Update font and height
        self.connection_button.place(relx=0.22, rely=0.35, anchor=tk.NW)

    def create_connection_entries(self):
        # Create and display the connection entries in the main window
        self.host_label = tk.Label(self.root, text="Host IP Address:")
        # self.host_label.place(relx=0.22, rely=0.45, anchor=tk.NW)
        self.host_entry = tk.Entry(self.root)
        # self.host_entry.place(relx=0.38, rely=0.45, anchor=tk.NW)

        self.port_label = tk.Label(self.root, text="Modbus Port:")
        # self.port_label.place(relx=0.22, rely=0.55, anchor=tk.NW)
        self.port_entry = tk.Entry(self.root)
        # self.port_entry.place(relx=0.38, rely=0.55, anchor=tk.NW)

        self.unit_label = tk.Label(self.root, text="Unit:")
        # self.unit_label.place(relx=0.22, rely=0.65, anchor=tk.NW)
        self.unit_entry = tk.Entry(self.root)
        # self.unit_entry.place(relx=0.38, rely=0.65, anchor=tk.NW)

    def entries_manager(self, *args):
        selected_option = self.protocol_type_var.get()

        self.host_label.place(relx=0.22, rely=0.45, anchor=tk.NW)
        self.host_entry.place(relx=0.38, rely=0.45, anchor=tk.NW)

        self.port_label.place(relx=0.22, rely=0.55, anchor=tk.NW)
        self.port_entry.place(relx=0.38, rely=0.55, anchor=tk.NW)
        if selected_option == 'Modbus TCP':
            self.unit_label.place(relx=0.22, rely=0.65, anchor=tk.NW)
            self.unit_entry.place(relx=0.38, rely=0.65, anchor=tk.NW)
        else:
            self.unit_label.place_forget()  # Hide the unit label
            self.unit_entry.place_forget()  # Hide the unit entry

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

