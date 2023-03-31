from tkinter import Frame
from modes.page import Page
from models.model import Model
from components.spedometer import Spedometer


class Efficiency(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Efficiency")
