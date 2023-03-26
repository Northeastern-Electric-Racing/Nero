from tkinter import Frame
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict
from models.model import Model
from modes.debug_mode.debug_utils import DebugPlotValue
from modes.page import Page
import numpy as np


class DebugPlotKey(Frame):
    def __init__(self, key_value: DebugPlotValue, parent: Frame):
        super().__init__(parent, bg="black", height=95, width=296, highlightbackground='gray', highlightthickness=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.name_frame = Frame(self, bg="black", height=30, width=300)
        self.name_label = customtkinter.CTkLabel(self.name_frame, text=key_value.name, font=("Lato", 25, "bold"))
        self.name_frame.grid(row=0, column=0, sticky="nsew")
        self.name_frame.grid_propagate(False)
        self.name_label.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self, bg="black", height=65, width=300)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_propagate(False)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.current_value_frame = Frame(self.bottom_frame, bg="black", height=65, width=200)
        self.current_value_label = customtkinter.CTkLabel(self.current_value_frame,
                                                          text=key_value.data[len(key_value.data) - 1], font=("Lato", 55))
        self.current_value_frame.grid(row=0, column=0, sticky="nsew")
        self.current_value_frame.grid_propagate(False)
        self.current_value_label.grid(row=0, column=0, padx=5)

        self.right_frame = Frame(self.bottom_frame, bg="black", height=65, width=100)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_propagate(False)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.unit_frame = Frame(self.right_frame, bg="black", height=30, width=100)
        self.unit_label = customtkinter.CTkLabel(self.unit_frame, text=key_value.unit, font=("Lato", 25, "bold"))
        self.unit_frame.grid(row=0, column=0, sticky="nsew")
        self.unit_frame.grid_propagate(False)
        self.unit_label.grid(row=0, column=0, sticky="nsew")

        self.multiplier_frame = Frame(self.right_frame, bg="black", height=35, width=100)
        self.multiplier_label = customtkinter.CTkLabel(self.multiplier_frame, text="1x", font=("Lato", 30, "bold"))
        self.multiplier_frame.grid(row=1, column=0, sticky="nsew")
        self.multiplier_frame.grid_propagate(False)
        self.multiplier_label.grid(row=0, column=0, sticky="nsew")


class DebugPlot(Page):
    def __init__(self, parent: Frame, model: Model):
        super().__init__(parent, model, "Debug Plot")
        self.time_presets = [30, 60, 120, 300, 600]
        self.current_time_index = 0
        self.current_time = self.time_presets[self.current_time_index]
        self.data: Dict[int, DebugPlotValue] = self.model.pinned_data[self.current_time_index]
        self.colors = {0: "red", 1: "green", 2: "blue", 3: "yellow", 4: "orange", 5: "purple"}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # the frame that will hold the keys
        self.key_frame = Frame(self, width=300, height=570, bg="black")
        self.key_frame.grid_propagate(False)
        self.key_frame.grid_rowconfigure(6, weight=1)
        self.key_frame.grid_columnconfigure(0, weight=1)
        self.key_frame.grid(row=0, column=0, sticky="sw")

        self.key_frames = []
        # Create the keys
        for i in range(6):
            self.key_frames.append(DebugPlotKey(DebugPlotValue("", "", [""]), self.key_frame))
            self.key_frames[i].grid(row=i, column=0, sticky="s")

        # the frame that will hold the figure
        figure_frame = Frame(self, background="blue", height=570, width=724)
        figure_frame.grid(row=0, column=1, sticky="s")

        # the figure that will contain the plot
        self.fig, self.ax = plt.subplots(facecolor="black", figsize=(7.24/2, 5.70/2), dpi=100)
        self.ax.set_facecolor('black')
        self.fig.suptitle('Debug Plot', color='white')
        self.ax.set_xlabel('Time [s]', color='white')
        self.ax.tick_params(labelcolor='white')

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=figure_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="s")

    def enter_button_pressed(self):
        self.current_time_index = (self.current_time_index +
                                   1) if self.current_time_index < len(self.time_presets) - 1 else 0
        self.current_time = self.time_presets[self.current_time_index]
        self.data = self.model.pinned_data[self.current_time_index]

    def update(self):
        self.ax.clear()
        i = 0
        for id in self.data:
            # creating key frame
            self.key_frames[i].name_label.configure(text=self.data[id].name)
            self.key_frames[i].unit_label.configure(text=self.data[id].unit)
            self.key_frames[i].current_value_label.configure(
                text=self.data[id].data[0], text_color=self.colors[i])

            # plotting the graph
            y = np.array(self.data[id].data)
            self.ax.plot(y, color=self.colors[i])
            self.ax.xaxis.set_major_formatter(lambda x, pos: str(int(x / 600 * self.current_time)) + "s")
            i += 1
        self.ax.invert_xaxis()
        for j in range(i, 5):
            self.key_frames[j].name_label.configure(text="")
            self.key_frames[j].unit_label.configure(text="")
            self.key_frames[j].current_value_label.configure(text="")
        self.canvas.draw()
