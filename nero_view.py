import customtkinter
from tkinter import Frame
from typing import Optional, List
from pages import home, debug
from mock_model import MockModel
from raspberry_model import RaspberryModel
import platform
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./themes/ner.json")


class NeroView(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.isLinux = platform.platform()[0:5] == "Linux"
        self.model = RaspberryModel() if self.isLinux else MockModel()

        self.view_index = 0
        self.view_dict = {0: "Home", 1: "Debug Table"}

        self.debounce_forward_value = 0
        self.debounce_enter_value = 0
        self.debounce_up_value = 0
        self.debounce_down_value = 0
        self.debounce_max_value = 75

        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        # create the container frame that holds all views
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create the views that the container will hold
        self.frames = {}
        for page in (home.Home, debug.Debug_Table):
            frame = page(parent=container, controller=self)
            name = frame.name
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        for frame in self.frames.values():
            frame.create_view()
        self.update_frame()
        self.check_can()
        self.update_buttons()

    def update_frame(self):
        frame = self.frames[self.view_dict[self.view_index]]
        frame.tkraise()

    def check_can(self):
        self.model.check_can()
        self.after(1, self.check_can)

    # Check for button inputs with debouncing / consistent time calls
    def update_buttons(self):
        start_time = time.time()
        self.update_forward_button_pressed()
        self.update_enter_button_pressed()
        self.update_up_button_pressed()
        self.update_down_button_pressed()
        end_time = time.time()
        while end_time - start_time < 0.0001:
            end_time = time.time()
            pass
        self.after(1, self.update_buttons)

    # Updates for specific attributes
    def update_speed(self):
        new_mph: Optional[int] = self.model.get_mph()
        new_kph: Optional[int] = self.model.get_kph()

        new_mph_text = str(new_mph) if new_mph else "N/A"
        new_kph_text = str(new_kph) if new_kph else "N/A"

        self.frames["Home"].mph.configure(text=new_mph_text)
        self.frames["Home"].kph.configure(text=new_kph_text)

    def update_status(self):
        new_status: Optional[bool] = self.model.get_status()

        if new_status == True:
            self.frames["Home"].status.configure(text="ON", text_color="green")
        elif new_status == False:
            self.frames["Home"].status.configure(text="OFF", text_color="red")
        else:
            self.frames["Home"].status.configure(text="N/A")

    def update_dir(self):
        new_dir: Optional[bool] = self.model.get_dir()

        if new_dir == True:
            self.frames["Home"].dir.configure(text="FORWARD")
        elif new_dir == False:
            self.frames["Home"].dir.configure(text="REVERSE")
        else:
            self.frames["Home"].dir.configure(text="N/A")

    def update_pack_temp(self):
        new_pack_temp: Optional[int] = self.model.get_pack_temp()

        new_pack_temp_text = str(new_pack_temp) + "°" if new_pack_temp else "N/A"

        self.frames["Home"].pack_temp.configure(text=new_pack_temp_text)

    def update_motor_temp(self):
        new_motor_temp: Optional[int] = self.model.get_motor_temp()

        new_motor_temp_text = str(new_motor_temp) + "°" if new_motor_temp else "N/A"

        self.frames["Home"].motor_temp.configure(text=new_motor_temp_text)

    def update_state_charge(self):
        new_charge: Optional[int] = self.model.get_state_of_charge()

        new_charge_text = str(new_charge) + "%" if new_charge else "N/A"

        self.frames["Home"].state_charge.configure(text=new_charge_text)

    # update for generic values (debug table)
    def update_by_id(self, id: int):
        new_generic: any = self.model.get_by_id(id)
        new_generic_text = str(new_generic) if new_generic else "N/A"
        self.frames["Debug Table"].table[id].value_label.configure(text=new_generic_text)

    # Create the debug table with initial values
    def create_debug_table(self) -> List[debug.Debug_Table_Row]:
        values: List[debug.Debug_Table_Row_Value] = self.model.get_debug_table_values()

        table: List[debug.Debug_Table_Row] = []
        for i in range(len(values)):
            parent: Frame
            if i % 2 == 0:
                parent = self.frames["Debug Table"].left_frame
            else:
                parent = self.frames["Debug Table"].right_frame
            table.append(debug.Debug_Table_Row(parent, values[i]))
        return table

    # Button updates with debouncing
    def update_forward_button_pressed(self):
        value = self.model.get_forward_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_forward_value == 0:
            self.debounce_forward_value = self.debounce_max_value
            self.change_view()
        elif value is not None and int(value) == 0:
            self.debounce_forward_value = 0
        else:
            self.debounce_forward_value -= 1

    def update_up_button_pressed(self):
        value = self.model.get_up_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_up_value == 0:
            self.frames[self.view_dict[self.view_index]].up_button_pressed()
            self.debounce_up_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_up_value = 0
        else:
            self.debounce_up_value -= 1

    def update_down_button_pressed(self):
        value = self.model.get_down_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_down_value == 0:
            self.frames[self.view_dict[self.view_index]].down_button_pressed()
            self.debounce_down_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_down_value = 0
        else:
            self.debounce_down_value -= 1

    def update_enter_button_pressed(self):
        value = self.model.get_enter_button_pressed()
        if value is not None and int(value) == 1 and self.debounce_enter_value == 0:
            self.frames[self.view_dict[self.view_index]].enter_button_pressed()
            self.debounce_enter_value = self.debounce_max_value
        elif value is not None and int(value) == 0:
            self.debounce_enter_value = 0
        else:
            self.debounce_enter_value -= 1

    # Handle view changes
    def change_view(self):
        self.view_index += 1
        if (self.view_index >= len(self.frames)):
            self.view_index = 0
        self.update_frame()

    def run(self):
        if (self.isLinux):
            self.attributes('-fullscreen', True)

        self.frames[self.view_dict[self.view_index]].mainloop()
