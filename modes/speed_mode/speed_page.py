from tkinter import Frame, BitmapImage
from modes.page import Page
from models.model import Model
from components.gforce_graph import GForceGraph
from customtkinter import CTkLabel
from components.thermometer_progress import ThermometerProgress
from components.spedometer import Spedometer
import numpy as np


class Speed(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Speed")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=self.width/4)
        self.grid_columnconfigure(1, weight=1, minsize=self.width/2)
        self.grid_columnconfigure(2, weight=1, minsize=self.width/4)

        self.left_frame = Frame(self, bg="black")
        self.left_frame.grid_rowconfigure(0, weight=1, minsize=self.height / 2)
        self.left_frame.grid_rowconfigure(1, weight=1, minsize=self.height/8)
        self.left_frame.grid_rowconfigure(2, weight=1, minsize=self.height/8)
        self.left_frame.grid_rowconfigure(3, weight=1, minsize=self.height/8)
        self.left_frame.grid_rowconfigure(4, weight=1, minsize=self.height/8)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.middle_frame = Frame(self)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")

        self.right_frame = Frame(self)
        self.right_frame.grid_rowconfigure(0, weight=1, minsize=self.height / 4)
        self.right_frame.grid_rowconfigure(1, weight=1, minsize=self.height / 12)
        self.right_frame.grid_rowconfigure(2, weight=1, minsize=self.height / 3)
        self.right_frame.grid_rowconfigure(3, weight=1, minsize=self.height / 3)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Create the left frame

        self.gforce_graph_frame = Frame(self.left_frame)
        self.gforce_graph_frame.grid(row=0, column=0, sticky="nsew")
        self.gforce_graph_frame.grid_rowconfigure(0, weight=1)
        self.gforce_graph_frame.grid_columnconfigure(0, weight=1)

        self.gforce_graph = GForceGraph(self.left_frame)
        self.gforce_graph.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.gforce_label = CTkLabel(self.left_frame, text="N/AG", font=("Lato", 50))
        self.gforce_label.grid(row=1, column=0, sticky="nsew")

        self.gforce_x_label = CTkLabel(self.left_frame, text="X: N/A", font=("Lato", 30))
        self.gforce_x_label.grid(row=2, column=0, sticky="nsw", padx=10)

        self.gforce_y_label = CTkLabel(self.left_frame, text="Y: N/A", font=("Lato", 30))
        self.gforce_y_label.grid(row=3, column=0, sticky="nsw", padx=10)

        self.gforce_z_label = CTkLabel(self.left_frame, text="Z: N/A", font=("Lato", 30))
        self.gforce_z_label.grid(row=4, column=0, sticky="nsw", padx=10)

        # Create the middle frame
        self.spedometer_frame = Frame(self.middle_frame)
        self.spedometer_frame.grid(row=0, column=0, sticky="nsew")
        self.spedometer_frame.grid_rowconfigure(0, weight=1)
        self.spedometer_frame.grid_columnconfigure(0, weight=1)

        self.spedometer = Spedometer(self.spedometer_frame, 0, self.height/8, self.width/2, self.height)
        self.spedometer.grid(row=0, column=0, sticky="nsew")
        self.spedometer.set(40)

        # Create the right frame
        # Create the current frame
        self.current_frame = Frame(self.right_frame, bg="black")
        self.current_frame.grid_rowconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

        self.current_icon = CTkLabel(self.current_frame, text="", image=BitmapImage(
            file="images/lightningBolt.xbm", foreground="yellow"))
        self.current_icon.grid(row=0, column=0, sticky="nse")

        self.current_label = CTkLabel(self.current_frame, text="N/AA", font=("Lato", 80))
        self.current_label.grid(row=0, column=1, sticky="nse", padx=10)

        # Create the dcl frame
        self.dcl_frame = Frame(self.right_frame, bg="black")
        self.dcl_frame.grid_rowconfigure(0, weight=1)
        self.dcl_frame.grid_columnconfigure(0, weight=1)
        self.dcl_frame.grid(row=1, column=0, sticky="nsew")

        self.dcl_icon = CTkLabel(self.dcl_frame, text="", image=BitmapImage(
            file="images/limitIcon.xbm", foreground="yellow"))
        self.dcl_icon.grid(row=0, column=0, sticky="nse")

        self.dcl_label = CTkLabel(self.dcl_frame, text="N/AA", font=("Lato", 30))
        self.dcl_label.grid(row=0, column=1, sticky="nse", padx=10)

        # Create the max cell frame
        self.max_cell_frame = Frame(self.right_frame)
        self.max_cell_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_frame.grid_columnconfigure(0, weight=1, minsize=self.width/16)
        self.max_cell_frame.grid_columnconfigure(1, weight=1, minsize=self.width * 3/16)
        self.max_cell_frame.grid(row=2, column=0, sticky="nsew")

        self.max_cell_thermometer = ThermometerProgress(self.max_cell_frame, -25, 25, 100, 150, 65, -15)
        self.max_cell_thermometer.grid(row=0, column=0, sticky="nsew")

        self.max_cell_value_frame = Frame(self.max_cell_frame, bg="black")
        self.max_cell_value_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_value_frame.grid_rowconfigure(1, weight=1)
        self.max_cell_value_frame.grid_columnconfigure(0, weight=1)
        self.max_cell_value_frame.grid(row=0, column=1, sticky="nsew")

        self.max_cell_value = CTkLabel(self.max_cell_value_frame, text="N/A°", font=("Lato", 50))
        self.max_cell_value.grid(row=0, column=0, sticky="sew")

        self.max_cell_label = CTkLabel(self.max_cell_value_frame, text="Max Cell",
                                       font=("Lato", 40), wraplength=self.width/4)
        self.max_cell_label.grid(row=1, column=0, sticky="new")

        # Create the Motor Temp Frame
        self.motor_temp_frame = Frame(self.right_frame)
        self.motor_temp_frame.grid(row=3, column=0, sticky="nsew")
        self.motor_temp_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_frame.grid_columnconfigure(0, weight=1, minsize=self.width/16)
        self.motor_temp_frame.grid_columnconfigure(1, weight=1, minsize=self.width * 3/16)

        self.motor_temp_thermometer = ThermometerProgress(self.motor_temp_frame, -25, 50, 100, 175)
        self.motor_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.motor_temp_value_frame = Frame(self.motor_temp_frame, bg="black")
        self.motor_temp_value_frame.grid(row=0, column=1, sticky="nsew")
        self.motor_temp_value_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_value_frame.grid_rowconfigure(1, weight=1)
        self.motor_temp_value_frame.grid_columnconfigure(0, weight=1)

        self.motor_temp_value = CTkLabel(self.motor_temp_value_frame, text="N/A°", font=("Lato", 50))
        self.motor_temp_value.grid(row=0, column=0, sticky="sew")

        self.motor_temp_label = CTkLabel(self.motor_temp_value_frame, text="Motor", font=("Lato", 40))
        self.motor_temp_label.grid(row=1, column=0, sticky="new")

    def update(self):
        self.update_speed()
        self.update_gforce()
        self.update_current()
        self.update_dcl()
        self.update_max_cell()
        self.update_motor_temp()

    def update_speed(self):
        speed = self.model.get_mph() if self.model.get_mph() is not None else "N/A"
        self.spedometer.set(speed)

    def update_gforce(self):
        gforce_x = self.model.get_gforce_x() if self.model.get_gforce_x() is not None else "N/A"
        gforce_y = self.model.get_gforce_y() if self.model.get_gforce_y() is not None else "N/A"
        gforce_z = self.model.get_gforce_z() if self.model.get_gforce_z() is not None else "N/A"
        self.gforce_graph.set(gforce_x, gforce_z)
        self.gforce_x_label.configure(text=f"x: {gforce_x}G")
        self.gforce_y_label.configure(text=f"y: {gforce_y}G")
        self.gforce_z_label.configure(text=f"z: {gforce_z}G")
        if (isinstance(gforce_x, int) and isinstance(gforce_y, int)):
            self.gforce_label.configure(text=f"{round(np.sqrt(np.square(gforce_x) + np.square(gforce_y)))}G")

    def update_current(self):
        current = -self.model.get_current() if self.model.get_current() is not None else "N/A"
        self.current_label.configure(text=f"{current}A")

    def update_dcl(self):
        dcl = self.model.get_dcl() if self.model.get_dcl() is not None else "N/A"
        self.dcl_label.configure(text=f"{dcl}A")

    def update_max_cell(self):
        max_cell = self.model.get_max_cell_temp() if self.model.get_max_cell_temp() is not None else "N/A"
        self.max_cell_value.configure(text=f"{max_cell}°")
        self.max_cell_thermometer.set(max_cell)

    def update_motor_temp(self):
        motor_temp = self.model.get_motor_temp() if self.model.get_motor_temp() is not None else "N/A"
        self.motor_temp_value.configure(text=f"{motor_temp}°")
        self.motor_temp_thermometer.set(motor_temp)
