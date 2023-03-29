from tkinter import Frame
from modes.page import Page
from models.model import Model
from modes.home import Home


class Speed(Home):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model)
        self.name = "Speed"
