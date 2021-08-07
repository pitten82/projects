from time import sleep
import pygatt
from influxdb import InfluxDBClient

sensor_mac = "F8:8A:5E:36:CB:34"
adapter = pygatt.GATTToolBackend(hci_device='hci0')
client = InfluxDBClient(host='192.168.128.92', 
                        port=8086, 
                        database="KP_lab_data")




try:
    adapter.start()
    print("BT started")

    try:
        device = adapter.connect(sensor_mac, timeout=10)
        print("connected...")
    except:
        print("couldn't connect, retrying...")
        device = adapter.connect(sensor_mac, timeout=10)

    while True:

        print("reading")
        #read specific characteristics
        pressure_hex = device.char_read_handle("0x000b")
        battery_hex = device.char_read_handle("0x0018")
        temperature_hex = device.char_read_handle("0x0012")

        #convert hex data
        pressure = int(int.from_bytes(pressure_hex, "big"))
        battery = int(int.from_bytes(battery_hex, "big"))
        temperature = (int.from_bytes(temperature_hex[2:3], "big"))/10

        if pressure > 65000:
            pressure = pressure -65536

        json_body = [
            {"measurement": "pressures",
            "fields": {"P1": pressure, "batt1": battery, "temp1": temperature}}
            ]
        

        client.write_points(json_body)

        #print(hexlify(data))
        print(f"pressure: {pressure} - {hexlify(pressure_hex)}")
        print(f"battery: {battery} - {hexlify(battery_hex)}")
        print(f"temp: {temperature} - {(temperature_hex)}")
        
        #input("press any key")
        sleep(10)

finally:
    device.disconnect()
    adapter.stop()