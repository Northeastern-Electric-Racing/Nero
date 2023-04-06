from tkinter import Frame
from modes.page import Page
from models.model import Model
from modes.home import Home


class PitLane(Home):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model)
        self.name = "Pit Lane"
