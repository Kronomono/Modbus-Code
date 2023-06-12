#ModbusClient.py
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import time
from pymodbus.constants import Endian
import struct


class ModbusClient:
    unit = 10
    def __init__(self, ip_address="127.0.0.1", port=502, unit = 1):
        # Initialize the modbus client with the provided IP address and port
        self.ip_address = ip_address
        self.port = port
        self.unit = unit
        self.client = ModbusTcpClient(self.ip_address, port=self.port)

    def update_host_port(self, ip_address, port):
        # Update the IP address and port for the modbus client and create a new client instance
        self.ip_address = ip_address
        self.port = port
        self.client = ModbusTcpClient(self.ip_address, port=self.port)
        print(f"Updated client host to: {self.ip_address}")
        print(f"Updated client port to: {self.port}")


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
        # Attempt to close the modbus connection
        if self.client.is_socket_open():
            self.client.close()
            print("Modbus connection closed.")
        else:
            print("Modbus connection is not open.")


    def write_register(self, address, value, unit= unit):
        # Attempt to write a value to a specific register
        try:
            response = self.client.write_register(address, value, unit=unit)
            if response.isError():
                print(f"Modbus response error: {response}")
            else:
                print(f"Written value: {value} to address: {address}")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def write_float(self, address, value, unit=unit):
        # Convert the float value to a 32-bit integer
        float_as_int = struct.unpack('<I', struct.pack('<f', value))[0]

        # Write the high-order word of the integer value to the first register
        self.write_register(address, float_as_int >> 16, unit)

        # Write the low-order word of the integer value to the next register
        self.write_register(address + 1, float_as_int & 0xFFFF, unit)

    def write_ascii(self, address, ascii_string, unit= unit):
        # Attempt to write an ASCII string to a specific register
        try:
            hex_data = [ord(c) for c in ascii_string]
            response = self.client.write_registers(address, hex_data, unit=unit)
            if response.isError():
                print(f"Modbus response error: {response}")
            else:
                print(f"Written ASCII string: {ascii_string} to address: {address}")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")
