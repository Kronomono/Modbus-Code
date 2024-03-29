#WidgetTemplateCreator.py
import tkinter as tk
from tkinter import messagebox,ttk
from PIL import Image, ImageTk

class WidgetTemplateCreator:
    def __init__(self, root):
        # references to other classes
        self.root = root


    def create_button(self, text, relx, rely, fontSize, buttonHeight, buttonWidth, command):
        button = tk.Button(self.root, text=text, command=command)
        button.config(font=('Arial', fontSize), height=buttonHeight, width=buttonWidth)
        button.place(relx=relx, rely=rely, anchor=tk.NW)
        return button

    def create_entry(self, relx, rely, width, readOnly, preFilledText=None):
        entry = tk.Entry(self.root, width=width)
        if preFilledText is not None:
            entry.insert(0, preFilledText)
        if readOnly:
            entry.configure(state="readonly")
        entry.place(relx=relx, rely=rely, anchor=tk.NW)
        return entry
    def create_label(self,label_text,relx,rely):
        label = tk.Label(self.root,text=label_text)
        self.placeOrHide(label,relx,rely,False)
        return label

    def create_label_and_entry(self, label_text, label_relx, label_rely, entry_relx, entry_rely, entry_width,entry_readOnly, preFilledText):
        # Create the label
        label = tk.Label(self.root, text=label_text)
        self.placeOrHide(label, label_relx, label_rely, False)

        # Create the entry
        entry = self.create_entry(entry_relx, entry_rely, entry_width, entry_readOnly, preFilledText)

        return label, entry

    def placeOrHide(self, widget, relx, rely, hide):
        if hide == False:
            widget.place(relx=relx, rely=rely, anchor=tk.NW)
        else:
            widget.place_forget()

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
        return image_label

    def create_dropdown_menu2(self, label_text,label_textX, options, default_option, relx, rely, trace_function):
        # Create a label
        entry_label = tk.Label(self.root, text=label_text)
        entry_label.config(font=('Arial', 10))
        entry_label.place(relx=label_textX, rely=rely, anchor=tk.NW)

        # Create a variable to hold the selected option
        type_var = tk.StringVar(self.root)
        type_var.set(default_option)

        # Create the dropdown menu
        type_dropdown = tk.OptionMenu(self.root, type_var, *options)
        type_dropdown.config(font=('Arial', 10))  # Update font
        type_dropdown.place(relx=relx, rely=rely + 0.03, anchor=tk.NW)

        # Add a trace to the variable
        type_var.trace('w', trace_function)

        # Call the function with the initial option
        trace_function()

        return type_var, entry_label, type_dropdown



