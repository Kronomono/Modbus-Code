import tkinter as tk
from tkinter import messagebox

class Widgets:
    def __init__(self, root, options):
        self.root = root
        self.options = options
        self.dropdown_menu = None
        self.entry = None
        self.submit_button = None
        self.dark_button = None
        self.selected_type = tk.StringVar(root)
        self.selected_type.set(self.options[0])

    def create_widgets(self):
        self.create_dropdown_menu()
        self.create_entry()
        self.create_submit_button()
        self.create_dark_button()

    def create_dropdown_menu(self):
        self.dropdown_menu = tk.OptionMenu(self.root, self.selected_type, *self.options)
        self.dropdown_menu.config(bg="white", fg="black")
        self.dropdown_menu.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

    def create_entry(self):
        self.entry = tk.Entry(self.root, width=30)
        self.entry.config(bg="white", fg="black")
        self.entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def create_submit_button(self):
        self.submit_button = tk.Button(self.root, text="Submit", command=self.handle_submit)
        self.submit_button.config(bg="white", fg="black")
        self.submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def create_dark_button(self):
        self.dark_button = tk.Button(self.root, text="Dark Mode", command=self.toggle_dark_mode)
        self.dark_button.place(relx=0.95, rely=0.05, anchor=tk.NE)

    def handle_submit(self):
        input_value = self.entry.get()
        print(f"Submitted value: {input_value}")
        print(f"Selected type: {self.selected_type.get()}")

        try:
            if self.selected_type.get() == "Float":
                input_value = float(input_value)
                print("Type is float")
            elif self.selected_type.get() == "Signed 16-bit":
                input_value = int(input_value)
                print("Type is Signed 16 bit int")
            elif self.selected_type.get() == "Unsigned 16-bit":
                input_value = int(input_value)
                print("Type is Unsigned 16 bit int")
            elif self.selected_type.get() == "Boolean":
                input_value = bool(input_value)
                print("Type is Boolean")
            elif self.selected_type.get() == "ASCII":
                print("Type is ASCII")
            else:
                raise ValueError("Invalid selection")
        except ValueError:
            messagebox.showerror("Error", "Invalid input value. Please try again.")

    def toggle_dark_mode(self):
        current_bg = self.root.cget("bg")

        if current_bg == "white":
            self.root.configure(bg="black")
            self.dropdown_menu.configure(bg="black", fg="white")
            self.entry.configure(bg="black", fg="white")
            self.submit_button.configure(bg="black", fg="white")
            self.dark_button.configure(text="Light Mode")
        else:
            self.root.configure(bg="white")
            self.dropdown_menu.configure(bg="white", fg="black")
            self.entry.configure(bg="white", fg="black")
            self.submit_button.configure(bg="white", fg="black")
            self.dark_button.configure(text="Dark Mode")