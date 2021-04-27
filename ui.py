# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
# Ported to RGB Display by Melissa LeBlanc-Williams
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
"""
This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from adafruit_debouncer import Debouncer
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

class UI(object):
    """ Handle display and buttons on footswitch Raspberry Pi"""
    
    def __init__(self,
                 onButtonA = None, onButtonB = None,
                 onButtonL = None, onButtonR = None,
                 onButtonU = None, onButtonC = None, onButtonD = None):
        # Create the display
        cs_pin = DigitalInOut(board.CE0)
        dc_pin = DigitalInOut(board.D25)
        reset_pin = DigitalInOut(board.D24)
        BAUDRATE = 24000000

        spi = board.SPI()
        self.disp = st7789.ST7789(
            spi,
            height=240,
            y_offset=80,
            rotation=180,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )

        # Input pins:
        self.button_A_pin = DigitalInOut(board.D5)
        self.button_A_pin.direction = Direction.INPUT
        self.button_A = Debouncer(self.button_A_pin)
        self.onButtonA = onButtonA
        
        self.button_B_pin = DigitalInOut(board.D6)
        self.button_B_pin.direction = Direction.INPUT
        self.button_B = Debouncer(self.button_B_pin)
        self.onButtonB = onButtonB

        self.button_L_pin = DigitalInOut(board.D27)
        self.button_L_pin.direction = Direction.INPUT
        self.button_L = Debouncer(self.button_L_pin)
        self.onButtonL = onButtonL

        self.button_R_pin = DigitalInOut(board.D23)
        self.button_R_pin.direction = Direction.INPUT
        self.button_R = Debouncer(self.button_R_pin)
        self.onButtonR = onButtonR

        self.button_U_pin = DigitalInOut(board.D17)
        self.button_U_pin.direction = Direction.INPUT
        self.button_U = Debouncer(self.button_U_pin)
        self.onButtonU = onButtonU

        self.button_D_pin = DigitalInOut(board.D22)
        self.button_D_pin.direction = Direction.INPUT
        self.button_D = Debouncer(self.button_D_pin)
        self.onButtonD = onButtonD

        self.button_C_pin = DigitalInOut(board.D4)
        self.button_C_pin.direction = Direction.INPUT
        self.button_C = Debouncer(self.button_C_pin)
        self.onButtonC = onButtonC

        self.udlr_fill = "#00FF00"
        self.udlr_outline = "#00FFFF"
        self.button_fill = "#FF00FF"
        self.button_outline = "#FFFFFF"

        # Turn on the Backlight
        backlight = DigitalInOut(board.D26)
        backlight.switch_to_output()
        backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        width = self.disp.width
        height = self.disp.height
        self.image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Clear display.
        self.draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
        self.disp.image(self.image)

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)

        self.fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        
    def loop(self):
        while True:
            self.button_U.update()
            up_fill = 0
            if not self.button_U.value:  # up pressed
                up_fill = self.udlr_fill
            self.draw.polygon(
                [(40, 40), (60, 4), (80, 40)], outline=self.udlr_outline, fill=up_fill
            )  # Up
            if self.button_U.fell: # up pressed since last update
                if self.onButtonU is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonU()

            self.button_D.update()
            down_fill = 0
            if not self.button_D.value:  # down pressed
                down_fill = self.udlr_fill
            self.draw.polygon(
                [(60, 120), (80, 84), (40, 84)], outline=self.udlr_outline, fill=down_fill
            )  # down
            if self.button_D.fell: # D pressed since last update
                if self.onButtonD is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonD()

            self.button_L.update()
            left_fill = 0
            if not self.button_L.value:  # left pressed
                left_fill = self.udlr_fill
            self.draw.polygon(
                [(0, 60), (36, 42), (36, 81)], outline=self.udlr_outline, fill=left_fill
            )  # left
            if self.button_L.fell: # L pressed since last update
                if self.onButtonL is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonL()

            self.button_R.update()
            right_fill = 0
            if not self.button_R.value:  # right pressed
                right_fill = self.udlr_fill
            self.draw.polygon(
                [(120, 60), (84, 42), (84, 82)], outline=self.udlr_outline, fill=right_fill
            )  # right
            if self.button_R.fell: # R pressed since last update
                if self.onButtonR is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonR()

            self.button_C.update()
            center_fill = 0
            if not self.button_C.value:  # center pressed
                center_fill = self.button_fill
            self.draw.rectangle((40, 44, 80, 80), outline=self.button_outline, fill=center_fill)  # center
            if self.button_C.fell: # C pressed since last update
                if self.onButtonC is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonC()

            self.button_A.update()
            A_fill = 0
            if not self.button_A.value:  # A currently pressed
                A_fill = self.button_fill
            self.draw.ellipse((140, 80, 180, 120), outline=self.button_outline, fill=A_fill)  # A button
            if self.button_A.fell: # A pressed since last update
                if self.onButtonA is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonA()
            
            self.button_B.update()
            B_fill = 0
            if not self.button_B.value:  # B currently pressed
                B_fill = self.button_fill
            self.draw.ellipse((190, 40, 230, 80), outline=self.button_outline, fill=B_fill)  # B button
            if self.button_B.fell: # B pressed since last update
                if self.onButtonB is not None:
                    # Display the Image
                    self.disp.image(self.image)
                    self.onButtonB()

            # make a random color and print text
            #rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            #self.draw.text((20, 150), "footswitch", font=self.fnt, fill=rcolor)
            #rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            #self.draw.text((20, 180), "Hello World", font=self.fnt, fill=rcolor)
            rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            self.draw.text((20, 210), "footswitch", font=self.fnt, fill=rcolor)
            
            # Display the Image
            self.disp.image(self.image)

            time.sleep(0.01)


