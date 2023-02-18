from tkinter import Frame
from page import Page
from models.model import Model


class Speed(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Speed")
