#ModBusProtocolStatus.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator


class ModBusProtocolStatus:
    def __init__(self, root, modbus_client,modbus_protocol_connection):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.names = Names()
        self.ModBusProtocolConnection = modbus_protocol_connection
        self.widgetTemp = WidgetTemplateCreator(self.root)




        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)


    def create_widgets(self):
        # Create the Connect
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        self.manage_UI()

    def create_label_and_entry(self, label_text, label_relx, label_rely, entry_relx, entry_rely, entry_width,entry_readOnly, preFilledText=None):
        # Create the label
        label = tk.Label(self.root, text=label_text)
        self.widgetTemp.placeOrHide(label, label_relx, label_rely, False)

        # Create the entry
        entry = self.widgetTemp.create_entry(entry_relx, entry_rely, entry_width, entry_readOnly, preFilledText)

        return label, entry

    def manage_widgets_visibility(self, *args):
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        selected_protocol = self.ModBusProtocolConnection.protocol_type_var.get()

        if selected_version == 'X3':
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.05, 0.93, False)
            self.widgetTemp.placeOrHide(self.progress_bar, 0.1, 0.97, False)
            self.widgetTemp.placeOrHide(self.current_operational_mode_label,0,0.07,False)
            self.widgetTemp.placeOrHide(self.current_operational_mode_entry,0.01,0.1,False)
            self.widgetTemp.placeOrHide(self.operational_status_label,0.14,0.07,False)
            self.widgetTemp.placeOrHide(self.operational_status_entry,0.15,0.1,False)
            self.widgetTemp.placeOrHide(self.control_command_label,0,0.17,False)
            self.widgetTemp.placeOrHide(self.control_command_entry,0.01,0.2,False)
            self.widgetTemp.placeOrHide(self.actuator_position_label,0.14,0.17,False)
            self.widgetTemp.placeOrHide(self.actuator_position_entry,0.15,0.2,False)
            self.widgetTemp.placeOrHide(self.deviation_label,0.24,0.34,False)
            self.widgetTemp.placeOrHide(self.deviation_entry,0.23,0.37,False)
            self.widgetTemp.placeOrHide(self.position_transmitter_label,0.22,0.57,False)
            self.widgetTemp.placeOrHide(self.position_transmitter_entry,0.23,0.60,False)
            self.widgetTemp.placeOrHide(self.warning_status_label,0.005,0.67,False)
            self.widgetTemp.placeOrHide(self.warning_status_entry, 0.01, 0.7, False)
            self.widgetTemp.placeOrHide(self.alarm_status_label,0.15,0.67,False)
            self.widgetTemp.placeOrHide(self.alarm_status_entry, 0.15, 0.7, False)
            self.widgetTemp.placeOrHide(self.accumulator_pressure_label,0.43,0.67,False)
            self.widgetTemp.placeOrHide(self.accumulator_pressure_entry,0.45,0.7,False)
        else:
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.05, 0.93, True)
            self.widgetTemp.placeOrHide(self.progress_bar, 0.1, 0.97, True)
            self.widgetTemp.placeOrHide(self.current_operational_mode_label, 0, 0.07, True)
            self.widgetTemp.placeOrHide(self.current_operational_mode_entry, 0.01, 0.1, True)
            self.widgetTemp.placeOrHide(self.operational_status_label,0.14,0.1,True)
            self.widgetTemp.placeOrHide(self.operational_status_entry, 0.15, 0.1, True)
            self.widgetTemp.placeOrHide(self.control_command_label, 0, 0.17, True)
            self.widgetTemp.placeOrHide(self.control_command_entry, 0.01, 0.2, True)
            self.widgetTemp.placeOrHide(self.actuator_position_label,0.14,0.17,True)
            self.widgetTemp.placeOrHide(self.actuator_position_entry, 0.15, 0.2, True)
            self.widgetTemp.placeOrHide(self.deviation_label, 0.24, 0.34, True)
            self.widgetTemp.placeOrHide(self.deviation_entry, 0.23, 0.37, True)
            self.widgetTemp.placeOrHide(self.position_transmitter_label, 0.22, 0.57, True)
            self.widgetTemp.placeOrHide(self.position_transmitter_entry, 0.23, 0.60, True)
            self.widgetTemp.placeOrHide(self.warning_status_label, 0.005, 0.67, True)
            self.widgetTemp.placeOrHide(self.warning_status_entry,0.01,0.7,True)
            self.widgetTemp.placeOrHide(self.alarm_status_label, 0.15, 0.67, True)
            self.widgetTemp.placeOrHide(self.alarm_status_entry,0.15,0.7,True)
            self.widgetTemp.placeOrHide(self.accumulator_pressure_label, 0.43, 0.67, True)
            self.widgetTemp.placeOrHide(self.accumulator_pressure_entry,0.45,0.7,True)

    def manage_UI(self,*args):

            self.progress_bar,self.progress_label  = self.create_progress_bar(0.5, 0.98)
            self.updateDataBtn = self.widgetTemp.create_button('Update Data', 0.05, 0.93, 10, 1, 10, self.retrieve_data)

            self.current_operational_mode_label, self.current_operational_mode_entry = self.create_label_and_entry(
                "Current Operational Mode", 0, 0.07, 0.01, 0.1, 12, True
            )

            self.operational_status_label, self.operational_status_entry = self.create_label_and_entry(
                "Operational Status", 0.14, 0.07, 0.15, 0.1, 12, True
            )

            self.control_command_label, self.control_command_entry = self.create_label_and_entry(
                "Control Command", 0, 0.17, 0.01, 0.2, 12, True
            )

            self.actuator_position_label, self.actuator_position_entry = self.create_label_and_entry(
                "Actuator Position", 0.14, 0.17, 0.15, 0.2, 12, True
            )

            self.deviation_label, self.deviation_entry = self.create_label_and_entry(
                "Deviation", 0.24, 0.34, 0.23, 0.37, 12, True
            )

            self.position_transmitter_label, self.position_transmitter_entry = self.create_label_and_entry(
                "Position Transmitter", 0.22, 0.57, 0.23, 0.60, 12, True
            )

            self.warning_status_label, self.warning_status_entry = self.create_label_and_entry(
                "Warning Status", 0.005, 0.67, 0.01, 0.7, 12, True
            )

            self.alarm_status_label, self.alarm_status_entry = self.create_label_and_entry(
                "Alarm Status", 0.15, 0.67, 0.15, 0.7, 12, True
            )

            self.accumulator_pressure_label, self.accumulator_pressure_entry = self.create_label_and_entry(
                "Accumulator Pressure", 0.43, 0.67, 0.45, 0.7, 12, True
            )

            self.manage_widgets_visibility()

    def create_progress_bar(self, relx, rely):
        progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        progress.place(relx=relx, rely=rely, relwidth=0.8, anchor=tk.CENTER)
        progress_label = tk.Label(self.root, text="")
        progress_label.place(relx=0.5, rely=rely - 0.05, anchor=tk.CENTER)
        return progress, progress_label  # return the created progress bar

    def retrieve_data(self, *args):
        if self.modbus_client.is_connected():
            threading.Thread(target=self.retrieve_data_thread).start()
        else:
            messagebox.showerror("Error", "Modbus connection is not open.")

    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        MAX_REQUESTS_PER_SECOND = 25  # Increase this number to increase the polling rate
        # Retrieve data from the Modbus server
        # Create a rate limiter
        rate_limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=1.0)
        try:
            unit = self.modbus_client.unit
            #print(f"This is unit in ModbusMasterClientWidget.py {unit}")
            count = 571
            raw_values = []  # Initialize raw_values outside the loop
            self.raw_values = raw_values
            self.progress_bar['maximum'] = count
            self.progress_bar['value'] = 0  # Reset the progress bar
            for address in range(0, count):
                with rate_limiter:
                    try:
                        result = self.modbus_client.client.read_holding_registers(address, 1 , unit)
                        if not result.isError():
                            raw_values.append(result.registers[0])
                            self.progress_bar['value'] += 1  # Increment the progress bar
                            self.progress_label['text'] = f"{self.progress_bar['value']}/{count}"  # Update the label text
                            self.root.update_idletasks()  # Update the GUI
                        else:
                            print(f"Error reading register at address {address}: {result}")
                            messagebox.showerror("Error",f"Error reading register at address {address}: {result}")
                            break;
                    except Exception as e:
                        print(f"Exception while reading register at address {address}: {e}")
            # Print the number of elements in raw_values
            print(f"Number of elements in raw_values: {len(raw_values)}")

            #self.refresh_table(raw_values)
        except ValueError:
            print("Invalid unit or count value. Please enter a valid number.")
            messagebox.showerror("Error", "Invalid unit or count value. Please enter a valid number.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")


