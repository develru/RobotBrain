__author__ = 'develru'

from RPiPyLib import rpilib
import time


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