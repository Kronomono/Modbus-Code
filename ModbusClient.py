#ModbusClient.py
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import time
from pymodbus.constants import Endian

unit = 10
class ModbusClient:
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

