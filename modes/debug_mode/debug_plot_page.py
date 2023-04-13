from tkinter import Frame
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List
from models.model import Model
from modes.debug_mode.debug_utils import DebugPlotValue
from modes.page import Page
import time

class DebugPlotKey(Frame):
    def __init__(self, key_value: DebugPlotValue, parent: Frame, width: int):
        super().__init__(parent, bg="black", highlightbackground='gray', highlightthickness=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.name_frame = Frame(self, bg="black", height=30)
        self.name_label = customtkinter.CTkLabel(self.name_frame, text=key_value.name, font=("Lato", 25, "bold"))
        self.name_frame.grid(row=0, column=0, sticky="nsew")
        self.name_label.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self, bg="black")
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1, minsize=width * 0.6)
        self.bottom_frame.grid_columnconfigure(1, weight=1, minsize=width * 0.4)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.current_value_label = customtkinter.CTkLabel(self.bottom_frame,
                                                          text=key_value.data[len(key_value.data) - 1], font=("Lato", 55))
        self.current_value_label.grid(row=0, column=0, padx=5, sticky="nsw")

        self.right_frame = Frame(self.bottom_frame, bg="black")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.unit_label = customtkinter.CTkLabel(self.right_frame, text=key_value.unit, font=("Lato", 25, "bold"))
        self.unit_label.grid(row=0, column=0, sticky="nsew")

        self.multiplier_label = customtkinter.CTkLabel(self.right_frame, text="1x", font=("Lato", 25, "bold"))
        self.multiplier_label.grid(row=1, column=0, sticky="nsew")


class DebugPlot(Page):
    def __init__(self, parent: Frame, model: Model):
        super().__init__(parent, model, "Debug Plot")
        self.data: Dict[int, DebugPlotValue] = model.pinned_data
        self.time_presets = [30, 60, 120, 300, 600]
        self.current_time_index = 0
        self.current_time = self.time_presets[self.current_time_index]
        self.colors = ["red", "green", "blue", "yellow", "orange", "purple"]

        self.grid_columnconfigure(0, weight=1, minsize=self.width * 0.3)
        self.grid_columnconfigure(1, weight=1, minsize=self.width * 0.7)
        self.grid_rowconfigure(0, weight=1)

        # the frame that will hold the keys
        self.key_frame = Frame(self, bg="black")
        self.key_frame.grid_columnconfigure(0, weight=1)
        self.key_frame.grid(row=0, column=0, sticky="nsew")

        self.key_frames: List[DebugPlotKey] = []
        # Create the keys
        for i in range(6):
            self.key_frame.grid_rowconfigure(i, weight=1, minsize=self.height/6)
            self.key_frames.append(DebugPlotKey(DebugPlotValue("", "", [""]), self.key_frame, self.width * 0.3))
            self.key_frames[i].grid(row=i, column=0, sticky="nsew")

        # the frame that will hold the figure
        figure_frame = Frame(self, background="black")
        figure_frame.grid(row=0, column=1, sticky="nsew")
        figure_frame.grid_rowconfigure(0, weight=1)
        figure_frame.grid_columnconfigure(0, weight=1)

        # the figure that will contain the plot
        self.fig, self.ax = plt.subplots(facecolor="black", dpi=100)
        self.ax.set_facecolor('black')
        self.fig.suptitle('Debug Plot', color='white')
        self.ax.set_xlabel('Time [s]', color='white')
        self.ax.tick_params(labelcolor='white')

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=figure_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.start_time = time.time()

    def enter_button_pressed(self):
        self.current_time_index = (self.current_time_index +
                                   1) if self.current_time_index < len(self.time_presets) - 1 else 0
        self.current_time = self.time_presets[self.current_time_index]

    def update(self):
        if (time.time() - self.start_time > 1):
            self.ax.clear()
            i = 0
            for id in self.data:
                # creating key frame
                self.key_frames[i].name_label.configure(text=self.data[id].name)
                self.key_frames[i].unit_label.configure(text=self.data[id].unit)
                self.key_frames[i].current_value_label.configure(
                    text=self.data[id].data[0], text_color=self.colors[i])

                # plotting the graph
                y = self.data[id].data
                self.ax.plot(y[0: self.current_time] if len(y) > self.current_time else y, color=self.colors[i])
                i += 1
            self.ax.invert_xaxis()
            for j in range(i, 5):
                self.key_frames[j].name_label.configure(text="")
                self.key_frames[j].unit_label.configure(text="")
                self.key_frames[j].current_value_label.configure(text="")
            self.canvas.draw()
