import numpy as np
import pandas as pd
import time
import argparse
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice
import seeed_si114x
import seeed_dht
import SDL_Pi_HM3301 as PM_sensor
from datetime import datetime



def main():
    SI1145 = seeed_si114x.grove_si114x()
    parser = argparse.ArgumentParser()
    parser.add_argument("--i2c-port", '-p', default='/dev/i2c-1')
    args = parser.parse_args()
    sensor = seeed_dht.DHT('11', 12)

    Dataset = pd.DataFrame(columns = ['LogDate', 'PM1', 'PM2.5', 'PM10', 'Co2', 'Temperature', 'Humidity', 'Light', 'UV', 'IR'])

    with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
        scd4x = Scd4xI2cDevice(I2cConnection(i2c_transceiver))
        scd4x.stop_periodic_measurement()



        scd4x.start_periodic_measurement()
        hm3301 = PM_sensor.Seeed_HM3301()

        for _ in range(60):
            time.sleep(5)
            Datum = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            #Kiszedjük a számunkra szükséges adatokat
            co2, temperature, humidity = scd4x.read_measurement()
            data = hm3301.read_data()
            pm1_read, pm2_5_read, pm10_read = hm3301.data_values(data)

            #Értékeljük a szükséges adatokat
            #print(f"A PM2.5 értéke {pm2_5_read}")
            #print(f"A PM10 értéke {pm10_read}")
            #hm3301.parse_data(data)

            Co2 = '{}'.format(co2)
            Temperature = '{}'.format(temperature)
            Humidity = '{}'.format(humidity)

            Co2 = float(Co2[:-3])
            Temperature = float(Temperature[:-2])
            Humidity = float(Humidity[:-3])

            Ertekek = [Datum, pm1_read, pm2_5_read, pm10_read, Co2, Temperature, Humidity, SI1145.ReadVisible, SI1145.ReadUV/100, SI1145.ReadIR]
            print("Co2: {}, Temperature: {}, Humidity: {}".format(co2, temperature, humidity))
            #print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible, SI1145.ReadUV/100, SI1145.ReadIR))
            Dataset.loc[len(Dataset)] = Ertekek
            print(Dataset)


if __name__ == '__main__':
    main()

