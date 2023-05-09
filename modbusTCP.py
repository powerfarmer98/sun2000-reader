from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
#your inverter ip
ip_inverter = '192.168.178.144'

client = ModbusClient(ip_inverter, port = 502)
client.connect ()
time.sleep (1)
if client.connect ():
    request = client.read_holding_registers(address = 30000, count = 15, unit = 1)

    print (request.registers [0])
    print (request.registers [1])
else:
    print ('if you are conected via LAN something is wrong with IP or port')
