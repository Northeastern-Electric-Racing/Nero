import customtkinter
from tkinter import Frame
from typing import Optional, List, Dict
from debug_mode.debug_mode import DebugMode
from debug_mode.debug_table_page import DebugTableRowValue
from efficiency_mode.efficiency_mode import EfficiencyMode
from off_mode.off_mode import OffMode
from pit_lane_mode.pit_lane_mode import PitLaneMode
from reverse_mode.reverse_mode import ReverseMode
from speed_mode.speed_mode import SpeedMode
from models.mock_model import MockModel
from models.raspberry_model import RaspberryModel
from mode import Mode
import platform
import time
from models.model import Model

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("themes/ner.json")


class NeroView(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.isLinux = platform.platform()[0:5] == "Linux"
        self.model: Model = RaspberryModel() if self.isLinux else MockModel()

        self.debounce_forward_value = 0
        self.debounce_backward_value = 0
        self.debounce_enter_value = 0
        self.debounce_up_value = 0
        self.debounce_down_value = 0
        self.debounce_left_value = 0
        self.debounce_right_value = 0
        self.debounce_max_value = 75

        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        # create the container frame that holds all modes
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create the modes that the container will hold
        self.modes: Dict[str, Mode] = {}
        self.mode_index = 0
        self.mode_names: List[str] = []
        for mode_class in (OffMode, PitLaneMode, DebugMode, SpeedMode, EfficiencyMode, ReverseMode):
            mode = mode_class(parent=container, controller=self, model=self.model)
            name = mode.name
            self.modes[name] = mode
            self.mode_names.append(name)
            mode.grid(row=0, column=0, sticky="nsew")

        for mode in self.modes.values():
            mode.create_view()

        self.update_mode()
        self.check_can()
        self.update_buttons()

    def update_mode(self):
        self.current_mode = self.modes[self.mode_names[self.mode_index]]
        self.current_mode.tkraise()

    def check_can(self):
        self.model.check_can()
        self.after(1, self.check_can)

    # Check for button inputs with debouncing / consistent time calls
    def update_buttons(self):
        start_time = time.time()
        self.update_forward_button_pressed()
        self.update_backward_button_pressed()
        self.update_enter_button_pressed()
        self.update_up_button_pressed()
        self.update_down_button_pressed()
        self.update_left_button_pressed()
        self.update_right_button_pressed()
        end_time = time.time()
        while end_time - start_time < 0.0001:
            end_time = time.time()
            pass
        self.after(1, self.update_buttons)

    # Button updates with debouncing
    def update_forward_button_pressed(self):
        value = self.model.get_forward_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_forward_value == 0:
            self.debounce_forward_value = self.debounce_max_value
            self.increment_view()
        elif value is not None and int(value) == 0:
            self.debounce_forward_value = 0
        else:
            self.debounce_forward_value -= 1

    def update_backward_button_pressed(self):
        value = self.model.get_backward_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_backward_value == 0:
            self.debounce_backward_value = self.debounce_max_value
            self.decrement_view()
        elif value is not None and int(value) == 0:
            self.debounce_backward_value = 0
        else:
            self.debounce_backward_value -= 1

    def update_right_button_pressed(self):
        value = self.model.get_right_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_right_value == 0:
            self.debounce_right_value = self.debounce_max_value
            self.current_mode.right_button_pressed()
        elif value is not None and int(value) == 0:
            self.debounce_right_value = 0
        else:
            self.debounce_right_value -= 1

    def update_left_button_pressed(self):
        value = self.model.get_left_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_left_value == 0:
            self.debounce_left_value = self.debounce_max_value
            self.current_mode.left_button_pressed()
        elif value is not None and int(value) == 0:
            self.debounce_left_value = 0
        else:
            self.debounce_left_value -= 1

    def update_up_button_pressed(self):
        value = self.model.get_up_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_up_value == 0:
            self.current_mode.up_button_pressed()
            self.debounce_up_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_up_value = 0
        else:
            self.debounce_up_value -= 1

    def update_down_button_pressed(self):
        value = self.model.get_down_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_down_value == 0:
            self.current_mode.down_button_pressed()
            self.debounce_down_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_down_value = 0
        else:
            self.debounce_down_value -= 1

    def update_enter_button_pressed(self):
        value = self.model.get_enter_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_enter_value == 0:
            self.current_mode.enter_button_pressed()
            self.debounce_enter_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_enter_value = 0
        else:
            self.debounce_enter_value -= 1

    # Handle view changes
    def increment_view(self):
        self.mode_index += 1
        if (self.mode_index >= len(self.modes)):
            self.mode_index = 0
        self.update_mode()

    def decrement_view(self):
        self.mode_index -= 1
        if (self.mode_index < 0):
            self.mode_index = len(self.modes) - 1
        self.update_mode()

    def run(self):
        if (self.isLinux):
            self.attributes('-fullscreen', True)

        self.current_mode.mainloop()
