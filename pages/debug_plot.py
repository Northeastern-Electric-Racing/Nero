from tkinter import Frame
from pages.page import Page
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from typing import Dict, List


class Debug_Plot(Page):
    def __init__(self, controller, parent):
        super().__init__(parent, controller, "Debug Plot")
        self.data: Dict[int, List[float]] = controller.pinned_data

    def create_view(self):
        # the frame that will hold the figure
        frame = Frame(self)
        frame.grid(row=0, column=0, sticky="s")

        # the figure that will contain the plot
        # the figure that will contain the plot
        self.fig = Figure(figsize=(11, 6), dpi=100)
        self.fig.suptitle("Debug Plot", fontsize=16)
        # adding the subplot
        self.plot1 = self.fig.add_subplot(111)
        

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="s")

        self.update_figure()
    
    def update_figure(self):
        self.plot1.clear()
        for id in self.data:
            y = self.data[id]
            # plotting the graph
            self.plot1.plot(y)
        self.canvas.draw()
        self.after(100, self.update_figure)
