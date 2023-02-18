from mode import Mode
from tkinter import Frame
from reverse_mode.reverse_page import Reverse
from models.model import Model


class ReverseMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Reverse Mode", [Reverse])
