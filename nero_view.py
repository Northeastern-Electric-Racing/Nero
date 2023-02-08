import customtkinter
from tkinter import Frame
from typing import Optional
from pages import home, debug

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./themes/ner.json")


class NeroView(customtkinter.CTk):
    def __init__(self, controller) -> None:
        super().__init__()
        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        self.controller = controller

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        index = 0
        for F in (home.Home, debug.Debug):
            frame = F(parent=container, controller=self)
            self.frames[index] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            index += 1

        for frame in self.frames.values():
            frame.create_view()
        self.view_index = 0
        self.update_frame()

    def update_frame(self):
        frame = self.frames[self.view_index]
        print(frame)
        frame.tkraise()

    def check_can(self):
        self.controller.check_can()
        self.after(1, self.check_can)

    def check_input(self):
        self.update_enter_button_pressed()
        self.update_forward_button_pressed()
        self.update_down_button_pressed()
        self.update_up_button_pressed()
        self.after(100, self.check_input)

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

        self.frames[1].table[id].configure(text=new_generic_text)

    def update_forward_button_pressed(self):
        forward_button_pressed = self.controller.get_forward_button_pressed()
        if forward_button_pressed:
            self.change_view()

    def update_down_button_pressed(self):
        down_button_pressed = self.controller.get_down_button_pressed()
        if down_button_pressed:
            self.frames[self.view_index].down_button_pressed()

    def update_up_button_pressed(self):
        up_button_pressed = self.controller.get_up_button_pressed()
        if up_button_pressed:
            self.frames[self.view_index].up_button_pressed()

    def update_enter_button_pressed(self):
        enter_button_pressed = self.controller.get_enter_button_pressed()
        if enter_button_pressed:
            self.frames[self.view_index].enter_button_pressed()

    def change_view(self):
        self.view_index += 1
        if (self.view_index >= len(self.frames)):
            self.view_index = 0
        self.update_frame()

    def run(self, fullscreen=False):
        if (fullscreen):
            self.attributes('-fullscreen', True)

        self.view.mainloop()
