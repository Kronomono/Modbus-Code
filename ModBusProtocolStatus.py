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
    def create_progress_bar(self, relx, rely):
        progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        progress.place(relx=relx, rely=rely, relwidth=0.8, anchor=tk.CENTER)
        progress_label = tk.Label(self.root, text="")
        progress_label.place(relx=0.5, rely=rely - 0.05, anchor=tk.CENTER)
        return progress, progress_label  # return the created progress bar

    def clear_entries(self,raw_values):
        print(f'called on')
        for widget, _, _ in self.widgets_index:
            # Skip label widgets
            if isinstance(widget, tk.Label):
                continue
            widget.config(state='normal')
            widget.delete(0, tk.END)
        self.set_entries(raw_values)

        for widget, _, _ in self.widgets_index:
            # Skip label widgets
            if widget == self.motor_starts_label:
                break
            if isinstance(widget, tk.Label):
                continue
            widget.config(state='readonly')
    def get_system_name(self, index):
        self.index_to_name = {1: "Auto Mode", 2: "Setup Mode",5: "Manual Mode"}
        return self.index_to_name.get(index,'Invalid Value')

    def set_entries(self,raw_values):
        #write what values should be in the registry here
        self.accumulator_pressure_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[12]))

        self.current_operational_mode_entry.insert(0, self.get_system_name(raw_values[13]))

    def retrieve_data(self, *args):

        if self.modbus_client.is_connected():
            threading.Thread(target=self.retrieve_data_thread).start()
            self.root.update()
        else:
            messagebox.showerror("Error", "Modbus connection is not open.")
    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        MAX_REQUESTS_PER_SECOND = 100  # Increase this number to increase the polling rate
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
            self.clear_entries(self.raw_values)  # Clear the entries

        except ValueError:
            print("Invalid unit or count value. Please enter a valid number.")
            messagebox.showerror("Error", "Invalid unit or count value. Please enter a valid number.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")

    def manage_widgets_visibility(self, *args):
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        selected_protocol = self.ModBusProtocolConnection.protocol_type_var.get()
        self.widgets_index = [(self.current_operational_mode_label, 0, 0.07),
                              (self.current_operational_mode_entry, 0.01, 0.1),
                              (self.operational_status_label, 0.14, 0.07),
                              (self.operational_status_entry, 0.15, 0.1),
                              (self.control_command_label, 0.0, 0.17),
                              (self.control_command_entry, 0.01, 0.2),
                              (self.actuator_position_label, 0.14, 0.17),
                              (self.actuator_position_entry, 0.15, 0.2),
                              (self.deviation_label, 0.24, 0.34),
                              (self.deviation_entry, 0.23, 0.37),
                              (self.position_transmitter_label, 0.22, 0.57),
                              (self.position_transmitter_entry, 0.23, 0.60),
                              (self.warning_status_label, 0.005, 0.67),
                              (self.warning_status_entry, 0.01, 0.7),
                              (self.alarm_status_label, 0.15, 0.67),
                              (self.alarm_status_entry, 0.15, 0.7),
                              (self.accumulator_pressure_label, 0.43, 0.67),
                              (self.accumulator_pressure_entry, 0.45, 0.7),
                              (self.main_feedback_label, 0.28, 0.2),
                              (self.main_feedback_entry, 0.25, 0.2),
                              (self.redundant_feedback_label, 0.28, 0.23),
                              (self.redundant_feedback_entry, 0.25, 0.23),

                              (self.motor_starts_label, 0.155, 0.81),
                              (self.motor_starts_entry, 0.15, 0.84),
                              (self.booster_starts_label, 0.25, 0.81),
                              (self.booster_starts_entry, 0.25, 0.84),
                              (self.accumulator_starts_label, 0.335, 0.81),
                              (self.accumulator_starts_entry, 0.35, 0.84),
                              (self.actuator_stokes_label, 0.445, 0.81),
                              (self.actuator_strokes_entry, 0.45, 0.84),
                              (self.total_auto_time_label, 0.545, 0.81),
                              (self.total_auto_time_entry, 0.55, 0.84),
                              (self.three_month_average_position_label, 0.645, 0.78),
                              (self.three_month_average_position_entry, 0.65, 0.84)
                              ]

        if selected_version == 'X3':
            self.progress_label.place(relx=0.5, rely=0.93, anchor=tk.CENTER)
            self.progress_bar.place(relx=0.5, rely=0.98, relwidth=0.8, anchor=tk.CENTER)
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.05, 0.93, False)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)

        else:
            self.progress_bar.place_forget()
            self.progress_label.place_forget()
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.05, 0.93, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):

        self.progress_bar, self.progress_label = self.create_progress_bar(0.5, 0.98)
        self.updateDataBtn = self.widgetTemp.create_button('Update Data', 0.05, 0.93, 10, 1, 10, self.retrieve_data)
        self.reset_current_odometer_btn = self.widgetTemp.create_button('Reset Current Odometer', 0.8, 0.8, 10, 2, 20, self.handle_submit)

        self.current_operational_mode_label, self.current_operational_mode_entry = self.widgetTemp.create_label_and_entry(
            "Current Operational Mode", 0, 0.07, 0.01, 0.1, 12, True, preFilledText=None
        )

        self.operational_status_label, self.operational_status_entry = self.widgetTemp.create_label_and_entry(
            "Operational Status", 0.14, 0.07, 0.15, 0.1, 12, True, preFilledText=None
        )

        self.control_command_label, self.control_command_entry = self.widgetTemp.create_label_and_entry(
            "Control Command", 0, 0.17, 0.01, 0.2, 12, True, preFilledText=None
        )

        self.actuator_position_label, self.actuator_position_entry = self.widgetTemp.create_label_and_entry(
            "Actuator Position", 0.14, 0.17, 0.15, 0.2, 12, True, preFilledText=None
        )

        self.deviation_label, self.deviation_entry = self.widgetTemp.create_label_and_entry(
            self.names.get_name(5), 0.24, 0.34, 0.23, 0.37, 12, True, preFilledText=None
        )

        self.position_transmitter_label, self.position_transmitter_entry = self.widgetTemp.create_label_and_entry(
            "Position Transmitter", 0.22, 0.57, 0.23, 0.60, 12, True, preFilledText=None
        )

        self.warning_status_label, self.warning_status_entry = self.widgetTemp.create_label_and_entry(
            "Warning Status", 0.005, 0.67, 0.01, 0.7, 12, True, preFilledText=None
        )

        self.alarm_status_label, self.alarm_status_entry = self.widgetTemp.create_label_and_entry(
            "Alarm Status", 0.15, 0.67, 0.15, 0.7, 12, True, preFilledText=None
        )

        self.accumulator_pressure_label, self.accumulator_pressure_entry = self.widgetTemp.create_label_and_entry(
            "Accumulator Pressure", 0.43, 0.67, 0.45, 0.7, 12, True, preFilledText=None
        )
        self.main_feedback_label, self.main_feedback_entry = self.widgetTemp.create_label_and_entry(
            "Main Feedback", 0.28, 0.2, 0.25, 0.2, 5, True, preFilledText=None
        )
        self.redundant_feedback_label, self.redundant_feedback_entry = self.widgetTemp.create_label_and_entry(
            "Redundant Feedback", 0.28, 0.23, 0.25, 0.23, 5, True, preFilledText=None
        )
        self.motor_starts_label, self.motor_starts_entry = self.widgetTemp.create_label_and_entry(
            "Motor Starts", 0.155, 0.81, 0.15, 0.84, 12, False, preFilledText=None
        )
        self.booster_starts_label, self.booster_starts_entry = self.widgetTemp.create_label_and_entry(
            "Booster Starts", 0.25, 0.81, 0.25, 0.84, 12, False, preFilledText=None
        )
        self.accumulator_starts_label, self.accumulator_starts_entry = self.widgetTemp.create_label_and_entry(
            "Accumulator Starts", 0.335, 0.81, 0.35, 0.84, 12, False, preFilledText=None
        )
        self.actuator_stokes_label, self.actuator_strokes_entry = self.widgetTemp.create_label_and_entry(
            "Actuator Stokes", 0.445, 0.81, 0.45, 0.84, 12, False, preFilledText=None
        )
        self.total_auto_time_label, self.total_auto_time_entry = self.widgetTemp.create_label_and_entry(
            "Total Auto Time", 0.545, 0.81, 0.55, 0.84, 12, False, preFilledText=None
        )
        self.three_month_average_position_label, self.three_month_average_position_entry = self.widgetTemp.create_label_and_entry(
            "3 Month Average \n Position", 0.645, 0.78, 0.65, 0.84, 12, False, preFilledText=None
        )

        self.manage_widgets_visibility()

    def handle_submit(self):
        # Get the input value, selected type, and selected register, and write the value to the register
        # input_value = self.entry.get()
        writables = [self.motor_starts_entry,self.booster_starts_entry,self.accumulator_starts_entry,self.actuator_strokes_entry,self.total_auto_time_entry,self.three_month_average_position_entry]
        for writing in writables:
            writing.delete(0,tk.END)
            writing.insert(0,0)

        motor_starts_value = self.motor_starts_entry.get()
        booster_starts_value = self.booster_starts_entry.get()
        accumulator_starts_value = self.accumulator_starts_entry.get()
        actuator_strokes_value = self.actuator_strokes_entry.get()
        total_auto_time_value = self.total_auto_time_entry.get()
        three_month_average_position_value = self.three_month_average_position_entry.get()

        #address_value = self.available_registers[self.selected_register.get()]
        print(f"motor_starts_value: {motor_starts_value}\n"
              f"booster_starts_value:{booster_starts_value}\n"
              f"accumulator_starts_value:{accumulator_starts_value}\n"
              f"actuator_strokes_value:{actuator_strokes_value}\n"
              f"total_auto_time_value:{total_auto_time_value}\n"
              f"three_month_average_position_value:{three_month_average_position_value}")
        # print(f"Submitted value: {input_value}")
        # print(f"Selected type: {self.selected_type.get()}")
        # print(f"Address value: {address_value}")

    '''
                try:
                    if input_value.isdigit():
                        self.modbus_client.write_register(address_value, input_value)
                    else:
                        raise ValueError("Invalid selection")

                except ValueError:
                    messagebox.showerror("Error", "Invalid input value. Please try again.")'''



