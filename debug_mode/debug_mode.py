from tkinter import Frame
from typing import List, Dict
from debug_mode.debug_plot_page import DebugPlot
from debug_mode.debug_table_page import DebugTable
from mode import Mode
from models.model import Model


class DebugMode(Mode):
    def __init__(self, parent: Frame, controller: Frame, model: Model):
        super().__init__(parent, controller, model, "Debug Mode", [DebugTable, DebugPlot])
        # the ids and values that are pinned by the table and will be displayed by the plot
