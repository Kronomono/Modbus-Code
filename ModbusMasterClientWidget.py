#ModbusMasterClientWidget.py
import tkinter as tk
from tkinter import messagebox, ttk
from ModbusClient import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
import struct
from pymodbus.constants import Endian
import unicodedata
import time
from ratelimiter import RateLimiter
import threading


class ModbusMasterClientWidget:
    def __init__(self, root, modbus_client):
        # Initialize the widget with a root window and a Modbus client
        self.root = root
        self.modbus_client = modbus_client
        self.connection_button = None
        self.retrieve_button = None


        # Create a frame to hold the table and the scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the table
        self.table = ttk.Treeview(self.root, columns=("Name","Address", "Type", "Registry"), show='headings')
        self.table.heading("Address", text="Address")
        self.table.heading("Type", text="Type")
        self.table.heading("Registry", text="Registry")
        self.table.heading("Name", text="Name")
        self.table.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the scrollbar to the table
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.table.yview)

        # Create the data type dropdown
        self.data_type_var = tk.StringVar(self.root)
        self.data_type_options = ['holding', 'Float 32 bit', 'ASCII 16 bit', 'Epoch 32 bit', 'Binary',
                                  'Signed Int 16 bit', 'Unsigned Int 16 bit', 'Boolean', 'Byte', 'Signed Int 32 bit',
                                  'Unsigned Int 32 bit', 'ALL']

        self.data_type_var.set(self.data_type_options[0])
        self.data_type_dropdown = tk.OptionMenu(self.root, self.data_type_var, *self.data_type_options)
        self.data_type_dropdown.place(relx=0.17, rely=0.075, anchor=tk.NW)
        # Add a trace to the data_type_var
        self.data_type_var.trace('w', self.refresh_table)


        self.unit_entry = self.create_unit_entry()  # Store the unit_entry widget
        self.count_entry = self.create_count_entry()
        self.progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        self.progress.place(relx=0.5, rely=0.2, relwidth=0.8, anchor=tk.CENTER)
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)


    def create_widgets(self):
        # Create the Connect, Retrieve Data, and Show Graph buttons
        self.create_connection_button()
        self.create_retrieve_button()

    def create_connection_button(self):
        # Create the Connect button and place it in the window
        self.connection_button = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connection_button.place(relx=0.05, rely=0.05, anchor=tk.NW)

    def create_unit_entry(self):
        # Create a unit entry field and place it in the window
        unit_entry = tk.Entry(self.root, width=10)
        unit_entry_label = tk.Label(self.root, text="Enter unit #")
        unit_entry_label.place(relx=0.38, rely=0.03, anchor=tk.CENTER)
        unit_entry.place(relx=0.35, rely=0.05, anchor=tk.NW)
        return unit_entry
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

            def connect():
                # Retrieve the host and port from the dialog
                host = host_entry.get()
                port = port_entry.get()

                print(f"Retrieved host from dialog: {host}")
                print(f"Retrieved port from dialog: {port}")

                if host and port:
                    # Check if the port enter is an int
                    if port.isdigit():
                        self.modbus_client.update_host_port(host, int(port))
                        if self.modbus_client.connect():
                            self.connection_button["text"] = "Disconnect"
                            messagebox.showinfo("Connected", "Connection successful")
                        else:
                            messagebox.showerror("Error", "Failed to establish Modbus connection.")
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid port. Please enter a valid number.")
                else:
                    messagebox.showerror("Error", "Please enter both the host IP address and port.")

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

    def disconnect_modbus(self):
        # Disconnect the Modbus connection and update the Connect button text
        self.modbus_client.close()
        self.connection_button["text"] = "Connect"

    def get_name(self,index):
        self.index_to_name = {
            1: "Control Signal",3:"Position",5:"Deviation",7:"Torque/Thrust",9:"Delta Pressure",10:"Open Pressure",11:"Close Pressure",12:"Pst Status",
            13:"Accumulator Pressure",14:"System Mode",15:"Last Event",16:"System Status",17:"Active Feedback",18:"Active Warnings",22:"Active Alarms",
            26:"Average Position Last 90 Days",28:"Max  Torque/Thrust Per Poll",30:"Min Torque/ Thrust Per Poll",32:"Max CW Torque Last 1hr",
            34:"Min CW Torque Last 1hr",36:"Max CCW Torque Last 1hr",38:"Min CCW Torque Last 1hr",40:"Max CW Torque Last 4hr",42:"Min CW Torque Last 4hr",
            44:"Max CCW Torque Last 4hr",46:"Min CCW Torque Last 4hr",48:"Max CW Torque Last 8hr", 50:"Min CW Torque Last 8hr",52:"Max CCW Torque Last 8hr",
            54:"Min CCW Torque Last 8hr",56:"Max CW Torque Last 12hr",58:"Min Cw Torque Last 12hr",60:"Max CCW Torque Last 12 hr",62:"Min CCW Torque Last 12hr",
            64:"Max CW Torque Last 24 hr",66:"Min CW Torque Last 24hr",68:"Max CCW Torque Last 24hr",70:"Min CCW Torque Last 24hr",72:"Max Deviation Last 1hr",
            74:"Max Deviation Last 4hr",76:"Max Deviation Last 8hr",78:"Max Deviation Last 12hr",80:"Max Deviation Last 24hr",82:"Current Position Sensor Noise",
            83:"Actuator Drift Events Last 1hr",84:"Seating Events Last 1hr",85:"Primary Motor Starts Last 1hr",86:"Strokes Last 1hr",87:"Online Motor Starts Last 1hr",
            88:"Online Recharge Time Last 1hr",89:"Boost Motor Starts Last 1hr",90:"Actuator Drift Events Last 4hrs",91:"Seating Events Last 4hrs",
            92:"Primary Motor Starts Last 4hrs",93:"Strokes Last 4hrs",94:"Online Motor Starts Last 4hrs",95:"Online Recharge Time Last 4hrs",
            96:"Boost Motor Starts Last 4hrs",97:"Actuator Drift Events Last 8 hrs",98:"Seating Events Last 8hrs", 99:"Primary Motor Starts Last 8hrs",
            100:"Stroke Last 8hrs",101:"Online Motor Starts Last 8hrs",102:"Online Recharge Time Last 8hrs",103:"Boost Motor Starts Lst 8 hrs",
            104:"Actuator Drift Events Last 12hrs",105:"Seating Events Last 12hrs",106:"Primary Motor Starts Last 12hrs",107:"Strokes Last 12hrs",
            108:"Online Motor Starts Last 12hrs",109:"Online Recharge TIme Last 12hrs",110:"Boost Motor Starts Last 12hrs",111:"Actuator Drift Events Last 24hrs",
            112:"Seating Events last 24hrs",113:"Primary Motor Starts Last 24hrs",114:"Strokes Last 24hrs",115:"Online Motor Starts Last 24hrs",
            116:"Online Recharge Time Last 24hrs",117:"Boost Motor Starts Last 24hrs",118:"Position Low",120:"Position High",122:"Position Low 2",124:"Position High 2",
            126:"Signal Low",128:"Signal High",130:"Failsafe Position",132:"Min. Mod. Position",134:"Calibrated Stroke",136:"Booster Breakpoint",138:"Deadband",
            140:"Speed Breakpoint",142:"Surge Breakpoint",144:"Surge Offpoint",146:"Relay 1 Setpoint",148:"Relay 2 Setpoint",150:"PST Increment",152:"PST Large Increment",
            154:"PST Signal Deviation",156:"PST Offpoint",158:"PST Target",160:"PST Max Target",162:"Transmitter Low",163:"Transmitter High",164:"Accumulator Recharge Time",
            165:"Accumulator Warning Pressure",166:"Accumulator Recharge Pressure",167:"Gain",168:"Max Down Speed",169:"Max Up Speed",170:"Max Manual Speed",
            171:"Delta Alarm Pressure",172:"Delta Warning Pressure",173:"PST Schedule Time",174:"PST Max RunTime",175:"Trip Mode",176:"Analog CS Enabled",
            177:"One-Contact Enabled",178:"Two-Contact Enabled",179:"Power-up Last Enabled",180:"Power-up Local Enabled",181:"Failsafe Position Enabled",
            182:"Failsafe In-Place Enabled",183:"Bumpless ransfer Enabled",184:"Minimum Modulation Enabled",185:"Solenoid Seating Enabled",
            186:"Contact Board Present",187:"Booster Motor Enabled",188:"Power Fail Accumulator Mode",189:"Power Fail In-Place Mode",190:"Accumulator Direction PL",
            191:"Accumulator Direction PH",192:"Two Speed Up/ Down Mode",193:"Two SPeed Breakpoint Mode",194:"Surge Enabled",195:"Surge Direction PL",
            196:"Surge Direction PH",197:"Surge Bi-Direction",198:"Mid-Point Relay Enabled",199:"Redundant CPU Present",200:"Reverse Acting Display",
            201:"Reverse Acting Transmitter",202:"PST Mode Contact Power",203:"PST MOde Signal Deviation",204:"PST Mode Schedule/Auto",205:"PSt Mode Contact Unpowered",
            206:"Model Character 1",207:"Model Character 2",208:"Model Character 3",209:"Model Character 4",210:"Model Character 5",211:"Model Character 6",
            212:"Model Character 7",213:"Model Character 8",214:"Model Character 9",215:"Model Character 10",216:"Model Character 11",217:"Model Character 12",
            218:"Model Character 13",219:"Model Character 14",220:"Model Character 15",221:"Model Character 16",222:"Model Character 17",223:"Model Character 18",
            224:"Model Character 19",225:"Model Character 20",226:"Model Character 21",227:"Model Character 22",228:"Model Character 23",229:"Model Character 24",
            230:"Model Character 25",231:"Tag Character 1",232:"Tag Character 2",233:"Tag Character 3",234:"Tag Character 4",235:"Tag Character 5",236:"Tag Character 6",
            237:"Tag Character 7",238:"Tag Character 8",239:"Tag Character 9",240:"Tag Character 10",241:"Tag Character 11",242:"Tag Character 12",243:"Tag Character 13",
            244:"Tag Character 14",245:"Tag Character 15",246:"Tag Character 16",247:"Tag Character 17",248:"Tag Character 18",249:"Tag Character 19",
            250:"Tag Character 20",251:"Tag Character 21",252:"Tag Character 22",253:"Tag Character 23",254:"Tag Character 24",255:"Tag Character 26",
            256:"Tag Character 27",257:"Tag Character 28",258:"Tag Character 29",259:"Tag Character 30",260:"Tag Character 31",261:"Tag Character 32",
            262:"",
263:"",
264:"",
265:"",
266:"",
267:"",
268:"",
269:"",
270:"",
271:"",
272:"",
273:"",
274:"",
275:"",
276:"",
277:"",
278:"",
279:"",
280:"",
281:"",
282:"",
283:"",
284:"",
285:"",
286:"",
287:"",
288:"",
289:"",
290:"",
291:"",
292:"",
293:"",
294:"",
295:"",
296:"",
297:"",
298:"",
299:"",
300:"",
301:"",
302:"",
303:"",
304:"",
305:"",
306:"",
307:"",
308:"",
309:"",
310:"",
311:"",
312:"",
313:"",
314:"",
315:"",
316:"",
317:"",
318:"",
319:"",
320:"",
321:"",
322:"",
323:"",
324:"",
325:"",
326:"",327:"",328:"",329:"",330:"",
331:"",
332:"",
333:"",
334:"",
335:"",
336:"",
337:"",
338:"",
339:"",
340:"",
341:"",
342:"",
343:"",
344:"",
345:"",
346:"",
347:"",
348:"",
349:"",
350:"",
351:"",
352:"",
353:"",
354:"",
355:"",
356:"",
357:"",
358:"",
359:"",
360:"",
361:"",
362:"",
363:"",
364:"",
365:"",
366:"",
367:"",
368:"",
369:"",
370:"",
371:"",
372:"",
373:"",
374:"",
375:"",
376:"",
377:"",
378:"",
379:"",
380:"",
381:"",
382:"",
383:"",
384:"",
385:"",
386:"",
387:"",
388:"",
389:"",
390:"",
391:"",
392:"",
393:"",
394:"",
395:"",
396:"",
397:"",
398:"",
399:"",
400:"",
401:"",
402:"",
403:"",
404:"",
405:"",
406:"",
407:"",
408:"",
409:"",
410:"",
411:"",
412:"",
413:"",
414:"",
415:"",
416:"",
417:"",
418:"",
419:"",
420:"",
421:"",
422:"",
423:"",
424:"",
425:"",
426:"",
427:"",
428:"",
429:"",
430:"",
431:"",
432:"",
433:"",
434:"",
435:"",
436:"",
437:"",
438:"",
439:"",
440:"",
441:"",
442:"",
443:"",
444:"",
445:"",
446:"",
447:"",
448:"",
449:"",
450:"",
451:"",
452:"",
453:"",
454:"",
455:"",
456:"",
457:"",
458:"",
459:"",
460:"",
461:"",
462:"",
463:"",
464:"",
465:"",
466:"",
467:"",
468:"",
469:"",
470:"",
471:"",
472:"",
473:"",
474:"",
475:"",
476:"",
477:"",
478:"",
479:"",
480:"",
481:"",
482:"",
483:"",
484:"",
485:"",
486:"",
487:"",
488:"",
489:"",
490:"",
491:"",
492:"",
493:"",
494:"",
495:"",
496:"",
497:"",
498:"",
499:"",
500:"",
501:"",
502:"",
503:"",
504:"",
505:"",
506:"",
507:"",
508:"",
509:"",
510:"",
511:"",
512:"",
513:"",
514:"",
515:"",
516:"",
517:"",
518:"",
519:"",
520:"",
521:"",
522:"",
523:"",
524:"",
525:"",
526:"",
527:"",
528:"",
529:"",
530:"",
531:"",
532:"",
533:"",
534:"",
535:"",
536:"",
537:"",
538:"",
539:"",
540:"",
541:"",
542:"",
543:"",
544:"",
545:"",
546:"",
547:"",
548:"",
549:"",
550:"",
551:"",
552:"",
553:"",
554:"",
555:"",
556:"",
557:"",
558:"",
559:"",
560:"",
561:"",
562:"",
563:"",
564:"",
565:"",
566:"",
567:"",
568:"",
569:"",
570:""



        }
        return self.index_to_name.get(index, "No Name")

    def retrieve_data(self, *args):
        threading.Thread(target=self.retrieve_data_thread).start()

    def retrieve_data_thread(self):
        # Define the maximum number of requests per second
        MAX_REQUESTS_PER_SECOND = 20  # Increase this number to increase the polling rate
        # Retrieve data from the Modbus server
        # Create a rate limiter
        rate_limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=1.0)
        try:
            unit = int(self.unit_entry.get())
            count = int(self.count_entry.get())
            raw_values = []  # Initialize raw_values outside the loop
            self.raw_values = raw_values
            self.progress[
                'maximum'] = count  # Set the maximum value of the progress bar to the total number of addresses to read
            self.progress['value'] = 0  # Reset the progress bar
            for address in range(0, count):  # Modbus address space is 0-65535
                with rate_limiter:
                    try:
                        result = self.modbus_client.client.read_holding_registers(address, 1, unit=unit)
                        if not result.isError():
                            raw_values.append(result.registers[0])
                            self.progress['value'] += 1  # Increment the progress bar
                            self.progress_label['text'] = f"{self.progress['value']}/{count}"  # Update the label text
                            self.root.update_idletasks()  # Update the GUI
                    except Exception as e:
                        print(f"Exception while reading register at address {address}: {e}")
            # Print the number of elements in raw_values
            print(f"Number of elements in raw_values: {len(raw_values)}")

            self.refresh_table(raw_values)
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")
        self.progress['value'] = 0  # Reset the progress bar

    def refresh_table(self, *args):
        raw_values = self.raw_values
        self.table.delete(*self.table.get_children())
        selected_type = self.data_type_var.get()  # Define selected_type before using it
        if selected_type == "ALL":
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
                                        113, 114, 115, 116, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
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

            Unsigned32Int_indices = [315, 316, 558, 559, 560, 561, 562, 563, 564,
                                     565]

            boolean_indices = [175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
                               191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 567,
                               568]
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
                    if index + 1 in float_indices and i + 1 < len(all_indices) and all_indices[i + 1] == index + 1:
                        value2 = raw_values[index + 1]
                        translated_value = self.translate_value("Float 32 bit", value, value2)
                        data_type = "Float 32 bit"
                    else:
                        continue
                elif index in ASCII16bit_indices:
                    translated_value = self.translate_value("ASCII 16 bit", value)
                    data_type = "ASCII 16 bit"
                elif index in Signed32Int_indices:
                    # Check if this is the first index of a pair
                    if index + 1 in Signed32Int_indices and i + 1 < len(all_indices) and all_indices[
                        i + 1] == index + 1:
                        value2 = raw_values[index + 1]
                        translated_value = self.translate_value("Signed Int 32 bit", value, value2)
                        data_type = "Signed Int 32 bit"
                    else:
                        continue
                elif index in UnsignedInt16bit_indices:
                    translated_value = self.translate_value("Unsigned Int 16 bit", value)
                    data_type = "Unsigned Int 16 bit"
                elif index in Unsigned32Int_indices:
                    # Check if this is the first index of a pair
                    if index + 1 in Unsigned32Int_indices and i + 1 < len(all_indices) and all_indices[
                        i + 1] == index + 1:
                        value2 = raw_values[index + 1]
                        translated_value = self.translate_value("Unsigned Int 32 bit", value, value2)
                        data_type = "Unsigned Int 32 bit"
                    else:
                        continue
                elif index in boolean_indices:
                    translated_value = self.translate_value("Boolean", value)
                    data_type = "Boolean"
                else:
                    translated_value = self.translate_value("holding", value)
                    data_type = "holding"

                # Insert the translated value into the table
                self.table.insert('', 'end', values=(self.get_name(index+1), index+1, data_type, translated_value))

        elif selected_type == "Float 32 bit":
            float_indices = [0, 1, 2, 3, 4, 5, 25, 26, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                             117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                             129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
                             141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
                             153, 154, 155, 156, 157, 158, 159, 160, 313, 314, 569,
                             570]  # The indices of the values you want to read as 32-bit floats
            for i in range(0, len(float_indices), 2):  # Step by 2
                index1 = float_indices[i]
                index2 = float_indices[i + 1] if i + 1 < len(
                    float_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.translate_value("Float 32 bit", value1, value2)
                translated_value =   round(translated_value,3)
                self.table.insert('', 'end', values=(self.get_name(index1+1),index1+1, "Float 32 bit", translated_value))
        elif selected_type == "ASCII 16 bit":
            ASCII16bit_indices = [205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
                                  220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234,
                                  235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249,
                                  250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264,
                                  265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
                                  280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
                                  295, 296, 297, 298, 299, 300, 301, 302,
                                  303]  # The indices of the values you want to read
            for i in range(0, len(ASCII16bit_indices)):
                index1 = ASCII16bit_indices[i]
                value1 = raw_values[index1]
                translated_value = self.translate_value("ASCII 16 bit", value1)
                # translated_value =   round(translated_value,2)
                self.table.insert('', 'end', values=(self.get_name(index1+1), index1+1, "ASCII 16 bit", translated_value))
        elif selected_type == "Signed Int 32 bit":
            Signed32Int_indices = [6, 7, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
                                   44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
                                   63, 64, 65, 66, 67, 68, 69, 70]  # The indices of the values you want to read
            for i in range(0, len(Signed32Int_indices), 2):  # Step by 2
                index1 = Signed32Int_indices[i]
                index2 = Signed32Int_indices[i + 1] if i + 1 < len(
                    Signed32Int_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.translate_value("Signed Int 32 bit", value1, value2)
                # translated_value =   round(translated_value,2)
                self.table.insert('', 'end',
                                  values=(self.get_name(index1+1), index1+1, "Signed Int 32 bit", translated_value))
        elif selected_type == "Unsigned Int 16 bit":
            UnsignedInt16bit_indices = [12, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
                                        98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                                        113, 114, 115, 116, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                        172, 173, 306, 312, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429,
                                        430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444,
                                        445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459,
                                        460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474,
                                        475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489,
                                        490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504,
                                        505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519,
                                        520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534,
                                        535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549,
                                        550, 551, 552, 553, 554, 555, 556, 557,
                                        566]  # The indices of the values you want to read
            for i in range(0, len(UnsignedInt16bit_indices)):
                index1 = UnsignedInt16bit_indices[i]
                value1 = raw_values[index1]
                translated_value = self.translate_value("Unsigned Int 16 bit", value1)
                self.table.insert('', 'end',
                                  values=(self.get_name(index1+1), index1+1, "Unsigned Int 16 bit", translated_value))
        elif selected_type == "Unsigned Int 32 bit":
            Unsigned32Int_indices = [315, 316, 558, 559, 560, 561, 562, 563, 564,
                                     565]  # The indices of the values you want to read
            for i in range(0, len(Unsigned32Int_indices), 2):  # Step by 2
                index1 = Unsigned32Int_indices[i]
                index2 = Unsigned32Int_indices[i + 1] if i + 1 < len(
                    Unsigned32Int_indices) else index1  # Use index1 if there's no second index
                value1 = raw_values[index1]
                value2 = raw_values[index2]

                translated_value = self.translate_value("Unsigned Int 32 bit", value1, value2)
                # translated_value =   round(translated_value,2)
                self.table.insert('', 'end',
                                  values=(self.get_name(index1+1), index1+1, "Unsigned Int 32 bit", translated_value))
        elif selected_type == "Boolean":
            boolean_indices = [175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
                               191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 567,
                               568]  # The indices of the values you want to read
            for i in range(0, len(boolean_indices)):
                index1 = boolean_indices[i]
                value1 = raw_values[index1]
                translated_value = self.translate_value("Boolean", value1)
                self.table.insert('', 'end', values=(self.get_name(index1+1), index1+1, "Boolean", translated_value))
        elif selected_type == "Binary":
            # Insert raw_values into the table
            for i, value in enumerate(raw_values):
                translated_value = self.translate_value("Binary", value)  # Translate the value
                self.table.insert('', 'end',
                                  values=(
                                  self.get_name(i+1), i+1, selected_type, translated_value))  # Use the translated value
        else:
            # Insert raw_values into the table
            for i, value in enumerate(raw_values):
                translated_value = self.translate_value("holding", value)  # Translate the value
                self.table.insert('', 'end', values=(self.get_name(i+1), i+1, selected_type, translated_value))  # Use the translated value

    def translate_value(self, data_type, value1, value2=None):
        # Translate the value based on the selected data type
        if data_type == "holding":
            return value1
        elif data_type == "Float 32 bit":
            # Assuming the value is a 32-bit float
            binary_data = struct.pack('>HH', value1, value2)  # Combine two 16-bit values
            decoded_value = struct.unpack('>f', binary_data)[0]
            return decoded_value
        elif data_type == "ASCII 16 bit":
            # Assuming the value is a 16-bit value representing an ASCII character
            ascii_value = value1 & 0xFF
            try:
                decoded_value = chr(ascii_value)
                # Check if the character is printable
                if not decoded_value.isprintable():
                    decoded_value = unicodedata.name(decoded_value, 'unknown')
            except ValueError:
                decoded_value = 'unknown'
            return decoded_value
        elif data_type == "Unsigned Int 16 bit":
            # Interpret as unsigned int
            return value1
        elif data_type == "Signed Int 16 bit":
            # Interpret as signed int
            return struct.unpack('>h', struct.pack('>H', value1))[0]
        elif data_type == "Epoch 32 bit":
            # Assuming the value is a 32-bit epoch timestamp
            binary_data = struct.pack('>HH', value1, value2)  # Combine two 16-bit values
            decoded_value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(struct.unpack('>I', binary_data)[0]))
            return decoded_value
        elif data_type == "Binary":
            # Assuming the value is a binary string
            binary_string = bin(value1)[2:]  # Remove '0b' prefix
            return binary_string
        elif data_type == "Boolean":
            # Translate 0/1 to True/False
            if value1 == 0:
                return False
            elif value1 == 1:
                return True
            else:
                return 'Not a Boolean'
        elif data_type == "Byte":
            # Assuming the value is a byte (8 bits)
            byte_value = value1 & 0xFF
            return byte_value
        elif data_type == "Signed Int 32 bit":
            binary_data = struct.pack('>HH', value1, value2)  # Combine two 16-bit values
            decoded_value = struct.unpack('>l', binary_data)[0]
            return decoded_value
        elif data_type == "Unsigned Int 32 bit":
            # Assuming the value is an unsigned 32-bit integer
            binary_data = struct.pack('>HH', value1, value2)  # Combine two 16-bit values
            decoded_value = struct.unpack('>L', binary_data)[0]
            return decoded_value
        else:
            return value1
