from tkinter import Frame
from modes.page import Page
from models.model import Model
from components.gforce_graph import GForceGraph


class Efficiency(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Efficiency")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.gforce_graph = GForceGraph(self)
        self.gforce_graph.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.gforce_graph.set(2, 4)
