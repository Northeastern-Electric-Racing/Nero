from tkinter import Frame
from page import Page
from models.model import Model


class Reverse(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Reverse")
