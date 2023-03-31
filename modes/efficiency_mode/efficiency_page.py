from tkinter import Frame
from modes.page import Page
from models.model import Model
from components.spedometer import Spedometer


class Efficiency(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Efficiency")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.spedometer = Spedometer(self, 100, 100, 500, 500)
        self.spedometer.set(40)
        self.spedometer.grid(row=0, column=0, sticky="nsew")
