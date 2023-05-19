#Widgets.py
import tkinter as tk
from tkinter import messagebox

class Widgets:
    def __init__(self, root, options, modbus_client):
        # Initialize the widget with a root window, options, and a Modbus client
        self.root = root
        self.options = options
        self.modbus_client = modbus_client
        self.dropdown_menu = None
        self.entry = None
        self.submit_button = None

        # Define the types and registers available
        self.selected_type = tk.StringVar(root)
        self.selected_type.set(self.options[0])
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

    def create_dropdown_menu(self):
        # Create the dropdown menu for types and place it in the window
        self.dropdown_menu = tk.OptionMenu(self.root, self.selected_type, *self.options)
        self.dropdown_menu.config(bg="white", fg="black")
        self.dropdown_menu.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

    def create_entry(self):
        # Create the entry field for input values and place it in the window
        self.entry = tk.Entry(self.root, width=30)
        self.entry.config(bg="white", fg="black")
        self.entry.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def create_submit_button(self):
        # Create the Submit button and place it in the window
        self.submit_button = tk.Button(self.root, text="Submit", command=self.handle_submit)
        self.submit_button.config(bg="white", fg="black")
        self.submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def create_register_dropdown_menu(self):
        # Create the dropdown menu for registers and place it in the window
        self.register_dropdown_menu = tk.OptionMenu(self.root, self.selected_register, *self.available_registers.keys())
        self.register_dropdown_menu.config(bg="white", fg="black")
        self.register_dropdown_menu.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

    def handle_submit(self):
        # Get the input value, selected type, and selected register, and write the value to the register
        input_value = self.entry.get()
        address_value = self.available_registers[self.selected_register.get()]
        print(f"Submitted value: {input_value}")
        print(f"Selected type: {self.selected_type.get()}")
        print(f"Address value: {address_value}")

        try:
            if self.selected_type.get() == "Float":
                input_value = float(input_value)
                self.modbus_client.write_float(address_value, input_value)
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