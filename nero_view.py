import customtkinter
from tkinter import Frame
from typing import List
from modes.debug_mode.debug_mode import DebugMode
from modes.mode import Mode
from constants import MODES
from models.mock_model import MockModel
from models.raspberry_model import RaspberryModel
import platform
import time
from models.model import Model
from header import Header
import os

customtkinter.set_appearance_mode("dark")

if platform.platform()[0:5] == "Linux":
    os.chdir("/home/ner/Desktop/Nero/")

customtkinter.set_default_color_theme("themes/ner.json")


class NeroView(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.isLinux = platform.platform()[0:5] == "Linux"
        self.model: Model = RaspberryModel() if self.isLinux else MockModel()

        self.is_debug = False

        self.debounce_forward_value = 0
        self.debounce_backward_value = 0
        self.debounce_enter_value = 0
        self.debounce_up_value = 0
        self.debounce_down_value = 0
        self.debounce_left_value = 0
        self.debounce_right_value = 0

        self.debounce_max_value = 125
        self.up_debounce_max_value = 125
        self.down_debounce_max_value = 125

        # configure window
        self.title("NERO")
        self.geometry(f"{self.model.page_width}x{self.model.page_height + 60}")
        self.grid_rowconfigure(0, weight=1, minsize=60)
        self.grid_rowconfigure(1, weight=1, minsize=self.model.page_height)
        self.grid_columnconfigure(0, weight=1, minsize=self.model.page_width)

        # The consistent Header across all modes
        self.header = Header(parent=self, model=self.model)
        self.header.grid(row=0, column=0, sticky="nsew")

        # create the modes that the container will hold
        self.modes: List[Mode] = []
        self.mode_index = 0
        for mode_class in MODES:
            mode = mode_class(parent=self, controller=self, model=self.model)
            self.modes.append(mode)
            mode.grid(row=1, column=0, sticky="nsew")

        self.debug_screen = DebugMode(parent=self, controller=self, model=self.model)
        self.debug_screen.grid(row=1, column=0, sticky="nsew")

        self.update_mode()
        self.check_can()
        self.start_time = time.time()
        self.update_buttons()
        self.update_current_page()
        self.last_pack_temp_update_time = time.time()
        self.last_pinned_update_time = time.time()
        self.update_pinned_data()
        self.update_header()

    def update_mode(self):
        self.mode_index = self.model.get_mode_index() if self.model.get_mode_index() is not None else self.mode_index
        if self.is_debug:
            self.current_screen = self.debug_screen
        else:
            self.current_screen = self.modes[self.mode_index]
        self.current_mode = self.modes[self.mode_index]
        self.current_screen.tkraise()
        self.header.tkraise()
        self.after(1, self.update_mode)

    def check_can(self):
        self.model.check_can()
        self.after(1, self.check_can)

    def update_current_page(self):
        self.current_screen.current_page.update()
        self.after(100, self.update_current_page)

    def update_header(self):
        self.header.update()
        self.after(100, self.update_header)

    # Check for button inputs with debouncing / consistent time calls
    def update_buttons(self):
        end_time = time.time()
        if end_time - self.start_time < .001:
            pass
        self.update_enter_button_pressed()
        self.update_up_button_pressed()
        self.update_down_button_pressed()
        self.update_debug_pressed()
        self.update_right_button_pressed()
        self.after(1, self.update_buttons)
        self.start_time = time.time()

    def update_pinned_data(self):
        if time.time() - self.last_pack_temp_update_time >= 1:
            self.model.update_pack_temp_data()
            self.last_pack_temp_update_time = time.time()
        if time.time() - self.last_pinned_update_time >= .05:
            self.model.update_pinned_data()
            self.last_pinned_update_time = time.time()
        self.after(10, self.update_pinned_data)

    def update_right_button_pressed(self):
        value = self.model.get_right_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_right_value == 0:
            self.debounce_right_value = self.debounce_max_value
            self.current_screen.right_button_pressed()
        elif value is not None and int(value) == 0:
            self.debounce_right_value = 0
        else:
            self.debounce_right_value -= 1

    def update_debug_pressed(self):
        value = self.model.get_debug_pressed()
        if value is not None and int(value) == 1 and self.debounce_left_value == 0:
            self.debounce_left_value = self.debounce_max_value
            self.is_debug = not self.is_debug
        elif value is not None and int(value) == 0:
            self.debounce_left_value = 0
        else:
            self.debounce_left_value -= 1

    def update_up_button_pressed(self):
        value = self.model.get_up_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_up_value == 0:
            self.current_screen.up_button_pressed()
            self.debounce_up_value = self.up_debounce_max_value
            # As you continue to hold the button, the debounce time decreases until the minimum of 40
            self.up_debounce_max_value -= 5 if self.up_debounce_max_value - 5 > 40 else 0
        elif value is not None and int(value) == 0:
            self.debounce_up_value = 0
            self.up_debounce_max_value = 125
        else:
            self.debounce_up_value -= 1

    def update_down_button_pressed(self):
        value = self.model.get_down_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_down_value == 0:
            self.current_screen.down_button_pressed()
            self.debounce_down_value = self.down_debounce_max_value
            # As you continue to hold the button, the debounce time decreases until the minimum of 40
            self.down_debounce_max_value -= 5 if self.down_debounce_max_value - 5 > 40 else 0
        elif value is not None and int(value) == 0:
            self.debounce_down_value = 0
            self.down_debounce_max_value = 125
        else:
            self.debounce_down_value -= 1

    def update_enter_button_pressed(self):
        value = self.model.get_enter_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_enter_value == 0:
            self.current_screen.enter_button_pressed()
            self.debounce_enter_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_enter_value = 0
        else:
            self.debounce_enter_value -= 1

    def run(self):
        if (self.isLinux):
            self.attributes('-fullscreen', True)

        self.mainloop()
