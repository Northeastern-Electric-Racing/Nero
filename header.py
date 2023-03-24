from tkinter import Frame, PhotoImage
import customtkinter
from models.model import Model
from components.circular_progress import CircularProgressbar
from PIL.ImageTk import BitmapImage

class Header(Frame):
    def __init__(self, parent: Frame, model: Model, controller) -> None:
        super().__init__(parent, bg="black")
        self.model = model
        self.controller = controller
        self.grid_rowconfigure(0, weight=1, minsize=30)
        self.grid_columnconfigure(0, weight=1, minsize=parent.model.page_width / 8)
        self.grid_columnconfigure(1, weight=1, minsize=parent.model.page_width / 4)
        self.grid_columnconfigure(2, weight=1, minsize=parent.model.page_width / 4)
        self.grid_columnconfigure(3, weight=1, minsize=parent.model.page_width / 4)
        self.grid_columnconfigure(4, weight=1, minsize=parent.model.page_width / 8)

        #configure state of charge circle
        self.soc_canvas = customtkinter.CTkCanvas(self, height=0, width=0)
        self.soc = CircularProgressbar(self.soc_canvas, 5, 0, 35, 30)
        self.soc_canvas.configure(background="black", highlightthickness=0)
        self.soc_canvas.grid(row=0, column=0, sticky="nsew")

        #configure mpu fault frame
        self.mpu_fault_frame = Frame(self, bg="black")
        self.mpu_fault_frame.grid(row=0, column=1, sticky="nsew")

        self.mpu_fault_image_label = customtkinter.CTkLabel(
            self.mpu_fault_frame, 
            # image=PhotoImage(file="images/mpu.png"),
            text="")
        self.mpu_fault_image_label.grid(row=0, column=0, sticky="nsew")

        self.mpu_fault_label = customtkinter.CTkLabel(self.mpu_fault_frame, text="N/A")
        self.mpu_fault_label.grid(row=0, column=1, sticky="nsew", padx=5)

        #configure current mode label
        self.current_mode_label = customtkinter.CTkLabel(self, text="Current Mode: ")
        self.current_mode_label.grid(row=0, column=2, sticky="nsew", padx=5)

        #configure BMS fault frame
        self.BMS_fault_frame = Frame(self, bg="black")
        self.BMS_fault_frame.grid(row=0, column=3, sticky="nsew")

        self.BMS_fault_image_label = customtkinter.CTkLabel(
            self.BMS_fault_frame, image=BitmapImage(file="images/batteryHorizontal.xbm", foreground="white"), text="")
        self.BMS_fault_image_label.grid(row=0, column=0, sticky="nsew", pady=1)

        self.BMS_fault_label = customtkinter.CTkLabel(self.BMS_fault_frame, text="N/A")
        self.BMS_fault_label.grid(row=0, column=1, sticky="nsew", padx=5)

        #configure precharge label
        self.precharge_label = customtkinter.CTkLabel(self, text="Precharge")
        self.precharge_label.grid(row=0, column=4, sticky="e", padx=5)

    def update(self) -> None:
        self.update_soc()
        self.update_mpu_label()
        self.update_bms_label()
        self.update_precharge_label()
        self.update_current_mode_label()

    def update_bms_label(self) -> None:
        BMS_faults = hex(self.model.get_BMS_fault()) if self.model.get_BMS_fault() is not None else "N/A"
        self.BMS_fault_label.configure(text=str(BMS_faults))
    
    def update_mpu_label(self) -> None:
        MPU_faults = hex(self.model.get_MPU_fault()) if self.model.get_MPU_fault() is not None else "N/A"
        self.mpu_fault_label.configure(text=str(MPU_faults))

    def update_precharge_label(self) -> None:
        pass

    def update_soc(self) -> None:
        self.soc.set(self.model.get_state_of_charge() if self.model.get_state_of_charge() is not None else "N/A")

    def update_current_mode_label(self) -> None:
        self.current_mode_label.configure(text=self.controller.current_mode.name.upper())