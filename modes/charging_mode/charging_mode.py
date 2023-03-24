from modes.mode import Mode
from tkinter import Frame
from modes.charging_mode.charging_page import Charging
from models.model import Model


class ChargingMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Charging Mode", [Charging])
