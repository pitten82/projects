from time import sleep
import pygatt
import logging
from influxdb import InfluxDBClient

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

sensor_mac = "F8:8A:5E:36:CB:34"
adapter = pygatt.GATTToolBackend(hci_device='hci0')
client = InfluxDBClient(host='192.168.128.92', 
                        port=8086, 
                        database="KP_lab_data")


# Celsius to Fahrenheit conversion
def fahrenheit(celcius):
    return int(round(celcius * (9/5.0) + 32))


# Process and save the realtime data
def handle_notification(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print(handle, value)

    # if handle == 0x000b:
    #     pressure = int(int.from_bytes(value, "big"))
    #     print(f"pressure: ", pressure)

    # if handle == 0x0012:
    #     temperature = value
    #     print(f"temperature: ", temperature)

    # print(handle)
    # print(value)


try:
    adapter.start()
    print("BT started")

    try:
        device = adapter.connect(sensor_mac, timeout=10)
        print("connected...")
    except:
        print("couldn't connect, retrying...")
        device = adapter.connect(sensor_mac, timeout=10)
        print("connected...")
    sleep(5)

    # Enable notifications
    notification_enable = bytearray([0x01,0x00])
    measurement_interval = bytearray([0x05,0x00])

    # device.char_write_handle(21, measurement_interval)
    # sleep(5)
    # device.char_write_handle(0xd, notification_enable) # pressure
    # sleep(5)
    # device.char_write_handle(0x13, notification_enable) # temperature
    
    device.subscribe("835ab4c0-51e4-11e3-a5bd-0002a5d5c51b", 
                            callback=handle_notification)
    
    # try:
    #     device.subscribe("835ab4c0-51e4-11e3-a5bd-0002a5d5c51b", 
    #                     callback=handle_notification)
    # except Exception as e:
    #     try:
    #         sleep(5)
    #         device.subscribe("835ab4c0-51e4-11e3-a5bd-0002a5d5c51b",
    #                         callback=handle_notification)
    #     except:
    #         pass


    # device.subscribe("00002a1c-0000-1000-8000-00805f9b34fb", 
    #                 callback=handle_notification, 
    #                 wait_for_response=False)
    # try:
    #     device.subscribe("835ab4c0-51e4-11e3-a5bd-0002a5d5c51b", callback=handle_notification)
    #     # device.subscribe("00002a1c-0000-1000-8000-00805f9b34fb", callback=handle_notification)
    # except Exception as e:
    #         try:
    #             device.subscribe("835ab4c0-51e4-11e3-a5bd-0002a5d5c51b", callback=handle_notification)
    #             # device.subscribe("00002a1c-0000-1000-8000-00805f9b34fb", callback=handle_notification)
    #         except:
    #             pass

    # pressure_hex = device.char_read_handle("0x000b")
    # battery_hex = device.char_read_handle("0x0018")
    # temperature_hex = device.char_read_handle("0x0012")

    #convert hex data
    # pressure = int(int.from_bytes(pressure_hex, "big"))
    # battery = int(int.from_bytes(battery_hex, "big"))
    # temperature = (int.from_bytes(temperature_hex[2:3], "big"))/10

    # if pressure > 65000:
    #     pressure = pressure -65536

    # json_body = [
    #     {"measurement": "pressures",
    #     "fields": {"P1": pressure, "batt1": battery, "temp1": temperature}}
    #     ]
    

    # client.write_points(json_body)

    # #print(hexlify(data))
    # print(f"pressure: {pressure} - {hexlify(pressure_hex)}")
    # print(f"battery: {battery} - {hexlify(battery_hex)}")
    # print(f"temp: {temperature} - {(temperature_hex)}")
    
    #input("press any key")
    # sleep(10)

    input("Enter any key to quit....")
    print("\n")

finally:
    print("stopping..")
    adapter.stop()
    print("stopped")