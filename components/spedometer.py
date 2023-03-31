import tkinter.font as tkFont
from tkinter import *
import math


class Spedometer(Canvas):
    def __init__(self, parent, x0: int, y0: int, x1: int, y1: int, width=2, start_ang=0, full_extent=180):
        super().__init__(parent, background="black", highlightthickness=0, width=0, height=0)
        self.value_font = tkFont.Font(family="Helvetica", size=int(((y1 - y0) / 4) - 5), weight='bold')
        self.label_font = tkFont.Font(family="Helvetica", size=int(((y1 - y0) / 8) - 5), weight='bold')
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        self.extent = 0

        self.arc = self.create_arc(self.x0, self.y0, self.x1, self.y1,
                                   start=self.start_ang, extent=self.full_extent,
                                   width=self.width, style='arc', outline="white")

        self.value_label = self.create_text(self.tx, (self.y1 - self.y0) / 2, text=self.extent,
                                            font=self.value_font, fill="white")
        self.mph_label = self.create_text(self.tx, self.ty, text="MPH",
                                          font=self.label_font, fill="white")

        self.zero_label = self.create_text(self.x0 - (self.tx / 10), self.ty, text="0",
                                           font=self.label_font, fill="white")

        self.fifty_label = self.create_text(self.tx, self.y0 - (self.ty / 10), text="50",
                                            font=self.label_font, fill="white")

        self.hundred_label = self.create_text(self.x1 + (self.tx / 5), self.ty, text="100",
                                              font=self.label_font, fill="white")

        self.zero_tick = self.create_line(self.x0 - 10,  self.ty,
                                          self.x0 + 10,  self.ty, fill="white")

        self.fifty_tick = self.create_line(self.tx, self.y0 - 10, self.tx, self.y0 + 10, fill="white")

        self.hundred_tick = self.create_line(self.x1 + 10,  self.ty, self.x1 - 10,
                                             self.ty, fill="white")

        self.value_tick = self.create_line(self.x0 - 10,  self.ty,
                                           self.x0 + 10,  self.ty, fill="red")

    def set(self, value):
        self.extent = value if isinstance(value, int) else 0
        # Update percentage value displayed.
        label = str(value)
        self.itemconfigure(self.value_label, text=label)

        x = self.tx + (self.tx/2 + 70) * math.cos((value / 100 * 180 + 180) * math.pi / 180)
        y = self.ty + (self.ty/2 + 70) * math.sin((value / 100 * 180 + 180) * math.pi / 180)
        tick_x = self.tx + (self.tx/2 + 100) * math.cos((value / 100 * 180 + 180) * math.pi / 180)
        tick_y = self.ty + (self.ty/2 + 100) * math.sin((value / 100 * 180 + 180) * math.pi / 180)
        self.coords(self.value_tick, x, y, tick_x, tick_y)
