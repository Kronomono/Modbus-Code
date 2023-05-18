from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

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
