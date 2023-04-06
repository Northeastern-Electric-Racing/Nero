from modes.mode import Mode
from tkinter import Frame
from modes.efficiency_mode.efficiency_page import Efficiency
from models.model import Model
from modes.home import Home

class EfficiencyMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Efficiency Mode", [Efficiency])
