#ModbusMasterClientWidget.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading

from Names import Names

class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client

        self.names = Names()

        self.connection_button = None
        self.retrieve_button = None

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Create a second frame to hold the table and the scrollbar
        self.frame = tk.Frame(self.main_frame)
        #.frame.pack(side='bottom', fill='x', expand=True)
        self.frame.place(relx=0.5, rely=0.6, anchor='center', relwidth=1, relheight=0.75)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the table
        self.table = ttk.Treeview(self.frame, columns=("Name", "Address", "Type", "Registry"), show='headings')
        self.table.heading("Address", text="Address")
        self.table.heading("Type", text="Type")
        self.table.heading("Registry", text="Registry")
        self.table.heading("Name", text="Name")
        self.table.pack(fill='both', expand=True)

        # Link the scrollbar to the table
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.table.yview)

        # Create the data type dropdown
        self.data_type_var = tk.StringVar(self.root)
        self.data_type_options = ['holding', 'Float 32 bit', 'ASCII 16 bit', 'Epoch 32 bit', 'Binary','Unsigned Int 16 bit', 'Boolean', 'Byte',
                                  'Signed Int 32 bit', 'Unsigned Int 32 bit','Unsigned Int 8 bit', 'ALL']

        self.data_type_var.set(self.data_type_options[0])
        self.data_type_dropdown = tk.OptionMenu(self.root, self.data_type_var, *self.data_type_options)
        self.data_type_dropdown.place(relx=0.05, rely=0.11, anchor=tk.NW)
        # Add a trace to the data_type_var
        self.data_type_var.trace('w', self.refresh_table)

        self.count_entry = self.create_count_entry()
        self.progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        self.progress.place(relx=0.5, rely=0.2, relwidth=0.8, anchor=tk.CENTER)
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)


    def create_widgets(self):
        # Create the Connect, Retrieve Data
        self.create_connection_button()
        self.create_retrieve_button()

    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def create_count_entry(self):
        # create a count entry field and place in window
        count_entry_label = tk.Label(self.root, text="Enter # of addresses to read")
        count_entry = tk.Entry(self.root,width=10)
        # placements
        count_entry_label.place(relx=0.55, rely=0.03, anchor=tk.CENTER)
        count_entry.place(relx=0.5, rely=0.05, anchor=tk.NW)
        return count_entry

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


    def toggle_connection(self):
        # Toggle the Modbus connection based on the current state
        if self.connection_button["text"] == "Connect":
            self.show_connection_dialog()
        else:
            self.disconnect_modbus()

    def disconnect_modbus(self,*args):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"
    def retrieve_data(self, *args):
        if self.modbus_client.is_connected():
            threading.Thread(target=self.retrieve_data_thread).start()
        else:
            messagebox.showerror("Error", "Modbus connection is not open.")
    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        MAX_REQUESTS_PER_SECOND = 50  # Increase this number to increase the polling rate
        # Retrieve data from the Modbus server
        # Create a rate limiter
        rate_limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=1.0)
        try:
            unit = self.modbus_client.unit
            print(f"This is unit in ModbusMasterClientWidget.py {unit}")
            count = int(self.count_entry.get())
            raw_values = []  # Initialize raw_values outside the loop
            self.raw_values = raw_values
            self.progress['maximum'] = count  # Set the maximum value of the progress bar to the total number of addresses to read
            self.progress['value'] = 0  # Reset the progress bar
            for address in range(0, count):  # Modbus address space is 0-65535
                with rate_limiter:
                    try:
                        result = self.modbus_client.client.read_holding_registers(address, 1 , unit)
                        if not result.isError():
                            raw_values.append(result.registers[0])
                            self.progress['value'] += 1  # Increment the progress bar
                            self.progress_label['text'] = f"{self.progress['value']}/{count}"  # Update the label text
                            self.root.update_idletasks()  # Update the GUI
                        else:
                            print(f"Error reading register at address {address}: {result}")
                            messagebox.showerror("Error",f"Error reading register at address {address}: {result}")
                            break;
                    except Exception as e:
                        print(f"Exception while reading register at address {address}: {e}")
            # Print the number of elements in raw_values
            print(f"Number of elements in raw_values: {len(raw_values)}")

            self.refresh_table(raw_values)
        except ValueError:
            print("Invalid unit or count value. Please enter a valid number.")
            messagebox.showerror("Error", "Invalid unit or count value. Please enter a valid number.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")
        finally:
            self.progress['value'] = 0  # Reset the progress bar

    def refresh_table(self,*args):
        try:
            raw_values = self.raw_values
        except AttributeError:
            print(f"Did not retrieve data")
            messagebox.showerror("Error", "Retrieve Data First")
        self.table.delete(*self.table.get_children())
        selected_type = self.data_type_var.get()  # Define selected_type before using it
        float_indices = [0, 1, 2, 3, 4, 5, 25, 26, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                         117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                         129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
                         141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
                         153, 154, 155, 156, 157, 158, 159, 160, 313, 314, 569, 570]

        ASCII16bit_indices = [205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
                              220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234,
                              235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249,
                              250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264,
                              265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
                              280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
                              295, 296, 297, 298, 299, 300, 301, 302,
                              303]
        Signed32Int_indices = [6, 7, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
                               44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
                               63, 64, 65, 66, 67, 68, 69, 70]
        UnsignedInt16bit_indices = [12, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
                                    98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                                    113, 114, 115, 116, 161, 162, 163, 164, 165, 166,170, 171,
                                    172, 173, 306, 312, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429,
                                    430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444,
                                    445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459,
                                    460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474,
                                    475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489,
                                    490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504,
                                    505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
                                    520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534,
                                    535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549,
                                    550, 551, 552, 553, 554, 555, 556, 557, 566]
        Unsigned32Int_indices = [315, 316, 558, 559, 560, 561, 562, 563, 564,565]
        boolean_indices = [174,175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
                           191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 567,
                           568]
        Unsigned8bit_indices = [167,168,169]

        byte_indices = [304, 305, 307, 308, 309, 310, 311]
        if selected_type == "ALL":

            # Combine all indices into one list
            all_indices = float_indices + ASCII16bit_indices + Signed32Int_indices + UnsignedInt16bit_indices + Unsigned32Int_indices + boolean_indices

            # Sort the list
            all_indices.sort()

            # Process each index
            for i in range(len(all_indices)):
                index = all_indices[i]
                value = raw_values[index]

                # Determine the type of the index and translate the value accordingly
                if index in float_indices:
                    # Check if this is the first index of a pair
                    if index + 1 in float_indices:
                        value2 = raw_values[index + 1]
                        translated_value = self.modbus_client.translate_value("Float 32 bit", value, value2)
                        data_type = "Float 32 bit"
                    else:
                        continue
                elif index in ASCII16bit_indices:
                    translated_value = self.modbus_client.translate_value("ASCII 16 bit", value)
                    data_type = "ASCII 16 bit"
                elif index in byte_indices:
                    translated_value = self.modbus_client.translate_value(("Byte"), value)
                    data_type = "Byte"
                elif index in Signed32Int_indices:
                    # Check if this is the first index of a pair
                    if index + 1 in Signed32Int_indices and i + 1 < len(all_indices) and all_indices[
                        i + 1] == index + 1:
                        value2 = raw_values[index + 1]
                        translated_value = self.modbus_client.translate_value("Signed Int 32 bit", value, value2)
                        data_type = "Signed Int 32 bit"
                    else:
                        continue
                elif index in UnsignedInt16bit_indices:
                    translated_value = self.modbus_client.translate_value("Unsigned Int 16 bit", value)
                    data_type = "Unsigned Int 16 bit"
                elif index in Unsigned32Int_indices:
                    # Check if this is the first index of a pair
                    if index + 1 in Unsigned32Int_indices and i + 1 < len(all_indices) and all_indices[
                        i + 1] == index + 1:
                        value2 = raw_values[index + 1]
                        translated_value = self.modbus_client.translate_value("Unsigned Int 32 bit", value, value2)
                        data_type = "Unsigned Int 32 bit"
                    else:
                        continue
                elif index in boolean_indices:
                    translated_value = self.modbus_client.translate_value("Boolean", value)
                    data_type = "Boolean"
                elif index in Unsigned8bit_indices:
                    translated_value = self.modbus_client.translate_value("Unsigned Int 8 bit", value)
                    data_type = "Unsigned Int 8 bit"
                else:
                    translated_value = self.modbus_client.translate_value("holding", value)
                    data_type = "holding"
                self.table.insert('', 'end', values=(self.names.get_name(index + 1), index + 1, data_type, translated_value))

        elif selected_type == "Float 32 bit":

            for i in range(0, len(float_indices), 2):  # Step by 2
                index1 = float_indices[i]
                index2 = float_indices[i + 1] if i + 1 < len(float_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.modbus_client.translate_value("Float 32 bit", value1, value2)
                translated_value = round(translated_value, 3)
                self.table.insert('', 'end',values=(self.names.get_name(index1 + 1), index1 + 1, "Float 32 bit", translated_value))
        elif selected_type == "ASCII 16 bit":
            for i in range(0, len(ASCII16bit_indices)):
                index1 = ASCII16bit_indices[i]
                value1 = raw_values[index1]
                translated_value = self.modbus_client.translate_value("ASCII 16 bit", value1)
                self.table.insert('', 'end',values=(self.names.get_name(index1 + 1), index1 + 1, "ASCII 16 bit", translated_value))
        elif selected_type == "Byte":
            for i in range(0, len(byte_indices)):
                index1 = byte_indices[i]
                value1 = raw_values[index1]
                translated_value = self.modbus_client.translate_value("Byte", value1)
                self.table.insert('', 'end', values=(self.names.get_name(index1 + 1), index1 + 1, "Byte", translated_value))
        elif selected_type == "Unsigned Int 8 bit":
            for i in range(0, len(Unsigned8bit_indices)):
                index1 = Unsigned8bit_indices[i]
                value1 = raw_values[index1]
                translated_value = self.modbus_client.translate_value("Unsigned Int 8 bit", value1)
                # translated_value =   round(translated_value,2)
                self.table.insert('', 'end', values=(self.names.get_name(index1 + 1), index1 + 1, "Unsigned Int 8 bit", translated_value))
        elif selected_type == "Signed Int 32 bit":
            for i in range(0, len(Signed32Int_indices), 2):  # Step by 2
                index1 = Signed32Int_indices[i]
                index2 = Signed32Int_indices[i + 1] if i + 1 < len(
                    Signed32Int_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.modbus_client.translate_value("Signed Int 32 bit", value1, value2)
                self.table.insert('', 'end',values=(self.names.get_name(index1 + 1), index1 + 1, "Signed Int 32 bit", translated_value))
        elif selected_type == "Unsigned Int 16 bit":
            for i in range(0, len(UnsignedInt16bit_indices)):
                index1 = UnsignedInt16bit_indices[i]
                value1 = raw_values[index1]
                translated_value = self.modbus_client.translate_value("Unsigned Int 16 bit", value1)
                self.table.insert('', 'end',values=(self.names.get_name(index1 + 1), index1 + 1, "Unsigned Int 16 bit", translated_value))
        elif selected_type == "Unsigned Int 32 bit":
            for i in range(0, len(Unsigned32Int_indices), 2):  # Step by 2
                index1 = Unsigned32Int_indices[i]
                index2 = Unsigned32Int_indices[i + 1] if i + 1 < len(
                    Unsigned32Int_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.modbus_client.translate_value("Unsigned Int 32 bit", value1, value2)
                self.table.insert('', 'end', values=(self.names.get_name(index1 + 1), index1 + 1, "Unsigned Int 32 bit", translated_value))
        elif selected_type == "Boolean":
            for i in range(0, len(boolean_indices)):
                index1 = boolean_indices[i]
                value1 = raw_values[index1]
                translated_value = self.modbus_client.translate_value("Boolean", value1)
                self.table.insert('', 'end',values=(self.names.get_name(index1 + 1), index1 + 1, "Boolean", translated_value))
        elif selected_type == "Binary":
            # Insert raw_values into the table
            for i, value in enumerate(raw_values):
                translated_value = self.modbus_client.translate_value("Binary", value)  # Translate the value
                self.table.insert('', 'end', values=(self.names.get_name(i + 1), i + 1, selected_type, translated_value))  # Use the translated value
        else:
            # Insert raw_values into the table
            for i, value in enumerate(raw_values):
                translated_value = self.modbus_client.translate_value("holding", value)  # Translate the value
                self.table.insert('', 'end', values=(self.names.get_name(i + 1), i + 1, selected_type, translated_value))  # Use the translated value
