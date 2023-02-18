from mode import Mode
from tkinter import Frame
from off_mode.off_page import Off
from models.model import Model


class OffMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Off Mode", [Off])
