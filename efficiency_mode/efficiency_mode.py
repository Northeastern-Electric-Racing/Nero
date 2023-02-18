from mode import Mode
from tkinter import Frame
from efficiency_mode.home import Home
from models.model import Model


class EfficiencyMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Efficiency Mode", [Home])
