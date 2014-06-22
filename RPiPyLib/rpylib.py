__author__ = 'develru'

from time import sleep


class GPIOrtx(object):

    def __init__(self, io='4'):
            self._gpioNum = io
            # state 0 is not initialized
            self._state = 0

    def export(self):
        try:
            gpioFileExport = open('/sys/class/gpio/export', 'w')
            gpioFileExport.write(self._gpioNum)
            gpioFileExport.close
            self._state = 1
        except IOError:
            print(('OPERATION FAILED: Unable to export GPIO{}!'.format(
                self._gpioNum)))

    def unexport(self):
        try:
            gpioFileUnexport = open('/sys/class/gpio/unexport', 'w')
            gpioFileUnexport.write(self._gpioNum)
            gpioFileUnexport.close
            self._state = 0
        except IOError:
            print(('OPERATION FAILED: Unable to unexport GPIO{}!'.format(
                self._gpioNum)))

    def setDirection(self, direction):
        try:
            gpioFile = open('/sys/class/gpio/gpio' + self._gpioNum +
                            '/direction', 'w')
            gpioFile.write(direction)
            gpioFile.close()
        except IOError:
            print((
                'OPERATION FAILED: Unable to set direction for GPIO{}!'.format(
                    self._gpioNum)))

    def writeValue(self, value):
        try:
            gpioFile = open('/sys/class/gpio/gpio' + self._gpioNum + '/value',
                            'w')
            gpioFile.write(value)
            gpioFile.close
        except IOError:
            print(('OPERATION FAILED: Unable to write value to GPIO{}!'.format(
                self._gpioNum)))

    def setup(self, direction):
        if self._state == 0:
            self.export()
        self.setDirection(direction)


class LCD16x2(object):

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display
    # on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags
    # for
    # display/cursor
    # shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00

    # flags
    # for
    # display/cursor
    # shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags
    # for
    # function
    # set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self, pinRS='25', pinE='24', pinsDB=['23', '17', '27', '22']):
        self._gpioRS = GPIOrtx(pinRS)
        self._gpioE = GPIOrtx(pinE)
        self._gpios = []
        for gpio in pinsDB:
            self._gpios.append(GPIOrtx(gpio))

        self._displayControl = (self.LCD_DISPLAYON | self.LCD_CURSOROFF |
                               self.LCD_BLINKOFF)

        self._displayFunction = (self.LCD_4BITMODE | self.LCD_1LINE |
                                 self.LCD_5x8DOTS)
        self._displayFunction |= self.LCD_2LINE

        self._displayMode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT

    def __enter__(self):
        self._gpioRS.setup('out')
        self._gpioE.setup('out')
        for gpio in self._gpios:
            gpio.setup('out')

        self.write4bits(0x33)
        self.write4bits(0x32)
        self.write4bits(0x28)
        self.write4bits(0x0C)
        self.write4bits(0x06)

        self.write4bits(self.LCD_ENTRYMODESET | self._displayMode)

        self.clear()

        return self

    def __exit__(self, typ, value, traceback):
        self._gpioRS.unexport()
        self._gpioE.unexport()
        for gpio in self._gpios:
            gpio.unexport()

    def begin(self, cols, lines):
        if lines > 1:
            self._numlines = lines
            self._displayFunction |= self.LCD_2LINE
            self._currline = 0

    def home(self):
        self.write4bits(self.LCD_RETURNHOME)
        sleep(self.convertSec(3000))

    def setCursor(self, col, row):
        self._rowOffset = [0x00, 0x40, 0x14, 0x54]
        if row > self._numlines:
            row = self._numlines - 1

        self.write4bits(self.LCD_SETDDRAMADDR | (col + self._rowOffset[row]))

    def noDisplay(self):
        self._displayControl &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self._displayControl)

    def display(self):
        self._displayControl |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self._displayControl)

    def noCursor(self):
        self._displayControl &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self._displayControl)

    def cursor(self):
        self._displayControl |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self._displayControl)

    def noBlink(self):
        self._displayControl &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self._displayControl)

    def scrollDisplayLeft(self):
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE |
                        self.LCD_MOVELEFT)

    def scrollDisplayRight(self):
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE |
                        self.LCD_MOVERIGHT)

    def leftToRight(self):
        self._displayMode |= self.LCD_ENTRYRIGHT
        self.write4bits(self.LCD_ENTRYMODESET | self._displayMode)

    def autoscroll(self):
        self._displayMode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self._displayMode)

    def leftToLeft(self):
        self._displayMode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self._displayMode)

    def write4bits(self, bits, charMode='0'):
        """ Sent command to the LCD """
        sleep(self.convertSec(1000))

        bits = bin(bits)[2:].zfill(8)
        self._gpioRS.writeValue(charMode)

        for gpio in self._gpios:
            gpio.writeValue('0')

        for i in range(4):
            if bits[i] == '1':
                self._gpios[::-1][i].writeValue('1')

        self.pulseEnable()

        for gpio in self._gpios:
            gpio.writeValue('0')

        for i in range(4, 8):
            if bits[i] == '1':
                self._gpios[::-1][i - 4].writeValue('1')

        self.pulseEnable()

    def convertSec(self, microSec):
        return microSec / float(1000000)

    def pulseEnable(self):
        self._gpioE.writeValue('0')
        sleep(self.convertSec(1))
        self._gpioE.writeValue('1')
        sleep(self.convertSec(1))
        self._gpioE.writeValue('0')
        sleep(self.convertSec(1))

    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY)
        sleep(self.convertSec(3000))

    def message(self, text):
        for char in text:
            if char == '\n':
                self.write4bits(0xC0)
            else:
                self.write4bits(ord(char), '1')