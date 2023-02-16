from tkinter import Frame
from pages.page import Page

class Off(Page):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller, "Off")

