from rplidar import RPLidar
import numpy as np
from math import floor
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

scan_data = [0]*360
print(scan_data)

for i, scan in enumerate(lidar.iter_scans()):
    for (_, angle, distance) in scan:
        print(_)
        print(angle)
        print(distance)
        scan_data[min([359, floor(angle)])] = distance
        print(scan_data)
    if i > 5:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        break


