from tkinter import Frame, BitmapImage
from modes.page import Page
from models.model import Model
import customtkinter

class Off(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Off Mode")
        self.label_font = customtkinter.CTkFont(size=80)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = Frame(self, bg="black")
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.middle_frame = Frame(self, bg="black")
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")

        self.right_frame = Frame(self, bg="black")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        #Configure the left frame
        self.pack_temp_frame = Frame(self.left_frame, bg="black")
        self.pack_temp_frame.grid_rowconfigure(0, weight=1)
        self.pack_temp_frame.grid_rowconfigure(1, weight=1)
        self.pack_temp_frame.grid_columnconfigure(0, weight=1)
        self.pack_temp_frame.grid(row=0, column=0, sticky="nsew")

        self.pack_temp_label = customtkinter.CTkLabel(self.pack_temp_frame, text="N/A°", font=self.label_font)
        self.pack_temp_label.grid(row=0, column=0, sticky="s")

        self.pack_temp_icon = customtkinter.CTkLabel(self.pack_temp_frame, text="", image=BitmapImage(file="images/batteryVertical.xbm", foreground="white"))
        self.pack_temp_icon.grid(row=1, column=0, sticky="n")

        self.precharge_label = customtkinter.CTkLabel(self.left_frame, text="N/A", font=self.label_font)
        self.precharge_label.grid(row=1, column=0, sticky="nsew")

        #Configure the middle frame
        self.off_label = customtkinter.CTkLabel(self.middle_frame, font=(customtkinter.CTkFont(size=200)), text_color="red", text="OFF")
        self.off_label.grid(row=0, column=0, sticky="nsew")

        #Configure the right frame
        self.state_of_charge_label = customtkinter.CTkLabel(self.right_frame, text="N/A%", font=self.label_font)
        self.state_of_charge_label.grid(row=0, column=0, sticky="nsew")

        self.motor_temp_frame = Frame(self.right_frame, bg="black")
        self.motor_temp_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_frame.grid_rowconfigure(1, weight=1)
        self.motor_temp_frame.grid_columnconfigure(0, weight=1)
        self.motor_temp_frame.grid(row=1, column=0, sticky="nsew")

        self.motor_temp_label = customtkinter.CTkLabel(self.motor_temp_frame, text="N/A°", font=self.label_font)
        self.motor_temp_label.grid(row=0, column=0, sticky="s")

        self.motor_temp_icon = customtkinter.CTkLabel(self.motor_temp_frame, text="", image=BitmapImage(file="images/voltageIcon.xbm", foreground="white"))
        self.motor_temp_icon.grid(row=1, column=0, sticky="n")

    def update(self) -> None:
        self.update_pack_temp()
        self.update_precharge()
        self.update_state_of_charge()
        self.update_motor_temp()

    def update_pack_temp(self) -> None:
        pack_temp = self.model.get_pack_temp() if not None else "N/A"
        self.pack_temp_label.configure(text=f"{pack_temp}°")


    def update_precharge(self) -> None:
        precharge = self.model.get_precharge() if not None else "N/A"
        self.precharge_label.configure(text=precharge)

    def update_state_of_charge(self) -> None:
        state_of_charge = self.model.get_state_of_charge() if not None else "N/A"
        self.state_of_charge_label.configure(text=f"{state_of_charge}%")

    def update_motor_temp(self) -> None:
        motor_temp = self.model.get_motor_temp() if not None else "N/A"
        self.motor_temp_label.configure(text=f"{motor_temp}°")

