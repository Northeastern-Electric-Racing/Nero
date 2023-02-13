import customtkinter
from tkinter import Frame
from typing import Optional, List
from pages import home, debug
from mock_model import MockModel
from raspberry_model import RaspberryModel
import platform

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./themes/ner.json")


class NeroView(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.isLinux = platform.platform()[0:5] == "Linux"
        self.controller = RaspberryModel() if self.isLinux else MockModel()

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
        index = 0
        for F in (home.Home, debug.Debug_Table):
            frame = F(parent=container, controller=self)
            self.frames[index] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            index += 1

        for frame in self.frames.values():
            frame.create_view()
        self.view_index = 0
        self.update_frame()

    def update_frame(self):
        self.controller.set_down_button_action(self.frames[self.view_index].down_button_pressed)
        self.controller.set_up_button_action(self.frames[self.view_index].up_button_pressed)
        self.controller.set_enter_button_action(self.frames[self.view_index].enter_button_pressed)
        self.controller.set_forward_button_action(self.change_view)
        frame = self.frames[self.view_index]
        frame.tkraise()

    def check_can(self):
        self.controller.check_can()
        self.after(1, self.check_can)

    # Updates for specific attributes
    def update_speed(self):
        new_mph: Optional[int] = self.controller.get_mph()
        new_kph: Optional[int] = self.controller.get_kph()

        new_mph_text = str(new_mph) if new_mph else "N/A"
        new_kph_text = str(new_kph) if new_kph else "N/A"

        self.frames[0].mph.configure(text=new_mph_text)
        self.frames[0].kph.configure(text=new_kph_text)

    def update_status(self):
        new_status: Optional[bool] = self.controller.get_status()

        if new_status == True:
            self.frames[0].status.configure(text="ON", text_color="green")
        elif new_status == False:
            self.frames[0].status.configure(text="OFF", text_color="red")
        else:
            self.frames[0].status.configure(text="N/A")

    def update_dir(self):
        new_dir: Optional[bool] = self.controller.get_dir()

        if new_dir == True:
            self.frames[0].dir.configure(text="FORWARD")
        elif new_dir == False:
            self.frames[0].dir.configure(text="REVERSE")
        else:
            self.frames[0].dir.configure(text="N/A")

    def update_pack_temp(self):
        new_pack_temp: Optional[int] = self.controller.get_pack_temp()

        new_pack_temp_text = str(new_pack_temp) + "°" if new_pack_temp else "N/A"

        self.frames[0].pack_temp.configure(text=new_pack_temp_text)

    def update_motor_temp(self):
        new_motor_temp: Optional[int] = self.controller.get_motor_temp()

        new_motor_temp_text = str(new_motor_temp) + "°" if new_motor_temp else "N/A"

        self.frames[0].motor_temp.configure(text=new_motor_temp_text)

    def update_state_charge(self):
        new_charge: Optional[int] = self.controller.get_state_of_charge()

        new_charge_text = str(new_charge) + "%" if new_charge else "N/A"

        self.frames[0].state_charge.configure(text=new_charge_text)

    def update_generic(self, id: int):
        new_generic: any = self.controller.get_generic(id)
        new_generic_text = str(new_generic) if new_generic else "N/A"
        self.frames[1].table[id].value_label.configure(text=new_generic_text)

    def create_debug_table(self) -> List[debug.Table_Row]:
        values: List[debug.Table_Row_Value] = self.controller.get_debug_table_values()

        table: List[debug.Table_Row] = []
        for i in range(len(values)):
            parent: Frame
            if i % 2 == 0:
                parent = self.frames[1].left_frame
            else:
                parent = self.frames[1].right_frame
            table.append(debug.Table_Row(parent, values[i]))
        return table

    def update_forward_button_pressed(self):
        self.change_view()

    # Handle view changes
    def change_view(self):
        self.view_index += 1
        if (self.view_index >= len(self.frames)):
            self.view_index = 0
        self.update_frame()

    def run(self):
        if (self.isLinux):
            self.attributes('-fullscreen', True)

        self.frames[self.view_index].mainloop()
