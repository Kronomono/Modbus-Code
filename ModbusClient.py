from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

class ModbusClient:
    def __init__(self, ip_address="127.0.0.1", port=502):
        self.ip_address = ip_address
        self.port = port
        self.client = ModbusTcpClient(self.ip_address, port=self.port)

    def update_host_port(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client = ModbusTcpClient(self.ip_address, port=self.port)  # Create a new client instance
        print("Updated client host to:", self.ip_address)
        print("Updated client port to:", self.port)

    def connect(self):
        print("Connecting to client at host:", self.ip_address)
        print("Connecting to client at port:", self.port)
        try:
            self.client.connect()
            if self.client.is_socket_open():
                print("Modbus connection established.")
                return True  # Return True to indicate a successful connection
            else:
                print("Failed to establish Modbus connection.")
                return False
        except Exception as e:  # Catch more general exception
            print("Exception while connecting to Modbus slave:", str(e))
            return False  # Return False to indicate a failed connection

    def read_holding_registers(self, address, count, unit=1):
        try:
            response = self.client.read_holding_registers(address=address, count=count, unit=unit)
            if response.isError():
                print("Modbus response error:", response)
            else:
                print("Received data:", response.registers)
        except ModbusIOException as e:
            print("Modbus communication error:", str(e))

    def close(self):
        if self.client.is_socket_open():
            self.client.close()
            print("Modbus connection closed.")
        else:
            print("Modbus connection is not open.")

    def write_register(self, address, value, unit=1):
        try:
            response = self.client.write_register(address, value, unit=unit)
            if response.isError():
                print("Modbus response error:", response)
            else:
                print("Written value:", value, "to address:", address)
        except ModbusIOException as e:
            print("Modbus communication error:", str(e))

    def write_float(self, address, value, unit=1):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_32bit_float(value)
        payload = builder.to_registers()
        response = self.client.write_registers(address, payload, unit=unit)
        if response.isError():
            print("Modbus response error:", response)
        else:
            print("Written value:", value, "to address:", address)

    def write_ascii(self, address, ascii_string, unit=1):
        try:
            # Convert ASCII string to hexadecimal values
            hex_data = [ord(c) for c in ascii_string]

            # Use pymodbus function to write multiple registers
            response = self.client.write_registers(address, hex_data, unit=unit)

            if response.isError():
                print("Modbus response error:", response)
            else:
                print("Written ASCII string:", ascii_string, "to address:", address)
        except ModbusIOException as e:
            print("Modbus communication error:", str(e))
