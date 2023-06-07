#Widget.py
import tkinter as tk
from tkinter import messagebox, ttk
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
class Widgets:
    def __init__(self, root, options, modbus_client):
        # Initialize the widget with a root window, options, and a Modbus client
        self.root = root
        self.options = options
        self.modbus_client = modbus_client
        self.dropdown_menu = None
        self.entry = None
        self.submit_button = None
        self.add_address_button = None
        self.add_address_entry = None


        # Define the types and registers available
        self.selected_type = tk.StringVar(root)
        self.selected_type.set(self.options[0])
        self.selected_type.trace("w", self.create_entry)  # Bind create_entry to selected_type change
        self.available_registers = {
            "Register 0": 0x0000,
            "Register 1": 0x0001,
            "Register 2": 0x0002,
            "Register 3": 0x0003,
            "Register 4": 0x0004,
            "Register 5": 0x0005,
            "Register 6": 0x0006,
            "Register 7": 0x0007,
            "Register 8": 0x0008,
            "Register 9": 0x0009,
            # ... add more registers as necessary ...
        }
        self.selected_register = tk.StringVar(self.root)
        self.selected_register.set(list(self.available_registers.keys())[0])
        self.register_dropdown_menu = None


    def create_widgets(self):
        # Create all the widgets for the application
        self.create_register_dropdown_menu()
        self.create_dropdown_menu()
        self.create_entry()
        self.create_submit_button()
        self.create_add_address_entry()
        self.create_add_address_button()

    def create_dropdown_menu(self):
        # Create the dropdown menu for types and place it in the window
        self.dropdown_menu = tk.OptionMenu(self.root, self.selected_type, *self.options)
        self.dropdown_menu.config(bg="white", fg="black")
        self.dropdown_menu.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

    def create_entry(self, *args):
        # Destroy the existing entry widget if it exists
        if self.entry is not None:
            self.entry.destroy()

        # Create the entry field or dropdown menu for input values and place it in the window
        if self.selected_type.get() == "Boolean":
            self.entry = ttk.Combobox(self.root, values=["True", "False"], state="readonly")
        else:
            self.entry = tk.Entry(self.root, width=30)

        self.entry.configure(background="white", foreground="black")
        self.entry.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def create_submit_button(self):
        # Create the Submit button and place it in the window
        self.submit_button = tk.Button(self.root, text="Submit", command=self.handle_submit)
        self.submit_button.config(bg="white", fg="black")
        self.submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def create_register_dropdown_menu(self):
        # Create the dropdown menu for registers and place it in the window
        self.register_dropdown_menu = ttk.Combobox(self.root, textvariable=self.selected_register, values=list(self.available_registers.keys()), state='readonly')
        self.register_dropdown_menu.place(relx=0.37, rely=0.6, anchor=tk.CENTER)

    def create_add_address_button(self):
        # Create the Add button and place it in the window
        self.add_address_button = tk.Button(self.root, text="Add address", command=self.add_address)
        self.add_address_button.config(bg="white", fg="black")
        self.add_address_button.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

    def create_add_address_entry(self):
        #Create instructions for Hexdecimal input
        hexdecimal_label = tk.Label(self.root, text = "To add Hexadecimal input start with 0x")
        #hexdecimal_label.config(bg="white", fg="black")
        hexdecimal_label.place(relx=0.6, rely=0.45, anchor=tk.CENTER)
        # Create the entry field for input values and place it in the window
        self.add_address_entry = tk.Entry(self.root, width=30)
        self.add_address_entry.config(bg="white", fg="black")
        self.add_address_entry.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

    def add_address(self):
        # Get the input address, add it to the available registers, and update the dropdown menu
        input_address = self.add_address_entry.get()
        print(f"Added address: {input_address}")

        try:
            if input_address.startswith('0x'):  # Hexadecimal input
                address_value = int(input_address, 16)  # Converts hex string to integer
                print(f"Hex value to inter: {address_value}")
            else:  # Integer input
                address_value = int(input_address)

            self.available_registers[f"Register {input_address}"] = address_value
            self.selected_register.set(f"Register {input_address}")
            # Update the values in the dropdown menu to include the new addresses
            self.register_dropdown_menu['values'] = list(self.available_registers.keys())
        except ValueError:
            messagebox.showerror("Error", "Invalid input address. Please try again.")


    def handle_submit(self):
        # Get the input value, selected type, and selected register, and write the value to the register
        input_value = self.entry.get()
        address_value = self.available_registers[self.selected_register.get()]
        print(f"Submitted value: {input_value}")
        print(f"Selected type: {self.selected_type.get()}")
        print(f"Address value: {address_value}")

        try:
            if self.selected_type.get() == "Boolean":
                input_value = input_value.lower()  # Convert input to lowercase for case-insensitive comparison
                if input_value == "true":
                    input_value = 1
                elif input_value == "false":
                    input_value = 0
                else:
                    raise ValueError("Invalid boolean value")

            if self.selected_type.get() == "Float":
                # Split the input values by whitespace and convert each value to a float
                input_values = [float(value) for value in input_value.split()]
                # Write each float value to consecutive registers
                for i, value in enumerate(input_values):
                    self.modbus_client.write_float(address_value + i, value)
            elif self.selected_type.get() == "Signed 16-bit":
                input_value = int(input_value)
                self.modbus_client.write_register(address_value, input_value)
            elif self.selected_type.get() == "Unsigned 16-bit":
                input_value = int(input_value)
                self.modbus_client.write_register(address_value, input_value)
            elif self.selected_type.get() == "Boolean":
                input_value = bool(input_value)
                self.modbus_client.write_register(address_value, input_value)
            elif self.selected_type.get() == "ASCII":
                self.modbus_client.write_ascii(address_value, input_value)
            else:
                raise ValueError("Invalid selection")

        except ValueError:
            messagebox.showerror("Error", "Invalid input value. Please try again.")