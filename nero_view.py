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

        self.view = debug.Debug(self)
        self.controller = controller
        self.view.create_view()

    def check_can(self):
        self.controller.check_can()
        self.after(1, self.check_can)

    def update_speed(self):
        new_mph: Optional[int] = self.controller.get_mph()
        new_kph: Optional[int] = self.controller.get_kph()

        new_mph_text = str(new_mph) if new_mph else "N/A"
        new_kph_text = str(new_kph) if new_kph else "N/A"

        self.view.mph.configure(text=new_mph_text)
        self.view.kph.configure(text=new_kph_text)

    def update_status(self):
        new_status: Optional[bool] = self.controller.get_status()

        if new_status == True:
            self.view.status.configure(text="ON", text_color="green")
        elif new_status == False:
            self.view.status.configure(text="OFF", text_color="red")
        else:
            self.view.status.configure(text="N/A")

    def update_dir(self):
        new_dir: Optional[bool] = self.controller.get_dir()

        if new_dir == True:
            self.view.dir.configure(text="FORWARD")
        elif new_dir == False:
            self.view.dir.configure(text="REVERSE")
        else:
            self.view.dir.configure(text="N/A")

    def update_pack_temp(self):
        new_pack_temp: Optional[int] = self.controller.get_pack_temp()

        new_pack_temp_text = str(new_pack_temp) + "°" if new_pack_temp else "N/A"

        self.view.pack_temp.configure(text=new_pack_temp_text)

    def update_motor_temp(self):
        new_motor_temp: Optional[int] = self.controller.get_motor_temp()

        new_motor_temp_text = str(new_motor_temp) + "°" if new_motor_temp else "N/A"

        self.view.motor_temp.configure(text=new_motor_temp_text)

    def update_state_charge(self):
        new_charge: Optional[int] = self.controller.get_state_of_charge()

        new_charge_text = str(new_charge) + "%" if new_charge else "N/A"

        self.view.state_charge.configure(text=new_charge_text)
    def update_generic(self, id: int):
        new_generic: any = self.controller.get_generic(id)

        new_generic_text = str(new_generic) if new_generic else "N/A"

        self.view.table[id].configure(placeholder_text=new_generic_text)

    def run(self, fullscreen=False):
        if (fullscreen):
            self.attributes('-fullscreen', True)
        
        self.view.mainloop()
