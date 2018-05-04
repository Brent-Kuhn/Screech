import rospy as rp
from std_msgs.msg import String
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import math
import time
import atexit

mh = Adafruit_MotorHAT(addr=0x60)
driveMotor = mh.getMotor(4)

def callback(data):
    rp.loginfo(data.data)
    
def drive(speed):
    driveMotor.setSpeed(speed)
    driveMotor.run(Adafruit_MotorHAT.FORWARD)

def subscribeToLidar():
    rp.init_node('driver')
    rp.Subscriber('lidar', String, callback)
    rp.spin()
    
if __name__ == '__main__':
    try:
        subscribeToLidar()
        '''
        speed =  255 * 2/math.pi * math.atan(speedstuff/15)
        drive(speed)
        '''
    except rp.ROSInterruptException:
        pass
driveMotor.setSpeed(0)
atexit.register(driveMotor.run, Adafruit_MotorHAT.RELEASE)