from tkinter import Frame
from modes.page import Page
from models.model import Model
from modes.efficiency_mode.home import Home


class Off(Home):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model)
        self.name = "Off"
