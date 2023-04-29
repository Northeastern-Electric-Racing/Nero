from tkinter import Frame, Canvas
import customtkinter
from models.model import Model
from components.circular_progress import CircularProgressbar
from PIL.ImageTk import BitmapImage
from color_transformers import precharge_state_color_transformer

class Header(Frame):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, bg="black")
        self.model = model
        self.parent = parent
        self.grid_rowconfigure(0, weight=1, minsize=60)
        self.grid_columnconfigure(0, weight=1, minsize=model.page_width / 8)
        self.grid_columnconfigure(1, weight=1, minsize=model.page_width / 4)
        self.grid_columnconfigure(2, weight=1, minsize=model.page_width / 4)
        self.grid_columnconfigure(3, weight=1, minsize=model.page_width / 4)
        self.grid_columnconfigure(4, weight=1, minsize=model.page_width / 8)

        # configure state of charge circle
        self.soc = CircularProgressbar(self, 5, 0, 65, 60)
        self.soc.grid(row=0, column=0, sticky="nsew")

        # configure fault frame
        self.fault_frame = Frame(self, bg="black")
        self.fault_frame.grid_rowconfigure(0, weight=1)
        self.fault_frame.grid_columnconfigure(0, weight=1)
        self.fault_frame.grid_columnconfigure(1, weight=1)
        self.fault_frame.grid(row=0, column=1, sticky="nsew")

        self.mpu_fault_image_label = customtkinter.CTkLabel(self.fault_frame, text="")
        self.mpu_fault_image_label.grid(row=0, column=0, sticky="nsew", pady=1)

        self.BMS_fault_image_label = customtkinter.CTkLabel(
            self.fault_frame, text="")
        self.BMS_fault_image_label.grid(row=0, column=1, sticky="nsew", pady=1)

        # configure current mode label
        self.current_mode_label = customtkinter.CTkLabel(self, text="Current Mode: ", font=customtkinter.CTkFont(size=28))
        self.current_mode_label.grid(row=0, column=2, sticky="nsew", padx=5)

        # configure summary frame
        self.summary_frame = Frame(self, bg="black")
        self.summary_frame.grid_rowconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(2, weight=1)
        self.summary_frame.grid(row=0, column=3, sticky="nsew")

        self.pack_temp_image = BitmapImage(file="images/packTemp.xbm", foreground="white")
        self.pack_temp_label = customtkinter.CTkLabel(self.summary_frame, image=self.pack_temp_image, text="")
        self.pack_temp_label.grid(row=0, column=0, sticky="nsew")

        self.motor_temp_image = BitmapImage(file="images/motorTemp.xbm", foreground="white")
        self.motor_temp_label = customtkinter.CTkLabel(self.summary_frame, image=self.motor_temp_image, text="")
        self.motor_temp_label.grid(row=0, column=1, sticky="nsew")

        self.pack_voltage_image = BitmapImage(file="images/packVoltage.xbm", foreground="white")
        self.pack_voltage_label = customtkinter.CTkLabel(self.summary_frame, image=self.pack_voltage_image, text="")
        self.pack_voltage_label.grid(row=0, column=2, sticky="nsew")

        # configure precharge label
        self.vbat_label = customtkinter.CTkLabel(self, text="N/A", font=customtkinter.CTkFont(size=25))
        self.vbat_label.grid(row=0, column=4, sticky="e", padx=5)

    def update(self) -> None:
        self.update_soc()
        self.update_mpu_image()
        self.update_bms_image()
        self.update_vbat_label()
        self.update_current_mode_label()
        self.update_pack_temp()
        self.update_motor_temp()
        self.update_pack_voltage()

    def update_bms_image(self) -> None:
        if self.model.get_BMS_fault() is not None and self.model.get_BMS_fault() > 0:
            self.BMS_fault_image_label.configure(image=BitmapImage(file="images/batteryWarning.xbm", foreground="red"))
        else:
            self.BMS_fault_image_label.configure(image=BitmapImage(file="images/batteryWarning.xbm", foreground="green"))

    def update_mpu_image(self) -> None:
        if self.model.get_traction_control() is not None and int(self.model.get_traction_control()) > 0:
            self.mpu_fault_image_label.configure(image=BitmapImage(file="images/mpu.xbm", foreground="green"))
        else:
            self.mpu_fault_image_label.configure(image=BitmapImage(file="images/mpu.xbm", foreground="red"))

    def update_vbat_label(self) -> None:
        vbat = self.model.get_vbat() if self.model.get_vbat() is not None else "N/A"
        self.vbat_label.configure(text=str(vbat))

    def update_pack_temp(self) -> None:
        pack_temp_value = self.model.get_pack_temp() if self.model.get_pack_temp() is not None else 0
        color = "purple" if pack_temp_value < 0 else "blue" if pack_temp_value < 20 else "green" if pack_temp_value < 30 else "yellow" if pack_temp_value < 40 else "orange" if pack_temp_value < 50 else "red"
        self.pack_temp_label.configure(image=BitmapImage(file="images/packTemp.xbm", foreground=color))

    def update_motor_temp(self) -> None:
        motor_temp_value = self.model.get_motor_temp() if self.model.get_motor_temp() is not None else 0
        color = "purple" if motor_temp_value < 10 else "blue" if motor_temp_value < 20 else "green" if motor_temp_value < 50 else "yellow" if motor_temp_value < 70 else "orange" if motor_temp_value < 85 else "red"
        self.motor_temp_label.configure(image=BitmapImage(file="images/motorTemp.xbm", foreground=color))

    def update_pack_voltage(self) -> None:
        pack_voltage_value = self.model.get_pack_voltage() if self.model.get_pack_voltage() is not None else 0
        color = "red" if pack_voltage_value < 200 else "orange" if pack_voltage_value < 240 else "yellow" if pack_voltage_value < 280 else "green"
        self.pack_voltage_label.configure(image=BitmapImage(file="images/packVoltage.xbm", foreground=color))

    def update_soc(self) -> None:
        self.soc.set(int(self.model.get_state_of_charge()) if self.model.get_state_of_charge() is not None else "N/A")

    def update_current_mode_label(self) -> None:
        self.current_mode_label.configure(text=self.parent.current_mode.name.upper())
