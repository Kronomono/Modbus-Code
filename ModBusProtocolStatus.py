#ModBusProtocolStatus.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator

class ModBusProtocolStatus:
    def __init__(self, root, modbus_client,modbus_protocol_connection,modbus_protocol_calibration,modbus_protocol_configuration, modbus_protocol_pst,modbus_protocol_diagnostics,current_tab):
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

        self.current_tab = current_tab

        self.retrieve_data()

        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        #fill raw values with 571 0s. Change if registers increase or decrease
        self.raw_values = [0]*571

    def create_widgets(self):
        # Create the GUI widgets for the Modbus Protocol Status tab
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)
        self.manage_UI()

 #clears the entries for Status tab
    def clear_entries(self,raw_values):
        #manually clear entry because not in entry index since have customized sizes instead of default ones
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
        #call set_entries functions which maps out the entries with correct translated register
        self.set_entries(raw_values)
        #set every entry back to read only except the reset odometer entries
        for widget, _, _ in self.widgets_index:
            # Skip label widgets
            if widget == self.motor_starts_entry:
                break
            if isinstance(widget, tk.Label):
                continue
            widget.config(state='readonly')
        self.main_feedback_entry.config(state='readonly')
        self.redundant_feedback_entry.config(state='readonly')

    def connection_clear_entries(self,raw_values):
        #clear entries for connection tab
        self.ModBusProtocolConnection.serial_entry.config(state='normal')
        self.ModBusProtocolConnection.serial_entry.delete(0, tk.END)
        self.ModBusProtocolConnection.tag_entry.config(state='normal')
        self.ModBusProtocolConnection.tag_entry.delete(0, tk.END)
        self.ModBusProtocolConnection.model_entry.config(state='normal')
        self.ModBusProtocolConnection.model_entry.delete(0, tk.END)
        self.ModBusProtocolConnection.software_version_entry.config(state='normal')
        self.ModBusProtocolConnection.software_version_entry.delete(0, tk.END)
        self.ModBusProtocolConnection.display_version_entry.config(state='normal')
        self.ModBusProtocolConnection.display_version_entry.delete(0, tk.END)
        #calls function to set entries for connection tab
        self.connection_set_entries(raw_values)

        #sets them back to read only
        self.ModBusProtocolConnection.serial_entry.config(state='readonly')
        self.ModBusProtocolConnection.tag_entry.config(state='readonly')
        self.ModBusProtocolConnection.model_entry.config(state='readonly')
        self.ModBusProtocolConnection.software_version_entry.config(state='readonly')
        self.ModBusProtocolConnection.display_version_entry.config(state='readonly')
    def connection_set_entries(self,raw_values):
        # Set the entries on the Modbus Protocol Connection tab
        self.process_segment(205, 230, self.ModBusProtocolConnection.model_entry, raw_values)
        self.process_segment(230, 262, self.ModBusProtocolConnection.tag_entry, raw_values)
        self.process_segment(262, 276, self.ModBusProtocolConnection.serial_entry, raw_values)
        self.process_segment(276, 290, self.ModBusProtocolConnection.software_version_entry, raw_values)
        self.process_segment(290, 304, self.ModBusProtocolConnection.display_version_entry, raw_values)

    def process_segment(self,range_start, range_end, entry,raw_values):
        # Process a segment of values and update the given entry
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
        # Set the entries on the Modbus Protocol Status tab
        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))
        self.operational_status_entry.insert(0,self.modbus_client.translate_value(self.names.get_status_name(raw_values[15])))




        self.alarm_status_entry.insert(0,self.modbus_client.translate_value("Epoch 64 Bit",raw_values[21],raw_values[22],raw_values[23],raw_values[24]))

        self.warning_status_entry.insert(0, self.modbus_client.translate_value("Epoch 64 Bit", raw_values[17],raw_values[18],raw_values[19],raw_values[20]))




        self.accumulator_pressure_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit",raw_values[12]))

        self.motor_starts_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 32 bit",raw_values[562],raw_values[563]))
        self.actuator_strokes_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 32 bit",raw_values[558],raw_values[559]))

        self.control_command_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[0], raw_values[1]), 3))
        self.actuator_position_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[2], raw_values[3]), 3))

        self.three_month_average_position_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[25], raw_values[26]),3))
        self.deviation_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[4], raw_values[5]),3))


        self.main_feedback = self.modbus_client.translate_value("Byte", raw_values[16])

        self.redundant_feedback =  self.modbus_client.translate_value("Byte", raw_values[16])

        if self.main_feedback == 0:
            self.main_feedback_entry.config(bg="green")
        else:
            self.main_feedback_entry.config(bg="red")

        if  self.redundant_feedback == 1:
            self.redundant_feedback_entry.config(bg="green")
        else:
            self.redundant_feedback_entry.config(bg="red")


        #Position_transmitter math
        self.actuator_position = float(self.actuator_position_entry.get())
        self.position_transmitter = 635*self.actuator_position+500
        self.position_transmitter_entry.insert(0, self.position_transmitter)


    def retrieve_data(self, *args):
        # Retrieve data from the Modbus server
        if self.modbus_client.is_connected():
            threading.Thread(target=self.retrieve_data_thread, daemon=True).start()
        else:
            print(f"connection failed. Trying again in 2 seconds")
            threading.Timer(2, self.retrieve_data).start()
    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        print(f"Current tab: ", self.current_tab)
        MAX_REQUESTS_PER_SECOND = 100  # Increase this number to increase the polling rate
        rate_limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=0.2) # change period variable to change amount of time between each request
        try:
            # gets whatever unit it is assign
            unit = self.modbus_client.unit
            # Define the Modbus registers to read based on the current tab
            tab_registers = {
                "Connection": list(range(205, 230)) + list(range(230, 262)) + list(range(262, 276)) + list(range(276, 290)) + list(range(290, 304)),
                "Status": [0, 1, 2, 3, 4, 5, 12, 13, 15, 16, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 558, 559, 562, 563], #list(range(0,27)) + list(range(558,564)),
                "PST":[11, 13, 15, 149, 150, 153, 154, 155, 156, 157, 158, 159, 160, 172, 173, 201, 202, 203, 204],   #[11,13,15] + list(range(159,205)),
                "Diagnostics":[13,15,163,164,171,170,14,
                               #numbers for fault
                               328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,
                               359,360,361,362,363,364,365,366,367,
                               #numbers for mode time stamp
                               378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,
                               409,410,411,412,413,414,415,416,417,
                               #numbers for current
                               418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435,
                               436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453,
                               454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471,
                               472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487,
                               # numbers for historic
                               488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505,
                               506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523,
                               524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541,
                               542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 556, 557, 558
                                ],
                #[13,14,15] + list(range(163,172)) + list(range(319,559)),#list(range(329,368)) + list(range(379,418))+list(range(419,559)),
                "Calibration": [0, 1, 2, 3, 13, 15, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 161, 162, 428, 429],#[0, 1, 2, 3, 428, 429] + list(range(117,163)),
                "Configuration": [0, 1, 13, 15, 129, 130, 131, 132, 133, 134, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 165, 166, 167, 168, 169,
                                  174, 178, 179, 182, 183, 184, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 197, 558, 559, 562, 563],#list(range(0,205))+ list(range(500,571)),


            }
            # match to get whatever tab the user is on and see what registers it needs to get
            registers = tab_registers[self.current_tab]

            #for loop with 0.2 delay
            for address in registers:
                with rate_limiter:
                    try:
                        #read register with address, and unit
                        result = self.modbus_client.client.read_holding_registers(address, 1 , unit)
                        if not result.isError():
                            self.raw_values[address] = result.registers[0]
                            self.root.update_idletasks()  # Update the GUI
                        # error / exception handling
                        else:
                            print(f"Error reading register at address {address}: {result}")
                            messagebox.showerror("Error",f"Error reading register at address {address}: {result}")
                            break;
                    except Exception as e:
                        print(f"Exception while reading register at address {address}: {e}")
            # if statements for each tab to clear and set entries
            if self.current_tab == "Connection":
                self.connection_clear_entries(self.raw_values)
            elif self.current_tab == "Status":
                self.clear_entries(self.raw_values)  # Clear the entries
            elif self.current_tab == "PST":
                self.ModBusProtocolPST.clear_entries(self.raw_values)
            elif self.current_tab == "Diagnostics":
                self.ModBusProtocolDiagnostics.clear_entries(self.raw_values)
                if self.ModBusProtocolDiagnostics.called == False:
                   #setting a flag so data in table is only imported once
                    self.ModBusProtocolDiagnostics.set_table(self.raw_values)
                    self.ModBusProtocolDiagnostics.called = True

            elif self.current_tab == "Calibration":

                self.ModBusProtocolCalibration.clear_entries(self.raw_values)
            elif self.current_tab == "Configuration":
                self.ModBusProtocolConfiguration.clear_entries(self.raw_values)
        # more error / exception handling
        except ValueError:
            print("Invalid unit or count value. Please enter a valid number.")
            messagebox.showerror("Error", "Invalid unit or count value. Please enter a valid number.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")
        # call itself again every 1.5 seconds and update the entries
        #print(f"list ", self.raw_values)
        threading.Timer(1.5, self.retrieve_data).start()

    # get variable from main and updates whatever tab user is on
    def update_current_tab(self, new_tab):
        self.current_tab = new_tab

    def manage_widgets_visibility(self, *args):
        # Manage the visibility of widgets based on the selected protocol and Rexa version
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()


        self.widgets_index = []

        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))

        if selected_version == 'X3':

            self.widgetTemp.placeOrHide(self.main_feedback_entry,0.25,0.2,False)
            self.widgetTemp.placeOrHide(self.redundant_feedback_entry, 0.25, 0.23, False)
            self.widgetTemp.placeOrHide(self.reset_current_odometer_btn,0.8,0.8,False)

            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)

        else:


            self.widgetTemp.placeOrHide(self.main_feedback_entry, 0.25, 0.2, True)
            self.widgetTemp.placeOrHide(self.redundant_feedback_entry, 0.25, 0.23, True)
            self.widgetTemp.placeOrHide(self.reset_current_odometer_btn, 0.8, 0.8, True)
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        #creates label variable name and there coordinates
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
        # loops through index to create labels
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)
        # index of entry names and their coordinates
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
        ] #make all of them read only except the reset current odometer entries
        readOnly = True
        # for loop to create entries
        for var_name, index in self.entry_index:
            if var_name == "motor_starts_entry":
                readOnly = False
            entry = self.widgetTemp.create_entry(*index, 13, readOnly, preFilledText=None)
            setattr(self, var_name, entry)

        # create reset_current_odometer button and custom sized entries
        self.reset_current_odometer_btn = self.widgetTemp.create_button('Reset Current Odometer', 0.8, 0.8, 10, 2, 20, self.reset_current_odometer)
        self.main_feedback_entry = self.widgetTemp.create_entry(0.25,0.2,5,True,preFilledText=None)
        self.redundant_feedback_entry = self.widgetTemp.create_entry(0.25, 0.23, 5, True, preFilledText=None)
        self.manage_widgets_visibility()

    def reset_current_odometer(self):
        # if self.raw_values is created then iterates through each entry and puts in a 0
        if self.raw_values:
            writables = [self.motor_starts_entry,self.booster_starts_entry,self.accumulator_starts_entry,self.actuator_strokes_entry,self.total_auto_time_entry,self.three_month_average_position_entry]
            for writing in writables:
                writing.delete(0,tk.END)
                writing.insert(0,0)
        else:
            messagebox.showerror("Error","data not collected")
        # gets whatever value is in each entry and prints it out in console
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

        #how to write registers
    '''self.modbus_client.write_register(address_value, input_value)'''




