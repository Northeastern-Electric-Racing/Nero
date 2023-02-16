from tkinter import Frame
from pages.page import Page

class Debug_Plot(Page):
    def __init__(self, controller, parent):
        super().__init__(parent, controller, "Debug Plot")
