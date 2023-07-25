#ModBusProtocolCalibration.py
import tkinter as tk
from Names import Names
from WidgetTemplateCreator import  WidgetTemplateCreator



class ModBusProtocolCalibration:
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
        # Create the widgets/ gui elements
        self.widgetTemp.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.ModBusProtocolConnection.protocol_type_var.trace('w', self.manage_widgets_visibility)
        self.ModBusProtocolConnection.rexa_version_type_var.trace('w', self.manage_widgets_visibility)

        # call manage UI function
        self.manage_UI()

    def manage_widgets_visibility(self, *args):
        # get variable from connection tab
        selected_version = self.ModBusProtocolConnection.rexa_version_type_var.get()
        # create index list of widgets
        self.widgets_index = []

        # take lable index and entry index and combine them
        for var_name, index in self.label_index + self.entry_index:
            if len(index) == 3:
                self.widgets_index.append((getattr(self, var_name), index[1], index[2]))
            elif len(index) == 2:
                self.widgets_index.append((getattr(self, var_name), index[0], index[1]))

        # if X3 option selected in connection tab show stuff
        if selected_version == 'X3':
            # show if x3 is selected on drop down menu
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, False)
        else:
            # hide if it is not chosen
            for widget in self.widgets_index:
                self.widgetTemp.placeOrHide(*widget, True)

    def manage_UI(self, *args):
        # entry index with var name, and coordinates
        self.entry_index =[("current_operational_mode_entry",(0.01,0.1,)),
                        ("operational_status_entry",(0.15,0.1)),
                        ("primary_feedback_position_low_entry",(0.05,0.3)),
                        ("redundant_feedback_position_low_entry",(0.35,0.3)),
                        ("primary_feedback_position_high_entry",(0.05,0.4)),
                        ("redundant_feedback_position_high_entry",(0.35,0.4)),
                        ("driven_device_mechanical_travel_entry",(0.19,0.48)),
                        ("signal_low_entry",(0.05,0.77)),
                        ("signal_high_entry",(0.2,0.77)),
                        ("current_cs_input_entry",(0.125, 0.85)),
                        ("primary_entry",(0.4, 0.75)),
                        ("redundant_entry",(0.4, 0.78,)),
                        ("transmitter_low_entry",(0.73, 0.85)),
                        ("transmitter_high_entry",(0.84, 0.85)),
                           ("position_transmitter_entry", (0.785, 0.75))
                        ]
        # for loop to create entries
        for var_name, index in self.entry_index:

            entry = self.widgetTemp.create_entry(*index, 13, True, preFilledText=None)
            setattr(self, var_name, entry)

        # label index with var name, display text, coordinates
        self.label_index=[("analog_input_label",("Analog input",0.03,0.7)),
                       ("feedback_values_label",("Feedback Values",0.35,0.7)),
                       ("primary_feedback_label",("Primary Feedback",0.04,0.23)),
                       ("redundant_feedback_label",("Redundant Feedback",0.33,0.23)),
                       ("stroke_limits_label",("Stroke Limits",0.03,0.18)),
                       ("using_primary_feedback_label",("Using Primary Feedback",0.35,0.84)),
                       ("factory_calibration_label",("Factory Calibration",0.77,0.79)),
                       ("mA1_label",("mA",0.12,0.77)),
                       ("mA2_label",("mA",0.27,0.77)),
                       ("mA3_label",("mA",0.2,0.85)),
                       ("current_operational_mode_label",("Current Operational Mode",0,0.07)),
                       ("operational_status_label",("Operational Status",0.14,0.07)),
                       ("primary_feedback_position_low_label",("Position Low",0.05,0.27)),
                       ("redundant_feedback_position_low_label",("Position Low",0.35,0.27)),
                       ("primary_feedback_position_high_label",("Position High",0.05,0.37)),
                       ("redundant_feedback_position_high_label",("Position High",0.35,0.37)),
                       ("driven_device_mechanical_travel_label",("Driven Device Mechanical Travel",0.02,0.48)),
                       ("signal_low_label",("Signal Low", 0.05,0.74)),
                       ("signal_high_label",("Signal High",0.2,0.74)),
                       ("current_cs_input_label",("Current CS Input", 0.115, 0.82)),
                       ("primary_label",("Primary",0.35,0.75)),
                       ("redundant_label",("Redundant",0.34,0.78)),
                       ("transmitter_low_label",("Transmitter Low",0.72,0.82)),
                       ("transmitter_high_label",("Transmitter High",0.83,0.82)),
                    ("position_transmitter_label", ("Position Transmitter", 0.77, 0.72))
                          ]
        # for loop for labels
        for  var_name, index in self.label_index:
            label = self.widgetTemp.create_label(*index)
            setattr(self,var_name,label)

    # clear entries
    def clear_entries(self,raw_values):
        # clear all the entries
        for var_name, _ in self.entry_index:
            # Get the corresponding entry widget
            entry = getattr(self, var_name)
            # Make the entry widget writable
            entry.config(state='normal')
            # Clear the existing text in the entry widget
            entry.delete(0, 'end')

        # call set_entries function
        self.set_entries(raw_values)

        #set all entries back to read only
        for var_name, _ in self.entry_index:
            entry = getattr(self, var_name)
            entry.config(state='readonly')

    def set_entries(self, raw_values):
        #sets all the entries and map them out
        self.current_operational_mode_entry.insert(0, self.names.get_system_name(raw_values[13]))
        self.operational_status_entry.insert(0, self.modbus_client.translate_value(self.names.get_status_name(raw_values[15])))

        self.transmitter_low_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[161]))
        self.transmitter_high_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[162]))
        self.primary_entry.insert(0, self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[428]))
        self.redundant_entry.insert(0,self.modbus_client.translate_value("Unsigned Int 16 bit", raw_values[429]))

        self.signal_low_entry.insert(0,round(self.modbus_client.translate_value("Float 32 bit", raw_values[125], raw_values[126]),3))
        self.signal_high_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[127], raw_values[128]), 3))

        self.primary_feedback_position_low_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[117], raw_values[118]), 3))
        self.primary_feedback_position_high_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[119], raw_values[120]), 3))
        self.redundant_feedback_position_low_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[121], raw_values[122]), 3))
        self.redundant_feedback_position_high_entry.insert(0, round(self.modbus_client.translate_value("Float 32 bit", raw_values[123], raw_values[124]), 3))

        self.control_command_entry_value = round(self.modbus_client.translate_value("Float 32 bit", raw_values[0], raw_values[1]), 3)
        self.actuator_position = round(self.modbus_client.translate_value("Float 32 bit", raw_values[2], raw_values[3]), 3)

        #get the variables from status tab and use it for math here
        #CurrentCsInput Math
        #control_command_entry_value = float(control_command_entry_value)
        self.current_cs_input = 0.16 * self.control_command_entry_value + 4


        self.current_cs_input_entry.insert(0,self.current_cs_input)

        #Position_transmitter math
        #self.actuator_position = float(actuator_position_entry_value)
        self.position_transmitter = 635 * self.actuator_position + 500

        self.position_transmitter_entry.insert(0, self.position_transmitter)