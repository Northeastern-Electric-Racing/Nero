from mode import Mode
from tkinter import Frame
from speed_mode.speed_page import Speed
from models.model import Model


class SpeedMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Speed Mode", [Speed])
