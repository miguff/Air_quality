import numpy as np
import pandas as pd
import time
import argparse
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice
import seeed_si114x
import signal
import seeed_dht

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
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

        for _ in range(60):
            time.sleep(5)
            co2, temperature, humidity = scd4x.read_measurement()
            print("Co2: {}, Temperature: {}, Humidity: {}".format(co2, temperature, humidity))
            print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible, SI1145.ReadUV/100, SI1145.ReadIR))
            humi, temp = sensor.read()
            print('DHT{0}, humidity {1:.1f}%, temperature {2:1f}*'.format(sensor.dht_type, humi, temp))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
