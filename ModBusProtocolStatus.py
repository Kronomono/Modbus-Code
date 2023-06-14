#ModBusProtocolStatus.py
import tkinter as tk
from tkinter import messagebox, ttk
from ratelimiter import RateLimiter
import threading
from Names import Names
from PIL import Image, ImageTk
from ModBusProtocolConnection import ModBusProtocolConnection
from WidgetTemplateCreator import  WidgetTemplateCreator


class ModBusProtocolStatus:
    def __init__(self, root, modbus_client):
        #references to other classes
        self.root = root
        self.modbus_client = modbus_client
        self.names = Names()
        self.ModBusProtocolConnection = ModBusProtocolConnection(root,modbus_client)
        self.widgetTemp = WidgetTemplateCreator


        # Create a main frame to take up the entire window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)


    def create_widgets(self):
        # Create the Connect
        self.add_image("Images/rexa logo.png", 300, 50, 0.5, 0)
        self.create_progress_bar()
        self.updateDataBtn = self.widgetTemp.create_button(self,'Update Data',0.05,0.08,10,1,10,self.retrieve_data)


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

    def create_progress_bar(self):
        self.progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        self.progress.place(relx=0.5, rely=0.15, relwidth=0.8, anchor=tk.CENTER)
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

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
            self.progress['maximum'] = count
            self.progress['value'] = 0  # Reset the progress bar
            for address in range(0, count):
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

            #self.refresh_table(raw_values)
        except ValueError:
            print("Invalid unit or count value. Please enter a valid number.")
            messagebox.showerror("Error", "Invalid unit or count value. Please enter a valid number.")
        except Exception as e:
            print(f"Exception while reading data from Modbus server: {e}")
            messagebox.showerror("Error", f"Exception while reading data from Modbus server: {e}")



