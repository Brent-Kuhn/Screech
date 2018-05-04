import rospy as rp
from std_msgs.msg import String

import atexit
import RPi.GPIO as GPIO
import time

pub = rp.Publisher('sensor1', String, queue_size=10)
rp.init_node('leftSensor', anonymous=False)

Sensor_Array = [[4, 17], [18, 27], [22, 23]]

def Ultrasonic_Sensor(GPIO_Numbers):
    TRIG = GPIO_Numbers[0]
    ECHO = GPIO_Numbers[1]
    GPIO.setmode(GPIO.BCM)

    #print("Distance Measurement In Progress")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, 0)
    #print("Waiting for sensor to settle")
    time.sleep(.1)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = distance//1

    GPIO.cleanup()

    return str(distance)

r = rp.Rate(10)
def publisher():
    while not rp.is_shutdown():
        pub.publish(Ultrasonic_Sensor(Sensor_Array[0]))
    rp.spin()

if __name__ == '__main__':
    try:
        publisher()
    except rp.ROSInterruptException:
        pass

atexit.register(GPIO.cleanup)