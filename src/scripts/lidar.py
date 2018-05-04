import rospy as rp
from std_msgs.msg import String

import serial
import time

pub = rp.Publisher('lidar', String, queue_size=10)
rp.init_node('lidar', anonymous=False)

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)

#ser.write(0x42)
ser.write(bytes(b'B'))

#ser.write(0x57)
ser.write(bytes(b'W'))

#ser.write(0x02)
ser.write(bytes(2))

#ser.write(0x00)
ser.write(bytes(0))

#ser.write(0x00)
ser.write(bytes(0))

#ser.write(0x00)
ser.write(bytes(0))
          
#ser.write(0x01)
ser.write(bytes(1))
          
#ser.write(0x06)
ser.write(bytes(6))

def lidar():
    while(True):
        while(ser.in_waiting >= 9):
            if((b'Y' == ser.read()) and ( b'Y' == ser.read())):

                Dist_L = ser.read()
                Dist_H = ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                for i in range (0,5):
                    ser.read()
                    
                return str(Dist_Total)
            
r = rp.Rate(10)
def publisher():
    while not rp.is_shutdown():
        pub.publish(lidar())
    rp.spin()

if __name__ == '__main__':
    try:
        publisher()
    except rp.ROSInterruptException:
        pass
