import time, random
from machine import Pin, SPI
import vga2_bold_16x32 as font
import st7789

class Bavard:

    def __init__(self):
        self.tft = st7789.ST7789(
            SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19)),
            135,
            240,
            reset=Pin(23, Pin.OUT),
            cs=Pin(5, Pin.OUT),
            dc=Pin(16, Pin.OUT),
            backlight=Pin(4, Pin.OUT),
            rotation=1
        )

        self.tft.text(font,"Bavard Init !",0,0)


        self.btn_up_pin = 0
        self.btn_down_pin = 35
        self.button_up = Pin(
            self.btn_up_pin, 
            Pin.IN, 
            Pin.PULL_UP
        )
        self.button_down = Pin(
            self.btn_down_pin, 
            Pin.IN, 
            Pin.PULL_UP
        )


        self.page_now = 1
        self.page_max = 5
        self.page_min = 1

        self.tft.text(font,"Ready...",0,0)

    def page_change(self, btn):
        first = btn.value()
        time.sleep(0.01)
        second = btn.value()
        if first and not second:
            if btn == self.button_up:
                self.page_now += 1
            if btn == self.button_down:
                self.page_now -= 1
            
            if self.page_now > self.page_max:
                self.page_now = self.page_max
            if self.page_now < self.page_min:
                self.page_now = self.page_min

            print("change page")
            print("page_now", self.page_now)

            self.tft.fill(st7789.BLACK)
            self.tft.text(font,"Page:",0,0)
            self.tft.text(font,str(self.page_now),0,35)

    def run(self):
        while True:
            self.page_change(self.button_up)
            self.page_change(self.button_down)

Bavard().run()