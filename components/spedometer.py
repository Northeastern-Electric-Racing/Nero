from tkinter import *
from customtkinter import CTkFont
import math
import numpy as np


class Spedometer(Canvas):
    def __init__(self, parent, x0: int, y0: int, width: int, height: int, start_ang=0, full_extent=180):
        super().__init__(parent, background="black", highlightthickness=0, width=0, height=0)

        # define the spedometer parameters
        self.speedometer_center_x = width / 2
        self.speedometer_center_y = height / 2
        self.speedometer_radius = 0.4 * min(width, height)
        self.speedometer_width = 0.08 * min(width, height)
        self.speedometer_start_angle = 0
        self.speedometer_end_angle = 180
        self.speedometer_outline_color = 'white'
        self.speedometer_outline_width = 2
        self.font_size = int(np.abs(0.2 * min(width, height)))

        # create the spedometer background
        self.create_arc(
            self.speedometer_center_x - self.speedometer_radius,
            self.speedometer_center_y - self.speedometer_radius,
            self.speedometer_center_x + self.speedometer_radius,
            self.speedometer_center_y + self.speedometer_radius,
            start=self.speedometer_start_angle,
            extent=self.speedometer_end_angle - self.speedometer_start_angle,
            style=ARC,
            outline=self.speedometer_outline_color,
            width=self.speedometer_outline_width,
        )

        # create the tick marks
        self.tick_length = 0.35 * min(width, height)
        self.tick_width = self.speedometer_width / 10
        for i in range(0, 101, 10):
            angle = self.speedometer_start_angle + (i / 100) * (self.speedometer_end_angle - self.speedometer_start_angle)
            x = self.speedometer_center_x + self.speedometer_radius * math.cos(angle * math.pi / 180)
            y = self.speedometer_center_y - self.speedometer_radius * math.sin(angle * math.pi / 180)
            tick_x = self.speedometer_center_x + self.tick_length * math.cos(angle * math.pi / 180)
            tick_y = self.speedometer_center_y - self.tick_length * math.sin(angle * math.pi / 180)
            self.create_line(x, y, tick_x, tick_y, width=self.tick_width)

        # create the mph label
        self.mph_value = self.create_text(self.speedometer_center_x, self.speedometer_center_y * .7, text="N/A", fill="white", font=CTkFont("Helevetica", size=self.font_size, weight="bold"))
        self.mph_label = self.create_text(self.speedometer_center_x, self.speedometer_center_y, text="mph", fill="white", font=CTkFont("Helevetica", size=int(self.font_size * 0.6), weight="bold"))

        # function to update the tick mark based on a speed value
    def set_speed(self, speed):
        self.delete("speed_marker")
        angle = self.speedometer_start_angle + (speed / 100) * (self.speedometer_start_angle - self.speedometer_end_angle) + 180
        x = self.speedometer_center_x + self.speedometer_radius * math.cos(angle * math.pi / 180)
        y = self.speedometer_center_y - self.speedometer_radius * math.sin(angle * math.pi / 180)
        tick_x = self.speedometer_center_x + self.tick_length * math.cos(angle * math.pi / 180)
        tick_y = self.speedometer_center_y - self.tick_length * math.sin(angle * math.pi / 180)
        self.create_line(x, y, tick_x, tick_y, width=self.tick_width, tags="speed_marker", fill="red")

        # update the mph label when the speed is changed

    def set(self, speed):
        speed_int = speed if isinstance(speed, int) else 0
        self.set_speed(speed_int)
        self.itemconfigure(self.mph_value, text=str(speed))
