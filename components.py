__author__ = 'develru'

from RPiPy import rpilib
import time
from nanpy import ArduinoApi, SerialManager



class DriveModule():
    def __init__(self):
        # self.gpio17 = rpilib.GPIOrtx('17')
        # self.gpio18 = rpilib.GPIOrtx('18')
        # self.gpio22 = rpilib.GPIOrtx('22')
        # self.gpio23 = rpilib.GPIOrtx('23')
        try:
            connection = SerialManager()
            self.a = ArduinoApi(connection=connection)
        except:
            print('Failed to connect to Arduino!')

        self.ENA = 10
        self.ENB = 5
        self.IN1 = 9
        self.IN2 = 8
        self.IN3 = 7
        self.IN4 = 6

    def online(self):
        # self.gpio17.export()
        # self.gpio17.setDirection('out')

        # self.gpio18.export()
        # self.gpio18.setDirection('out')

        # self.gpio22.export()
        # self.gpio22.setDirection('out')

        # self.gpio23.export()
        # self.gpio23.setDirection('out')
        self.a.pinMode(self.IN1, self.a.OUTPUT)
        self.a.pinMode(self.IN2, self.a.OUTPUT)
        self.a.pinMode(self.ENA, self.a.OUTPUT)
        self.a.digitalWrite(self.ENA, self.a.HIGH)
        self.a.pinMode(self.IN3, self.a.OUTPUT)
        self.a.pinMode(self.IN4, self.a.OUTPUT)
        self.a.pinMode(self.ENB, self.a.OUTPUT)
        self.a.digitalWrite(self.ENB, self.a.HIGH)

    def offline(self):
        # self.gpio17.unexport()
        # self.gpio18.unexport()
        # self.gpio22.unexport()
        # self.gpio23.unexport()
        self.a.digitalWrite(self.ENA, self.a.LOW)
        self.a.digitalWrite(self.ENB, self.a.LOW)

    def stop(self):
        # self.gpio17.writeValue('0')
        # self.gpio18.writeValue('0')
        # self.gpio22.writeValue('0')
        # self.gpio23.writeValue('0')
        self.a.digitalWrite(self.IN1, self.a.LOW)
        self.a.digitalWrite(self.IN2, self.a.LOW)
        self.a.digitalWrite(self.IN3, self.a.LOW)
        self.a.digitalWrite(self.IN4, self.a.LOW)


    def drive_forward(self):
        # self.gpio18.writeValue('1')
        # self.gpio22.writeValue('1')
        self.a.digitalWrite(self.IN1, self.a.LOW)
        self.a.digitalWrite(self.IN2, self.a.HIGH)
        self.a.digitalWrite(self.IN3, self.a.HIGH)
        self.a.digitalWrite(self.IN4, self.a.LOW)

    def drive_backward(self):
        # self.gpio17.writeValue('1')
        # self.gpio23.writeValue('1')
        self.a.digitalWrite(self.IN1, self.a.HIGH)
        self.a.digitalWrite(self.IN2, self.a.LOW)
        self.a.digitalWrite(self.IN3, self.a.LOW)
        self.a.digitalWrite(self.IN4, self.a.HIGH)

    def steer_left(self):
        # self.gpio17.writeValue('1')
        # self.gpio22.writeValue('1')
        self.a.digitalWrite(self.IN1, self.a.HIGH)
        time.sleep(0.2)
        self.a.digitalWrite(self.IN1, self.a.LOW)
        # self.gpio17.writeValue('0')
        # self.gpio22.writeValue('0')

    def steer_right(self):
        # self.gpio18.writeValue('1')
        # self.gpio23.writeValue('1')
        self.a.digitalWrite(self.IN4, self.a.HIGH)
        time.sleep(0.2)
        self.a.digitalWrite(self.IN4, self.a.LOW)
        # self.gpio18.writeValue('0')
        # self.gpio23.writeValue('0')


def main():
    drv = DriveModule()
    drv.online()
    drv.drive_backward()
    time.sleep(2)
    drv.stop()
    drv.offline()
    # try:
    #     connection = SerialManager()
    #     a = ArduinoApi(connection=connection)
    # except:
    #     print('Failed to connect to Arduino!')

    # try:
    #     ENA = 10
    #     ENB = 5
    #     IN1 = 9
    #     IN2 = 8
    #     IN3 = 7
    #     IN4 = 6
    #     a.pinMode(IN1, a.OUTPUT)
    #     a.pinMode(IN2, a.OUTPUT)
    #     a.pinMode(ENA, a.OUTPUT)
    #     a.digitalWrite(ENA, a.HIGH)
    #     a.pinMode(IN3, a.OUTPUT)
    #     a.pinMode(IN4, a.OUTPUT)
    #     a.pinMode(ENB, a.OUTPUT)
    #     a.digitalWrite(ENB, a.HIGH)

    #     a.digitalWrite(IN3, a.LOW)
    #     a.digitalWrite(IN4, a.HIGH) # left wheel back
    #     a.digitalWrite(IN1, a.HIGH)
    #     a.digitalWrite(IN2, a.LOW) # right wheel backward
    #     time.sleep(0.5)
    #     a.digitalWrite(IN3, a.LOW)
    #     a.digitalWrite(IN4, a.LOW)
    #     a.digitalWrite(IN1, a.LOW)
    #     a.digitalWrite(IN2, a.LOW)

    #     a.digitalWrite(IN3, a.HIGH)
    #     a.digitalWrite(IN4, a.LOW) # left wheel forward
    #     a.digitalWrite(IN1, a.LOW)
    #     a.digitalWrite(IN2, a.HIGH) # right whelle forward
    #     time.sleep(0.5)
    #     a.digitalWrite(IN3, a.LOW)
    #     a.digitalWrite(IN4, a.LOW)
    #     a.digitalWrite(IN1, a.LOW)
    #     a.digitalWrite(IN2, a.LOW)

    #     time.sleep(0.5)
    #     a.digitalWrite(ENB, a.LOW)
    # except:
    #     a.digitalWrite(ENB, a.LOW)


if __name__ == '__main__':
    main()
