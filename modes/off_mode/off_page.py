from tkinter import Frame, BitmapImage
from modes.page import Page
from models.model import Model
from components.battery_progress import BatteryProgress
from components.thermometer_progress import ThermometerProgress
import customtkinter
from color_transformers import precharge_state_color_transformer


class Off(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Off Mode")
        self.label_font = customtkinter.CTkFont(size=75)
        self.grid_columnconfigure(0, weight=1, minsize=self.width / 3)
        self.grid_columnconfigure(1, weight=1, minsize=self.width / 3)
        self.grid_columnconfigure(2, weight=1, minsize=self.width / 3)
        self.grid_rowconfigure(0, weight=1)

        self.state_of_charge_battery = BatteryProgress(self, 50, 100, 250, 450)
        self.state_of_charge_battery.grid(row=0, column=0, sticky="nsew")

        self.middle_frame = Frame(self, bg="black")
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")

        self.right_frame = Frame(self, bg="black")
        self.right_frame.grid_rowconfigure(0, weight=1, minsize=self.height / 2)
        self.right_frame.grid_rowconfigure(1, weight=1, minsize=self.height / 2)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Configure the middle frame
        self.off_label = customtkinter.CTkLabel(self.middle_frame, font=(
            customtkinter.CTkFont(size=200)), text_color="red", text="OFF")
        self.off_label.grid(row=0, column=0, sticky="nsew")

        self.precharge_label = customtkinter.CTkLabel(self.middle_frame, font=(
            customtkinter.CTkFont(size=50)), text_color="red", text="N/A")
        self.precharge_label.grid(row=1, column=0, sticky="nsew")

        # Configure the right frame
        # Configure the pack temp frame
        self.pack_temp_frame = Frame(self.right_frame, bg="black")
        self.pack_temp_frame.grid_rowconfigure(0, weight=1)
        self.pack_temp_frame.grid_rowconfigure(1, weight=1)
        self.pack_temp_frame.grid_columnconfigure(0, weight=1)
        self.pack_temp_frame.grid(row=0, column=0, sticky="nsew")

        self.pack_temp_thermometer = ThermometerProgress(self.pack_temp_frame, 0, 50, 200, 200, 65, -15)
        self.pack_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.pack_temp_value_frame = Frame(self.pack_temp_frame, bg="black")
        self.pack_temp_value_frame.grid_rowconfigure(0, weight=1)
        self.pack_temp_value_frame.grid_rowconfigure(1, weight=1)
        self.pack_temp_value_frame.grid_columnconfigure(0, weight=1)
        self.pack_temp_value_frame.grid(row=0, column=1, sticky="nsew")

        self.pack_temp_value = customtkinter.CTkLabel(self.pack_temp_value_frame, text="N/A°", font=self.label_font)
        self.pack_temp_value.grid(row=0, column=0, sticky="sew")

        self.pack_temp_label = customtkinter.CTkLabel(self.pack_temp_value_frame, text="Pack", font=self.label_font)
        self.pack_temp_label.grid(row=1, column=0, sticky="new", padx=5)

        # Configure the motor temp frame
        self.motor_temp_frame = Frame(self.right_frame, bg="black")
        self.motor_temp_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_frame.grid_rowconfigure(1, weight=1)
        self.motor_temp_frame.grid_columnconfigure(0, weight=1)
        self.motor_temp_frame.grid(row=1, column=0, sticky="nsew")

        self.motor_temp_thermometer = ThermometerProgress(self.motor_temp_frame, 0, 50, 200, 200)
        self.motor_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.motor_temp_value_frame = Frame(self.motor_temp_frame, bg="black")
        self.motor_temp_value_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_value_frame.grid_rowconfigure(1, weight=1)
        self.motor_temp_value_frame.grid_columnconfigure(0, weight=1)
        self.motor_temp_value_frame.grid(row=0, column=1, sticky="nsew")

        self.motor_temp_value = customtkinter.CTkLabel(self.motor_temp_value_frame, text="N/A°", font=self.label_font)
        self.motor_temp_value.grid(row=0, column=0, sticky="sew")

        self.motor_temp_label = customtkinter.CTkLabel(self.motor_temp_value_frame, text="Motor", font=self.label_font)
        self.motor_temp_label.grid(row=1, column=0, sticky="new", padx=5)

    def update(self) -> None:
        self.update_pack_temp()
        self.update_precharge()
        self.update_state_of_charge()
        self.update_motor_temp()

    def update_pack_temp(self) -> None:
        pack_temp = self.model.get_pack_temp() if self.model.get_pack_temp() is not None else "N/A"
        self.pack_temp_thermometer.set(pack_temp)
        self.pack_temp_value.configure(text=f"{pack_temp}°")

    def update_precharge(self) -> None:
        precharge = self.model.get_precharge() if self.model.get_precharge() is not None else "N/A"
        precharge = self.mapValueToPrecharge(precharge)
        self.precharge_label.configure(text=precharge, text_color=precharge_state_color_transformer(precharge))
        if precharge == "Ready":
            self.off_label.configure(text="ACTIVE", text_color="yellow")

    def update_state_of_charge(self) -> None:
        state_of_charge = int(self.model.get_state_of_charge()) if self.model.get_state_of_charge() is not None else "N/A"
        self.state_of_charge_battery.set(state_of_charge)

    def update_motor_temp(self) -> None:
        motor_temp = self.model.get_motor_temp() if self.model.get_motor_temp() is not None else "N/A"
        self.motor_temp_thermometer.set(motor_temp)
        self.motor_temp_value.configure(text=f"{motor_temp}°")
    
    def mapValueToPrecharge(self, value: int | str) -> str:
        if isinstance(value, int):
            match value:
                case 0:
                    return "GLV ON"
                case 1:
                    return "PRECHARGING"
                case 2:
                    return "TSMS ON"
                case 3:
                    return "PRECHARGING"
                case 4: 
                    return "READY"
                case 5:
                    return "FAULTED"
        else:
            return value



