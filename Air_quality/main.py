import numpy as np
import pandas as pd
import time
import argparse
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice
import seeed_si114x
import signal
import seeed_dht
import pigpio
import SDL_Pi_HM3301 as PM_sensor

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    PM2_5 = 25
    PM10 = 50
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    SI1145 = seeed_si114x.grove_si114x()
    parser = argparse.ArgumentParser()
    parser.add_argument("--i2c-port", '-p', default='/dev/i2c-1')
    args = parser.parse_args()
    sensor = seeed_dht.DHT('11', 12)

    with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
        scd4x = Scd4xI2cDevice(I2cConnection(i2c_transceiver))
        scd4x.stop_periodic_measurement()
        print("scd4x Serial Number: {}".format(scd4x.read_serial_number()))

        scd4x.start_periodic_measurement()
        hm3301 = PM_sensor.Seeed_HM3301()

        for _ in range(60):
            time.sleep(5)
            co2, temperature, humidity = scd4x.read_measurement()
            data = hm3301.read_data()
            pm1_read, pm2_5_read, pm10_read = hm3301.data_values(data)
            AQI2_5 = (pm2_5_read/PM2_5)*100
            AQI10 = (pm10_read/PM10)*100
            AQI_measure(AQI2_5)
            AQI_measure(AQI10)
            #hm3301.parse_data(data)
            #print("Co2: {}, Temperature: {}, Humidity: {}".format(co2, temperature, humidity))
            #print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible, SI1145.ReadUV/100, SI1145.ReadIR))
            #humi, temp = sensor.read()
            #print('DHT{0}, humidity {1:.1f}%, temperature {2:1f}*'.format(sensor.dht_type, humi, temp))

def AQI_measure(data):
    if data > 0 and data <= 33:
        print("Very Good AQI")
    elif data <= 66:
        print("Good AQI")
    elif data <= 99:
        print("Fair AQI")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
