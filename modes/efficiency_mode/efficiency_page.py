from tkinter import Frame
from modes.page import Page
from models.model import Model
from components.thermometer_progress import ThermometerProgress


class Efficiency(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Efficiency")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)