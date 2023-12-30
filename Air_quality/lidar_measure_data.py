#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:

$ ./record_measurments.py out.txt'''

'''
Mostmár nagyjából tudom, hogy melyik érték mit jelent
Itt van a fontos forrás:

https://github.com/SkoltechRobotics/rplidar/blob/master/rplidar.py

'''
import sys
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB0'
DMAX = 4000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line


def run(path):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    info = lidar.get_info()
    health = lidar.get_health()


    #fig = plt.figure()
    #ax = plt.subplot(111, projection='polar')
    #line = ax.scatter([0,0], [0,0], s=5, c=[IMIN, IMAX],
    #                  cmap=plt.cm.Greys_r, lw=0)
    #ax.set_rmax(DMAX)
    #ax.grid(True)

    #iterator = lidar.iter_scans(max_buf_meas=3000)
    #ani = animation.FuncAnimation(fig, update_line,
    #                              fargs=(iterator, line), interval=50)
    #plt.show()


    #Adatgyűjtés2
    outfile = open(path, 'w')
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            line = '\t'.join(str(v) for v in measurment)
            print(line)
            outfile.write(line + '\n')
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    run('/home/miguff/PycharmProjects/Air_quality/Lidar_measure/record_measurements_3.csv')