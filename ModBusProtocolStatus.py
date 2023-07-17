#ModBusProtocolStatus.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator



class ModBusProtocolStatus:
    def __init__(self, root, modbus_client,modbus_protocol_connection,modbus_protocol_calibration,modbus_protocol_configuration, modbus_protocol_pst,modbus_protocol_diagnostics):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.names = Names()
        self.ModBusProtocolConnection = modbus_protocol_connection
        self.widgetTemp = WidgetTemplateCreator(self.root)
        self.ModBusProtocolCalibration = modbus_protocol_calibration
        self.ModBusProtocolConfiguration = modbus_protocol_configuration
        self.ModBusProtocolPST = modbus_protocol_pst
        self.ModBusProtocolDiagnostics = modbus_protocol_diagnostics

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.raw_values = {}


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

        self.main_feedback_entry.config(state='normal')

        self.main_feedback_entry.delete(0,tk.END)

        self.redundant_feedback_entry.config(state='normal')

        self.redundant_feedback_entry.delete(0,tk.END)



        for widget, _, _ in self.widgets_index:
            # Skip label widgets
            if isinstance(widget, tk.Label):
                continue
            widget.config(state='normal')
            widget.delete(0, tk.END)

        self.set_entries(raw_values)

        for widget, _, _ in self.widgets_index:
            # Skip label widgets
            if widget == self.motor_starts_entry:
                break
            if isinstance(widget, tk.Label):
                continue
            widget.config(state='readonly')
            self.main_feedback_entry.config(state='readonly')
            self.redundant_feedback_entry.config(state='readonly')

    def process_segment(self,range_start, range_end, entry,raw_values):
        character = ""
        entry.configure(state="normal")
        for i in range(range_start, range_end):
            segment = self.modbus_client.translate_value("ASCII 16 bit", raw_values[i])
            if segment == "unknown":
                character += str(raw_values[i])
            else:
                character += segment
        entry.insert(0, character)
        entry.configure(state="readonly")

    def set_entries(self,raw_values):
        self.process_segment(205, 230, self.ModBusProtocolConnection.model_entry,raw_values)
        self.process_segment(230, 262, self.ModBusProtocolConnection.tag_entry,raw_values)
        self.process_segment(262, 276, self.ModBusProtocolConnection.serial_entry,raw_values)
        self.process_segment(276, 290, self.ModBusProtocolConnection.software_version_entry,raw_values)
        self.process_segment(290, 304, self.ModBusProtocolConnection.display_version_entry,raw_values)


        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))

        self.operational_status_entry.insert(0,self.modbus_client.translate_value("Byte",raw_values[15]))
        self.main_feedback_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[16]))
        self.redundant_feedback_entry.insert(0, self.modbus_client.translate_value("Byte", raw_values[16]))

        self.accumulator_pressure_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[12]))

        self.motor_starts_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 32 bit",raw_values[562],raw_values[563]))
        self.actuator_strokes_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 32 bit",raw_values[558],raw_values[559]))

        self.control_command_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[0], raw_values[1]), 3))
        self.actuator_position_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[2], raw_values[3]), 3))
        self.three_month_average_position_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[25], raw_values[26]),3))
        self.deviation_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[4], raw_values[5]),3))



        self.ModBusProtocolCalibration.clear_entries(self.raw_values,self.control_command_entry.get(),self.actuator_position_entry.get())
        self.ModBusProtocolConfiguration.clear_entries(self.raw_values)
        self.ModBusProtocolDiagnostics.clear_entries(self.raw_values)
        self.ModBusProtocolPST.clear_entries(self.raw_values)

        #Position_transmitter math
        self.actuator_position = float(self.actuator_position_entry.get())
        self.position_transmitter = 635*self.actuator_position+500

        self.position_transmitter_entry.insert(0, self.position_transmitter)

    def retrieve_data(self, *args):
        if self.modbus_client.is_connected():
            self.retrieve_data_thread()  # Call the function immediately
            self.root.after(1500, self.retrieve_data)

        else:
            messagebox.showerror("Error", "Modbus connection is not open.")


    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        #call every 1.2 seconds
        MAX_REQUESTS_PER_SECOND = 100  # Increase this number to increase the polling rate
        # Retrieve data from the Modbus server
        # Create a rate limiter
        rate_limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=0.2)
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
        self.widgets_index = []

        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))

        if selected_version == 'X3':
            self.progress_label.place(relx=0.5, rely=0.93, anchor=tk.CENTER)
            self.progress_bar.place(relx=0.5, rely=0.98, relwidth=0.8, anchor=tk.CENTER)
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.0, 0.96, False)
            self.widgetTemp.placeOrHide(self.main_feedback_entry,0.25,0.2,False)
            self.widgetTemp.placeOrHide(self.redundant_feedback_entry, 0.25, 0.23, False)
            self.widgetTemp.placeOrHide(self.reset_current_odometer_btn,0.8,0.8,False)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)

        else:
            self.progress_bar.place_forget()
            self.progress_label.place_forget()
            self.widgetTemp.placeOrHide(self.updateDataBtn, 0.0, 0.96, True)
            self.widgetTemp.placeOrHide(self.main_feedback_entry, 0.25, 0.2, True)
            self.widgetTemp.placeOrHide(self.redundant_feedback_entry, 0.25, 0.23, True)
            self.widgetTemp.placeOrHide(self.reset_current_odometer_btn, 0.8, 0.8, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        self.label_index = [("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                             ("operational_status_label",("Operational Status",0.14,0.07)),
                             ("control_command_label",("Control Command",0,0.17)),
                             ("actuator_position_label",("Actuator Position",0.14,0.17)),
                             ("deviation_label",(self.names.get_name(5),0.24,0.34)),
                             ("position_transmitter_label",("Position Transmitter",0.22,0.57)),
                             ("warning_status_label",("Warning Status",0.005,0.67)),
                             ("alarm_status_label",("Alarm Status",0.15,0.67)),
                             ("accumulator_pressure_label",("Accumulator Pressure",0.43,0.67)),
                             ("main_feedback_label",("Main Feedback",0.28,0.2)),
                             ("redundant_feedback_label",("Redundant Feedback",0.28,0.23)),
                             ("motor_starts_label",("Motor Starts",0.155, 0.81)),
                             ("booster_starts_label",("Booster Starts",0.25,0.81)),
                             ("accumulator_starts_label",("Accumulator Starts",0.335,0.81)),
                             ("actuator_strokes_label",("Actuator Strokes",0.445,0.81)),
                             ("total_auto_time_label",("Total Auto Time",0.545,0.81)),
                             ("three_month_average_position_label",("3 Month Average \n Position", 0.645, 0.78))
        ]
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

        self.entry_index =[("current_operational_mode_entry",(0.01,0.1)),
                           ("operational_status_entry",(0.15,0.1)),
                           ("control_command_entry",(0.01,0.2)),
                           ("actuator_position_entry",(0.15,0.2)),
                           ("deviation_entry",(0.23,0.37)),
                           ("position_transmitter_entry",(0.23,0.6)),
                           ("warning_status_entry",(0.01,0.7)),
                           ("alarm_status_entry",(0.15,0.7)),
                           ("accumulator_pressure_entry",(0.45,0.7)),
                           ("motor_starts_entry",(0.15,0.84)),
                           ("booster_starts_entry",(0.25,0.84)),
                           ("accumulator_starts_entry",(0.35,0.84)),
                           ("actuator_strokes_entry",(0.45,0.84)),
                           ("total_auto_time_entry",(0.55,0.84)),
                           ("three_month_average_position_entry",(0.65,0.84))
        ]
        readOnly = True
        for var_name, index in self.entry_index:
            if var_name == "motor_starts_entry":
                readOnly = False
            entry = self.widgetTemp.create_entry(*index, 13, readOnly, preFilledText=None)
            setattr(self, var_name, entry)
        self.progress_bar, self.progress_label = self.create_progress_bar(0.5, 0.98)
        self.updateDataBtn = self.widgetTemp.create_button('Update Data', 0.0, 0.96, 10, 1, 12, self.retrieve_data)

        self.reset_current_odometer_btn = self.widgetTemp.create_button('Reset Current Odometer', 0.8, 0.8, 10, 2, 20, self.reset_current_odometer)
        self.main_feedback_entry = self.widgetTemp.create_entry(0.25,0.2,5,True,preFilledText=None)
        self.redundant_feedback_entry = self.widgetTemp.create_entry(0.25, 0.23, 5, True, preFilledText=None)
        self.manage_widgets_visibility()

    def reset_current_odometer(self):
        # Get the input value, selected type, and selected register, and write the value to the register
        # input_value = self.entry.get()
        if self.raw_values:
            writables = [self.motor_starts_entry,self.booster_starts_entry,self.accumulator_starts_entry,self.actuator_strokes_entry,self.total_auto_time_entry,self.three_month_average_position_entry]
            for writing in writables:
                writing.delete(0,tk.END)
                writing.insert(0,0)
        else:
            messagebox.showerror("Error","data not collected")

        motor_starts_value = self.motor_starts_entry.get()
        booster_starts_value = self.booster_starts_entry.get()
        accumulator_starts_value = self.accumulator_starts_entry.get()
        actuator_strokes_value = self.actuator_strokes_entry.get()
        total_auto_time_value = self.total_auto_time_entry.get()

        three_month_average_position_value = self.three_month_average_position_entry.get()
        print(f"motor_starts_value: {motor_starts_value}\n"
              f"booster_starts_value:{booster_starts_value}\n"
              f"accumulator_starts_value:{accumulator_starts_value}\n"
              f"actuator_strokes_value:{actuator_strokes_value}\n"
              f"total_auto_time_value:{total_auto_time_value}\n"
              f"three_month_average_position_value:{three_month_average_position_value}")
    '''self.modbus_client.write_register(address_value, input_value)'''





