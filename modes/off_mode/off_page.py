from tkinter import Frame
from modes.page import Page
from models.model import Model


class Off(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Off")
