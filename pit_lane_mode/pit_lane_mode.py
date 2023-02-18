from mode import Mode
from tkinter import Frame
from pit_lane_mode.pit_lane_page import PitLane
from models.model import Model


class PitLaneMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Pit Lane Mode", [PitLane])
