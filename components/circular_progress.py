import tkinter.font as tkFont
from tkinter import *


class CircularProgressbar(Canvas):
    def __init__(self, parent, x0: int, y0: int, x1: int, y1: int, width=2, start_ang=0, full_extent=360.):
        super().__init__(parent, background="black", highlightthickness=0, width=0, height=0)
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        self.extent = 0

        self.oval_id1 = self.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2, outline="white")
        self.oval_id2 = self.create_oval(self.x0+w2, self.y0+w2,
                                         self.x1-w2, self.y1-w2, outline="white")
        self.arc_id = self.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                      width=self.width, style='arc', outline="white")
        self.label_id = self.create_text(self.tx, self.ty, text=self.extent,
                                                font=self.custom_font, fill="black")

    def set(self, value):
        self.extent = value if isinstance(value, int) else 0
        self.itemconfigure(self.arc_id, extent=((self.extent / 100) * self.full_extent))
        # Update percentage value displayed.
        percent = value
        self.itemconfigure(self.label_id, text=percent)

        color = "red"
        if self.extent > 80:
            color = "green"
        elif self.extent > 50:
            color = "yellow"
        elif self.extent > 20:
            color = "orange"
        self.itemconfigure(self.oval_id2, fill=color)
         
