import tkinter.font as tkFont
from tkinter import *
import numpy as np


class ThermometerProgress(Canvas):
    def __init__(self, parent, x0: int, y0: int, x1: int, y1: int, high=100, low=0):
        super().__init__(parent, background="black", highlightthickness=0, width=0, height=0)
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.height = y1 - y0
        self.width = x1 - x0
        self.high, self.low = high, low
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.start_ang, self.full_extent = 135, 360
        # draw static bar outline
        self.extent = 0
        self.radius = self.width/8
        self.starting_x = self.tx - self.radius
        self.ending_x = self.tx + self.radius
        self.starting_height = self.y1 - (self.radius * 2)
        self.rectangle_starting_x = np.cos(np.deg2rad(135)) * self.radius + self.tx
        self.rectangle_ending_x = np.cos(np.deg2rad(45)) * self.radius + self.tx
        self.rectangle_ending_y = self.y1 - self.radius
        self.custom_font = tkFont.Font(family="Helvetica", size=int(self.radius), weight='bold')

      #   self.rectangle = self.create_rectangle(self.rectangle_starting_x, self.y0,
      #                                          self.rectangle_ending_x, self.rectangle_ending_y, outline="red")
        self.filler = self.create_rectangle(self.rectangle_starting_x, self.rectangle_ending_y,
                                            self.rectangle_ending_x, self.rectangle_ending_y, outline="red", fill="red")

        self.left_line = self.create_line(self.rectangle_starting_x, self.y0,
                                          self.rectangle_starting_x, self.starting_height + self.starting_height/50, fill="white")
        self.right_line = self.create_line(self.rectangle_ending_x, self.y0,
                                           self.rectangle_ending_x, self.starting_height + self.starting_height/50, fill="white")

        self.bottom_arc = self.create_arc(self.starting_x, self.starting_height, self.ending_x, self.y1,
                                          start=self.start_ang, extent=270, outline="red", fill="red")
        self.bottom_arc_fill = self.create_arc(self.starting_x, self.starting_height, self.ending_x, self.y1,
                                          start=self.start_ang, extent=270, style="arc", outline="white")

        self.top_arc = self.create_arc(self.rectangle_starting_x, self.y0 - self.radius, self.rectangle_ending_x, self.y0 + self.radius,
                                       start=0, extent=180, style="arc", outline="white")
        
        # Create incremental lines for the thermometer
        for i in range(10):
            self.create_line(self.rectangle_starting_x, self.starting_height - (((self.height - self.radius * 2)/10) * i), self.rectangle_starting_x + self.radius/2, self.starting_height - (((self.height - self.radius * 2) /10) * i), fill="white")

    def set(self, value):
        self.value = value if isinstance(value, int) else 0
        x0, y0, x1, y1 = self.coords(self.filler)
        y0 = self.y1 - (self.y1 - self.y0) * (self.value / (self.low + self.high))
        self.coords(self.filler, x0, y0, x1, y1)
