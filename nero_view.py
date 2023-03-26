import customtkinter
from tkinter import Frame
from modes.debug_mode.debug_mode import DebugMode
from modes.efficiency_mode.efficiency_mode import EfficiencyMode
from modes.off_mode.off_mode import OffMode
from modes.charging_mode.charging_mode import ChargingMode
from modes.pit_lane_mode.pit_lane_mode import PitLaneMode
from modes.reverse_mode.reverse_mode import ReverseMode
from modes.speed_mode.speed_mode import SpeedMode
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

        self.debounce_forward_value = 0
        self.debounce_backward_value = 0
        self.debounce_enter_value = 0
        self.debounce_up_value = 0
        self.debounce_down_value = 0
        self.debounce_left_value = 0
        self.debounce_right_value = 0
        self.debounce_max_value = 125

        # configure window
        self.title("NERO")
        self.geometry(f"{1024}x{600}")

        # create the container frame that holds all modes
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create the modes that the container will hold
        self.modes = []
        self.mode_index = 0

        self.header = Header(parent=container)
        self.header.place(x=0, y=0, relwidth=1, relheight=0.05)
        for mode_class in (OffMode, PitLaneMode, EfficiencyMode, SpeedMode, DebugMode, ReverseMode, ChargingMode):
            # for mode_class in (EfficiencyMode, DebugMode, ChargingMode):
            mode = mode_class(parent=container, controller=self, model=self.model)
            self.modes.append(mode)
            mode.grid(row=0, column=0, sticky="s")

        self.update_mode()
        self.check_can()
        self.update_buttons()
        self.update_current_page()
        self.last_pinned_update_time_600 = time.time()
        self.last_pinned_update_time_300 = time.time()
        self.last_pinned_update_time_120 = time.time()
        self.last_pinned_update_time_60 = time.time()
        self.last_pinned_update_time_30 = time.time()
        self.update_pinned_data()
        self.update_header()

    def update_mode(self):
        if self.model.get_BMS_state() is not None and self.model.get_BMS_state() >= 2:
            self.current_mode = self.modes[6]
        else:
            self.current_mode = self.modes[self.mode_index]
        self.current_mode.tkraise()
        self.header.tkraise()

    def check_can(self):
        self.model.check_can()
        self.after(1, self.check_can)

    def update_current_page(self):
        self.current_mode.current_page.update()
        self.after(100, self.update_current_page)

    # Check for button inputs with debouncing / consistent time calls
    def update_buttons(self):
        start_time = time.time()
        # self.update_forward_button_pressed()
        # self.update_backward_button_pressed()
        self.update_mode_index()
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

    def update_pinned_data(self):
        if time.time() - self.last_pinned_update_time_600 >= 1:
            self.model.update_pack_temp_data()
            self.model.update_pinned_data(self.model.pinned_data_600)
            self.last_pinned_update_time_600 = time.time()
        if time.time() - self.last_pinned_update_time_300 >= 0.5:
            self.model.update_pinned_data(self.model.pinned_data_300)
            self.last_pinned_update_time_300 = time.time()
        if time.time() - self.last_pinned_update_time_120 >= 0.2:
            self.model.update_pinned_data(self.model.pinned_data_120)
            self.last_pinned_update_time_120 = time.time()
        if time.time() - self.last_pinned_update_time_60 >= 0.1:
            self.model.update_pinned_data(self.model.pinned_data_60)
            self.last_pinned_update_time_60 = time.time()
        if time.time() - self.last_pinned_update_time_30 >= 0.05:
            self.model.update_pinned_data(self.model.pinned_data_30)
            self.last_pinned_update_time_30 = time.time()

        for pinned in self.model.pinned_data:
            print("new")
            for data in pinned.values():
                print(len(data.data))
        self.after(10, self.update_pinned_data)

    def update_mode_index(self):
        self.mode_index = self.model.get_mode_index() if self.model.get_mode_index() is not None else self.mode_index
        self.update_mode()

    # Button updates with debouncing
    # def update_forward_button_pressed(self):
    #     value = self.model.get_forward_button_pressed()
    #     if value is not None and int(value) == 1 and self.debounce_forward_value == 0:
    #         self.debounce_forward_value = self.debounce_max_value
    #         self.increment_mode()
    #     elif value is not None and int(value) == 0:
    #         self.debounce_forward_value = 0
    #     else:
    #         self.debounce_forward_value -= 1

    # def update_backward_button_pressed(self):
    #     value = self.model.get_backward_button_pressed()
    #     if value is not None and int(value) == 1 and self.debounce_backward_value == 0:
    #         self.debounce_backward_value = self.debounce_max_value
    #         self.decrement_mode()
    #     elif value is not None and int(value) == 0:
    #         self.debounce_backward_value = 0
    #     else:
    #         self.debounce_backward_value -= 1

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

    def update_header(self):
        self.header.current_mode_label.configure(text=self.current_mode.name)
        self.after(100, self.update_header)

    def increment_mode(self):
        self.mode_index += 1
        if (self.mode_index >= len(self.modes)):
            self.mode_index = 0
        self.update_mode()

    def decrement_mode(self):
        self.mode_index -= 1
        if (self.mode_index < 0):
            self.mode_index = len(self.modes) - 1
        self.update_mode()

    def run(self):
        if (self.isLinux):
            self.attributes('-fullscreen', True)

        self.mainloop()
