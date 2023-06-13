#ModBusProtocolConnection.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from PIL import Image, ImageTk


class ModBusProtocolConnection:
    def __init__(self, root, modbus_client):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client


        self.connection_button = None

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
    def create_widgets(self):
        # Create the Connect
        self.create_connection_button()
        self.add_image("rexa logo.png",300,50,0.5,0)

        # Drop down menu protocol
        self.protocol_entry_label = tk.Label(self.root, text="Protocol")
        self.protocol_entry_label.config(font=('Arial', 14))
        self.protocol_entry_label.place(relx=0.38, rely=0.30, anchor=tk.NW)
        self.protocol_type_var = tk.StringVar(self.main_frame)
        self.protocol_options = ['Modbus TCP', 'Ethernet/IP']
        self.protocol_type_var.set(self.protocol_options[0])
        self.protocol_type_dropdown = tk.OptionMenu(self.main_frame, self.protocol_type_var, *self.protocol_options)
        self.protocol_type_dropdown.config(font=('Arial', 14), height=2, width= 10)  # Update font and height
        self.protocol_type_dropdown.place(relx=0.35, rely=0.35, anchor=tk.NW)
        #self.protocol_type_var.trace('w', self.print_selected_option)

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


    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.config(font=('Arial', 14), height= 2, width = 10 )  # Update font and height
        self.connection_button.place(relx=0.22, rely=0.35, anchor=tk.NW)

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

            unit_label = tk.Label(dialog, text="Unit:")
            unit_label.pack()
            unit_entry = tk.Entry(dialog)
            unit_entry.pack()

            def connect():
                # Retrieve the host, port, and unit from the dialog
                host = host_entry.get()
                port = port_entry.get()
                unit = unit_entry.get()

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
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid port or unit. Please enter a valid number.")
                else:
                    messagebox.showerror("Error", "Please enter the host IP address, port, and unit.")

            connect_button = tk.Button(dialog, text="Connect", command=connect)
            connect_button.pack()

            dialog.transient(self.root)
            dialog.title("Modbus Connection Settings")
            dialog.geometry("400x400")  # Set the width and height of the dialog window
            dialog.grab_set()
            self.root.wait_window(dialog)
    def toggle_connection(self,*args):
        selected_option = self.protocol_type_var.get()
        print("Selected option:", selected_option)
        # Toggle the Modbus connection based on the current state
        if self.connection_button["text"] == "Connect" and selected_option == 'Modbus TCP':
            self.show_connection_dialog()
        else:
            self.disconnect_modbus()

    def disconnect_modbus(self,*args):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"

