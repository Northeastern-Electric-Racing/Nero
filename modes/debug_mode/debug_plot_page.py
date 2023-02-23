from tkinter import Frame
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from typing import Dict
from models.model import Model
from modes.debug_mode.debug_utils import DebugPlotValue
from modes.page import Page


class DebugPlotKey(Frame):
    def __init__(self, key_value: DebugPlotValue, parent: Frame):
        super().__init__(parent, bg="black", height=115, width=296, highlightbackground='gray', highlightthickness=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)

        self.name_frame = Frame(self, bg="black", height=30, width=150)
        self.name_label = customtkinter.CTkLabel(self.name_frame, text=key_value.name, font=("Lato", 15, "bold"))
        self.name_frame.grid(row=0, column=0, sticky="nsew")
        self.name_frame.grid_propagate(False)
        self.name_label.grid(row=0, column=0, sticky="nsew")

        self.current_value_frame = Frame(self, bg="black", height=80, width=150)
        self.current_value_label = customtkinter.CTkLabel(self.current_value_frame,
                                                          text=key_value.data[len(key_value.data) - 1], font=("Lato", 60))
        self.current_value_frame.grid(row=1, column=0, sticky="w")
        self.current_value_frame.grid_propagate(False)
        self.current_value_label.grid(row=0, column=0, sticky="w")

        self.right_frame = Frame(self, bg="black", height=80, width=150)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_propagate(False)
        self.right_frame.grid(row=1, column=1, sticky="nsew")

        self.unit_frame = Frame(self.right_frame, bg="black", height=30, width=150)
        self.unit_label = customtkinter.CTkLabel(self.unit_frame, text=key_value.unit, font=("Lato", 25, "bold"))
        self.unit_frame.grid(row=0, column=0, sticky="nsew")
        self.unit_frame.grid_propagate(False)
        self.unit_label.grid(row=0, column=0, sticky="nsew")

        self.multiplier_frame = Frame(self.right_frame, bg="black", height=50, width=150)
        self.multiplier_label = customtkinter.CTkLabel(self.multiplier_frame, text="1x", font=("Lato", 40, "bold"))
        self.multiplier_frame.grid(row=1, column=0, sticky="nsew")
        self.multiplier_frame.grid_propagate(False)
        self.multiplier_label.grid(row=0, column=0, sticky="nsew")


class DebugPlot(Page):
    def __init__(self, parent: Frame, model: Model):
        super().__init__(parent, model, "Debug Plot")
        self.data: Dict[int, DebugPlotValue] = model.pinned_data
        self.time_presets = [30, 60, 120, 300, 600]
        self.current_time_index = 0
        self.current_time = self.time_presets[self.current_time_index]
        self.colors = {0: "red", 1: "green", 2: "blue", 3: "yellow", 4: "orange", 5: "purple"}

        self.grid_columnconfigure(1, weight=1)
        # the frame that will hold the keys
        self.key_frame = Frame(self, width=300, height=598, bg="black")
        self.key_frame.grid_propagate(False)
        self.key_frame.grid_rowconfigure(19, weight=1)
        self.key_frame.grid_columnconfigure(4, weight=1)
        self.key_frame.grid(row=0, column=0, sticky="ew")
        self.key_frames = []

        # Create the keys
        for i in range(6):
            self.key_frames.append(DebugPlotKey(DebugPlotValue("", "", [""]), self.key_frame))
            self.key_frames[i].grid(row=i, column=0, sticky="nsew")

        # the frame that will hold the figure
        figure_frame = Frame(self, background="blue", height=600, width=800)
        figure_frame.grid(row=0, column=1, sticky="sw")

        # the figure that will contain the plot
        self.fig, self.ax = plt.subplots(facecolor="black", figsize=(8, 6), dpi=100)
        self.ax.set_facecolor('black')
        self.fig.suptitle('Debug Plot', color='c')
        self.ax.set_xlabel('Time [s]', color='c')
        self.ax.tick_params(labelcolor='blue')

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=figure_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="s")

        self.update_pinned_data()

    def enter_button_pressed(self):
        self.current_time_index += 1 if self.current_time_index < len(self.time_presets) - 1 else 0
        self.current_time = self.time_presets[self.current_time_index]

    def update(self):
        self.ax.clear()

        if time.time() - self.start >= 1:
            self.update_pinned_data()

        i = 0
        for id in self.data:
            # creating key frame
            self.key_frames[i].name_label.configure(text=self.data[id].name)
            self.key_frames[i].unit_label.configure(text=self.data[id].unit)
            self.key_frames[i].current_value_label.configure(
                text=self.data[id].data[len(self.data[id].data) - 1], text_color=self.colors[i])
            # plotting the graph
            y = self.data[id]
            self.ax.plot(y.data[len(y.data)-self.current_time: len(y.data)] if len(y.data)
                         > self.current_time else y.data, color=self.colors[i])
            i += 1

        for j in range(i, 5):
            self.key_frames[j].name_label.configure(text="")
            self.key_frames[j].unit_label.configure(text="")
            self.key_frames[j].current_value_label.configure(text="")

        self.canvas.draw()

    def update_pinned_data(self):
        self.start = time.time()
        self.model.update_pinned_data()
