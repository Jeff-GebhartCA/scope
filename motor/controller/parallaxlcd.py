import machine
import gc
from time import sleep

gc.enable()

LCD_UART = 2
LCD_BAUDRATE = 19200
LCD_BOUNCE = 0.05
LCD_DISPLAY_OFF = '\x15'
LCD_DISPLAY_ON = '\x18'
LCD_DISPLAY_CLEAR = '\x0C'
LCD_CARRIAGE_RETURN = '\x0D'
LCD_BACKLIGHT_ON = '\x11'
LCD_BACKLIGHT_OFF = '\x12'
LCD_CURSOR_LINE_FEED = '\x0D'
LCD_CURSOR_LEFT = '\x08'
LCD_CURSOR_RIGHT = '\x09'
LCD_CURSOR_UNDERLINE = '\x18'
LCD_CURSOR_BLOCK = '\x17'
LCD_CURSOR_OFF = '\x16'
LCD_CURSOR_ON = '\x17'
LCD_CURSOR_CHR_BLINK = '\x19'
LCD_ROW = 0
LCD_ROW_MIN = 0
LCD_ROW_MAX = 4
LCD_COL = 0
LCD_COL_MIN = 0
LCD_COL_MAX = 20

eraseOLD = ' '
eraseROW = LCD_ROW_MAX
eraseCOL = LCD_COL_MAX

class CharLCD:
    def __init__(self):
        self.connection = machine.UART(LCD_UART, baudrate=LCD_BAUDRATE)
        sleep(LCD_BOUNCE)
        self.write(LCD_DISPLAY_ON)
        self.clear()
        self.write(LCD_BACKLIGHT_ON)

    def write(self, text):
        self.connection.write(text)
        sleep(LCD_BOUNCE)

    def clear(self):
        self.write(LCD_DISPLAY_CLEAR)

    def newLine(self):
        self.write(LCD_CARRIAGE_RETURN)

    def cursorUnderline(self):
        self.write(LCD_CURSOR_UNDERLINE)

    def noCursorBlock(self):
        self.write(LCD_CURSOR_BLOCK)

    def cursorOff(self):
        self.write(LCD_CURSOR_OFF)

    def cursorOn(self):
        self.write(LCD_CURSOR_ON)

    def cursorBlockBlink(self):
        self.write(LCD_CURSOR_CHR_BLINK)

    def cursorLeft(self):
        self.write(LCD_CURSOR_LEFT)

    def cursorRight(self):
        self.write(LCD_CURSOR_RIGHT)

    def cursorLineFeed(self):
        self.write(LCD_CURSOR_LINE_FEED)

    def backlightOn(self):
        self.write(LCD_BACKLIGHT_ON)

    def backlightOff(self):
        self.write(LCD_BACKLIGHT_OFF)

    def print(self, message, row=0, column=0):
        self.cursorPos(row, column)
        self.write(message)

    def printCenter(self, message):
        global eraseROW
        global eraseCOL
        global eraseOLD

        self.cursorPos(eraseROW, eraseCOL)
        self.write(eraseOLD)

        messageCenterROW = LCD_ROW_MAX//2 - 1
        messageCenterCOL = LCD_COL_MAX//2 - len(message)//2 - 1

        self.cursorPos(messageCenterROW, messageCenterCOL)
        self.write(message)

        eraseOLD = ' ' * len(message)
        eraseROW = messageCenterROW
        eraseCOL = messageCenterCOL
        
    def move(self, message, times, dir = 'R'):
        #self.print(message)
        erase = ' ' * len(message)
        times = times -1

        def cursor_back():
            for i in range(len(message)):
               self.cursorLeft()
            


        for i in range(times):
            self.print(message)
            cursor_back()
            self.write(erase)
            cursor_back()

            #self.cursorRight()

            if dir in ['l', 'L']:
                self.cursorLeft()
                self.cursorLeft()
 
            self.write(message)

        
    def cursorPos(self, row, column):
        row = max(min(row, LCD_ROW_MAX), LCD_ROW_MIN)
        column = max(min(column, LCD_COL_MAX), LCD_COL_MIN)
        self.write(chr(0x80 + row * LCD_COL_MAX + column))
