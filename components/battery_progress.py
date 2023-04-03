import tkinter.font as tkFont
from tkinter import *


class BatteryProgress(Canvas):
    def __init__(self, parent, x0: int, y0: int, x1: int, y1: int):
        super().__init__(parent, background="black", highlightthickness=0, width=0, height=0)
        self.custom_font = tkFont.Font(family="Helvetica", size=int(((x1 - x0) / 2) - 5), weight='bold')
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2

        self.extent = 0
        self.rectangle_1 = self.create_rectangle(self.x0, self.y0 ,
                                         self.x1, self.y1, outline="white")
        self.rectangle_top = self.create_rectangle(self.tx - (self.tx - x0) /2, self.y0-self.ty/20,
                                                    self.tx + (self.tx - x0) /2, self.y0, outline="white")
        self.filling_rectangle = self.create_rectangle(self.x0, self.y1, self.x1, self.y1, fill="yellow")
        self.label_id = self.create_text(self.tx, self.ty, text=self.extent,
                                         font=self.custom_font, fill="white")

    def set(self, value):
        self.extent = value if isinstance(value, int) else 0
        x0, y0, x1, y1 = self.coords(self.filling_rectangle)
        y0 = self.y1 - (self.y1 - self.y0) * (self.extent / 100)
        self.coords(self.filling_rectangle, x0, y0, x1, y1)
        # Update percentage value displayed.
        percent = str(value) + "%"
        self.itemconfigure(self.label_id, text=percent)

        color = "red"
        if self.extent > 60:
            color = "green"
        elif self.extent > 20:
            color = "orange"
        if self.extent >= 100:
            self.itemconfigure(self.label_id, font=tkFont.Font(family="Helvetica", size=int(((self.x1 - self.x0) / 3)), weight='bold'))
        self.itemconfigure(self.rectangle_1, outline=color)
        self.itemconfigure(self.rectangle_top, outline=color)
        self.itemconfigure(self.label_id, fill=color)

