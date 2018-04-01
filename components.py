__author__ = 'develru'

from RPiPy import rpilib
import time
from nanpy import ArduinoApi, SerialManager



class DriveModule():
    def __init__(self):
        self.gpio17 = rpilib.GPIOrtx('17')
        self.gpio18 = rpilib.GPIOrtx('18')
        self.gpio22 = rpilib.GPIOrtx('22')
        self.gpio23 = rpilib.GPIOrtx('23')

    def online(self):
        self.gpio17.export()
        self.gpio17.setDirection('out')

        self.gpio18.export()
        self.gpio18.setDirection('out')

        self.gpio22.export()
        self.gpio22.setDirection('out')

        self.gpio23.export()
        self.gpio23.setDirection('out')

    def offline(self):
        self.gpio17.unexport()
        self.gpio18.unexport()
        self.gpio22.unexport()
        self.gpio23.unexport()

    def stop(self):
        self.gpio17.writeValue('0')
        self.gpio18.writeValue('0')
        self.gpio22.writeValue('0')
        self.gpio23.writeValue('0')

    def drive_forward(self):
        self.gpio18.writeValue('1')
        self.gpio22.writeValue('1')

    def drive_backward(self):
        self.gpio17.writeValue('1')
        self.gpio23.writeValue('1')

    def steer_left(self):
        self.gpio17.writeValue('1')
        self.gpio22.writeValue('1')
        time.sleep(0.2)
        self.gpio17.writeValue('0')
        self.gpio22.writeValue('0')

    def steer_right(self):
        self.gpio18.writeValue('1')
        self.gpio23.writeValue('1')
        time.sleep(0.2)
        self.gpio18.writeValue('0')
        self.gpio23.writeValue('0')


def main():
    try:
        connection = SerialManager()
        a = ArduinoApi(connection=connection)
    except:
        print('Failed to connect to Arduino!')

    try:
        ENA = 10
        ENB = 5
        IN1 = 9
        IN2 = 8
        IN3 = 7
        IN4 = 6
        a.pinMode(IN1, a.OUTPUT)
        a.pinMode(IN2, a.OUTPUT)
        a.pinMode(ENA, a.OUTPUT)
        a.digitalWrite(ENA, a.HIGH)
        a.pinMode(IN3, a.OUTPUT)
        a.pinMode(IN4, a.OUTPUT)
        a.pinMode(ENB, a.OUTPUT)
        a.digitalWrite(ENB, a.HIGH)

        a.digitalWrite(IN3, a.LOW)
        a.digitalWrite(IN4, a.HIGH) # left wheel back
        a.digitalWrite(IN1, a.HIGH)
        a.digitalWrite(IN2, a.LOW) # right wheel backward
        time.sleep(0.5)
        a.digitalWrite(IN3, a.LOW)
        a.digitalWrite(IN4, a.LOW)
        a.digitalWrite(IN1, a.LOW)
        a.digitalWrite(IN2, a.LOW)

        a.digitalWrite(IN3, a.HIGH)
        a.digitalWrite(IN4, a.LOW) # left wheel forward
        a.digitalWrite(IN1, a.LOW)
        a.digitalWrite(IN2, a.HIGH) # right whelle forward
        time.sleep(0.5)
        a.digitalWrite(IN3, a.LOW)
        a.digitalWrite(IN4, a.LOW)
        a.digitalWrite(IN1, a.LOW)
        a.digitalWrite(IN2, a.LOW)

        time.sleep(0.5)
        a.digitalWrite(ENB, a.LOW)
    except:
        a.digitalWrite(ENB, a.LOW)


if __name__ == '__main__':
    main()