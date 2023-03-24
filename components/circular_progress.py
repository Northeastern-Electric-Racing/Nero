import tkinter.font as tkFont
from tkinter import *


class CircularProgressbar(object):
    def __init__(self, canvas: Canvas, x0: int, y0: int, x1: int, y1: int, width=2, start_ang=0, full_extent=360.):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1+x0) / 2, (y1+y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        self.extent = 0
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc')
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=self.extent,
                                                font=self.custom_font)

    def set(self, value):
        self.extent = value if isinstance(value, int) else 0
        self.canvas.itemconfigure(self.arc_id, extent=((self.extent / 100) * self.full_extent))
        # Update percentage value displayed.
        self.percent = value if isinstance(value, int) else "N/A"
        self.canvas.itemconfigure(self.label_id, text=self.percent)
