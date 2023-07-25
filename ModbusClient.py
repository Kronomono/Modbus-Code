#ModbusClient.py
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import time
import struct
import unicodedata
from tkinter import messagebox, ttk


class ModbusClient:

    def __init__(self, ip_address="127.0.0.1", port=502, unit= 1):
        # Initialize the modbus client with the provided IP address, port, and unit
        self.ip_address = ip_address
        self.port = port
        self.unit = unit
        self.client = ModbusTcpClient(self.ip_address, port=self.port)

    def update_host_port(self, ip_address, port, unit):
        # Update the IP address, port, and unit for the modbus client and create a new client instance
        self.ip_address = ip_address
        self.port = port
        self.unit = unit
        self.client = ModbusTcpClient(self.ip_address, port=self.port)
        print(f"Updated client host to: {self.ip_address}")
        print(f"Updated client port to: {self.port}")
        print(f"Updated client unit to: {self.unit}")


    def connect(self):
        # Attempt to connect to the modbus server
        print(f"Connecting to client at host: {self.ip_address}")
        print(f"Connecting to client at port: {self.port}")
        try:
            self.client.connect()
            if self.client.is_socket_open():
                print("Modbus connection established.")
                return True
            else:
                print("Failed to establish Modbus connection.")
                return False
        except Exception as e:
            print(f"Exception while connecting to Modbus slave: {e}")
            return False

    def close(self):
        try:
            # Attempt to close the modbus connection
            if self.client.is_socket_open():
                self.client.close()
                print("Modbus connection closed.")
            else:
                print("Modbus connection is not open.")
        except Exception as e:
            print(f"Exception while closing the Modbus connection: {e}")

    def is_connected(self):
        # Check if the Modbus client is connected
        if self.client.is_socket_open():
            print("Modbus connection is open.")
            return True
        else:
            print("Modbus connection is closed.")
            return False
    def write_register(self, address, value):
        # Default to instance's unit if not provided
        unit = self.unit
        # Attempt to write a value to a specific register
        try:
            response = self.client.write_register(address, value, unit)
            if response.isError():
                print(f"Modbus response error: {response}")
                messagebox.showerror("Error", f"Modbus reponse error: {response}")

            else:
                print(f"Written value: {value} to address: {address}")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def write_float(self, address, value):
        # Default to instance's unit if not provided
        unit = self.unit
        # Convert the float value to a 32-bit integer
        float_as_int = struct.unpack('<I', struct.pack('<f', value))[0]

        # Write the high-order word of the integer value to the first register
        self.write_register(address, float_as_int >> 16, unit)

        # Write the low-order word of the integer value to the next register
        self.write_register(address + 1, float_as_int & 0xFFFF, unit)

    def write_ascii(self, address, ascii_string):
        # Default to instance's unit if not provided
        unit = self.unit
        # Attempt to write an ASCII string to a specific register
        try:
            hex_data = [ord(c) for c in ascii_string]
            response = self.client.write_registers(address, hex_data, unit)
            if response.isError():
                print(f"Modbus response error: {response}")
                messagebox.showerror("Error", f"Modbus reponse error: {response}")
            else:
                print(f"Written ASCII string: {ascii_string} to address: {address}")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def translate_value(self, data_type, value1, value2=None,value3=None,value4=None):
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
                decoded_value = 'ValueError'
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
                return "False"
            elif value1 == 1:
                return "True"
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
        elif data_type == "Unsigned Int 8 bit":
            # Assuming the value is an unsigned 8-bit integer
            return value1 & 0xFF
        elif data_type == "Epoch 64 bit time":
            # Assuming the values are 4 x 16-bit chunks of a 64-bit epoch timestamp
            binary_data = struct.pack('>HHHH', value1, value2, value3, value4)  # Combine four 16-bit values
            #to use utc. use time.gmtime
            decoded_value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(struct.unpack('>Q', binary_data)[0]))

            return decoded_value
        elif data_type == "Epoch 64 bit":
            # Assuming the values are 4 x 16-bit chunks of a 64-bit epoch timestamp
            binary_data = struct.pack('>HHHH', value1, value2, value3, value4)  # Combine four 16-bit values

            # Unpack the binary data without time translation
            unpacked_values = struct.unpack('>Q', binary_data)
            return unpacked_values
        else:
            return value1
