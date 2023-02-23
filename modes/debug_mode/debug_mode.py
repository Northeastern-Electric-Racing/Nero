from tkinter import Frame
from modes.debug_mode.debug_plot_page import DebugPlot
from modes.debug_mode.debug_table_page import DebugTable
from modes.mode import Mode
from models.model import Model


class DebugMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Debug Mode", [DebugTable, DebugPlot])
