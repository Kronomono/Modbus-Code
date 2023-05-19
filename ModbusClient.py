#ModbusClient.py
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

class ModbusClient:
    def __init__(self, ip_address="127.0.0.1", port=502):
        # Initialize the modbus client with the provided IP address and port
        self.ip_address = ip_address
        self.port = port
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

    def read_holding_registers(self, address, count, unit=1):
        # Attempt to read the holding registers from the modbus server
        try:
            response = self.client.read_holding_registers(address=address, count=count, unit=unit)
            if response.isError():
                print(f"Modbus response error: {response}")
            else:
                print(f"Received data: {response.registers}")
                return response.registers  # Add this line
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def close(self):
        # Attempt to close the modbus connection
        if self.client.is_socket_open():
            self.client.close()
            print("Modbus connection closed.")
        else:
            print("Modbus connection is not open.")

    def write_register(self, address, value, unit=1):
        # Attempt to write a value to a specific register
        try:
            response = self.client.write_register(address, value, unit=unit)
            if response.isError():
                print(f"Modbus response error: {response}")
            else:
                print(f"Written value: {value} to address: {address}")
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")

    def write_float(self, address, value, unit=1):
        # Attempt to write a float value to a specific register
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_32bit_float(value)
        payload = builder.to_registers()
        response = self.client.write_registers(address, payload, unit=unit)
        if response.isError():
            print(f"Modbus response error: {response}")
        else:
            print(f"Written value: {value} to address: {address}")

    def write_ascii(self, address, ascii_string, unit=1):
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