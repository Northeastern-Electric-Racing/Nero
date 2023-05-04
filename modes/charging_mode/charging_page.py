from tkinter import Frame, ttk
from modes.page import Page
from models.model import Model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from PIL.ImageTk import BitmapImage


class Charging(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Charging")
        self.model = model

        self.grid_rowconfigure(0, weight=1, minsize=self.height * 4 / 5)
        self.grid_rowconfigure(1, weight=1, minsize=self.height / 5)
        self.grid_columnconfigure(0, weight=1, minsize=self.width)

        # The top and bottom frame that compose the frame
        self.top_frame = Frame(self, bg="black")
        self.bottom_frame = Frame(
            self, bg="black", highlightbackground="gray", highlightthickness=1
        )

        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1, minsize=self.width / 3)
        self.top_frame.grid_columnconfigure(1, weight=1, minsize=self.width / 3)
        self.top_frame.grid_columnconfigure(2, weight=1, minsize=self.width / 3)

        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        # Create the three frames that compose the top frame
        self.left_frame = Frame(
            self.top_frame, bg="black", highlightbackground="gray", highlightthickness=1
        )
        self.middle_frame = Frame(
            self.top_frame, bg="black", highlightbackground="gray", highlightthickness=1
        )
        self.right_frame = Frame(
            self.top_frame, bg="black", highlightbackground="gray", highlightthickness=1
        )

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_rowconfigure(0, weight=1, minsize=self.height * 2 / 5)
        self.left_frame.grid_rowconfigure(1, weight=1, minsize=self.height * 1 / 5)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.middle_frame.grid(row=0, column=1, sticky="nsew")
        self.middle_frame.grid_rowconfigure(2, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid(row=0, column=2, sticky="nsew")
        for x in range(4):
            self.right_frame.grid_rowconfigure(x, weight=1, minsize=self.height * 1 / 5)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # the figure that will contain the plot
        self.fig, self.ax = plt.subplots(facecolor="black", dpi=100)
        self.ax.set_facecolor("black")
        self.fig.suptitle("Pack Temp", color="white", fontsize=5)
        self.ax.set_xlabel("Time [s]", color="white")
        self.ax.tick_params(labelcolor="white", labelsize=5)

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Create The top left frame
        self.current_value = customtkinter.CTkLabel(
            self.left_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=125, weight="bold"),
        )
        self.current_value.grid(row=0, column=0, sticky="sew")

        self.current_label = customtkinter.CTkLabel(
            self.left_frame, text="Current", font=customtkinter.CTkFont(size=20)
        )
        self.current_label.grid(row=1, column=0, sticky="new")

        # Create the top right frame
        self.max_cell_frame = Frame(self.right_frame, bg="black")

        self.min_cell_frame = Frame(self.right_frame, bg="black")

        self.cell_delta_frame = Frame(self.right_frame, bg="black")

        self.pack_voltage_frame = Frame(self.right_frame, bg="black")

        self.max_cell_frame.grid(row=0, column=0, sticky="nsew")
        self.max_cell_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_frame.grid_columnconfigure(1, weight=1)

        self.min_cell_frame.grid(row=1, column=0, sticky="nsew")
        self.min_cell_frame.grid_rowconfigure(0, weight=1)
        self.min_cell_frame.grid_columnconfigure(1, weight=1)

        self.cell_delta_frame.grid(row=2, column=0, sticky="nsew")
        self.cell_delta_frame.grid_rowconfigure(0, weight=1)
        self.cell_delta_frame.grid_columnconfigure(1, weight=1)

        self.pack_voltage_frame.grid(row=3, column=0, sticky="nsew")
        self.pack_voltage_frame.grid_rowconfigure(0, weight=1)
        self.pack_voltage_frame.grid_columnconfigure(1, weight=1)

        self.max_cell_label = customtkinter.CTkLabel(
            self.max_cell_frame,
            text="Max Cell: ",
            font=customtkinter.CTkFont(size=25, weight="bold"),
        )
        self.max_cell_value = customtkinter.CTkLabel(
            self.max_cell_frame, text="N/A", font=customtkinter.CTkFont(size=25)
        )

        self.max_cell_label.grid(row=0, column=0, sticky="e", padx=15)
        self.max_cell_value.grid(row=0, column=1, sticky="w")

        self.min_cell_label = customtkinter.CTkLabel(
            self.min_cell_frame,
            text="Min Cell: ",
            font=customtkinter.CTkFont(size=25, weight="bold"),
        )
        self.min_cell_value = customtkinter.CTkLabel(
            self.min_cell_frame, text="N/A", font=customtkinter.CTkFont(size=25)
        )

        self.min_cell_label.grid(row=0, column=0, sticky="e", padx=15)
        self.min_cell_value.grid(row=0, column=1, sticky="w")

        self.cell_delta_label = customtkinter.CTkLabel(
            self.cell_delta_frame,
            text="Cell Delta: ",
            font=customtkinter.CTkFont(size=25, weight="bold"),
        )
        self.cell_delta_value = customtkinter.CTkLabel(
            self.cell_delta_frame, text="N/A", font=customtkinter.CTkFont(size=25)
        )

        self.cell_delta_label.grid(row=0, column=0, sticky="e", padx=15)
        self.cell_delta_value.grid(row=0, column=1, sticky="w")

        self.pack_voltage_label = customtkinter.CTkLabel(
            self.pack_voltage_frame,
            text="Pack Voltage: ",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        self.pack_voltage_value = customtkinter.CTkLabel(
            self.pack_voltage_frame, text="N/A", font=customtkinter.CTkFont(size=30)
        )

        self.pack_voltage_label.grid(row=0, column=0, sticky="e", padx=15)
        self.pack_voltage_value.grid(row=0, column=1, sticky="w")

        # Create the middle frame
        self.battery_progress_frame = Frame(self.middle_frame, bg="black")
        self.battery_progress_frame.grid(row=0, column=0, sticky="n")
        self.battery_progress_frame.grid_rowconfigure(
            0, weight=1, minsize=self.height * 2 / 5
        )
        self.battery_progress_frame.grid_rowconfigure(1, weight=1)
        self.battery_progress_frame.grid_columnconfigure(0, weight=1)

        # Build the progress bar
        self.progress_bar_frame = Frame(self.battery_progress_frame, bg="black")
        self.progress_bar_frame.grid(row=0, column=0, sticky="ew")
        self.progress_bar_frame.grid_rowconfigure(0, weight=1)
        self.progress_bar_frame.grid_columnconfigure(0, weight=1)

        s = ttk.Style()
        s.theme_use("classic")
        s.configure(
            "green.Vertical.TProgressbar", foreground="green", background="green"
        )
        self.progress_bar = ttk.Progressbar(
            self.progress_bar_frame,
            orient="vertical",
            length=150,
            mode="determinate",
            style="green.Vertical.TProgressbar",
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(75, 25))

        # Build the SOC label
        self.soc_frame = Frame(self.middle_frame, bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.soc_frame.grid(row=1, column=0, sticky="n")

        self.soc_label = customtkinter.CTkLabel(
            self.soc_frame, text="N/A", font=customtkinter.CTkFont(size=40)
        )
        self.soc_label.grid(row=0, column=0, sticky="n")

        # Build the battery image
        self.charging_frame = Frame(self.battery_progress_frame, bg="black")
        self.charging_frame.grid(row=0, column=1, sticky="nsew", padx=15)

        self.charging_frame.grid_rowconfigure(0, weight=1)
        self.charging_frame.grid_columnconfigure(0, weight=1)

        self.charging_image = BitmapImage(
            file="images/largeBatteryHorizontal.xbm",
            foreground="white",
            background="black",
        )
        self.charging_label = customtkinter.CTkLabel(
            self.charging_frame, image=self.charging_image, text=""
        )
        self.charging_label.grid(row=0, column=0, sticky="ew")

        # Build the burning cells image
        self.burning_cells_frame = Frame(self.middle_frame, bg="black")
        self.burning_cells_frame.grid(row=2, column=0, sticky="nsew")
        self.burning_cells_frame.grid_rowconfigure(0, weight=1)
        self.burning_cells_frame.grid_columnconfigure(0, weight=1)

        self.burning_cells_image = BitmapImage(
            file="images/burningIcon.xbm", foreground="orange", background="black"
        )

        self.voltage_image = BitmapImage(
            file="images/voltageIcon.xbm", foreground="green", background="black"
        )

        self.default_image = None

        self.current_image_label = customtkinter.CTkLabel(
            self.burning_cells_frame, image=self.default_image, text=""
        )
        self.current_image_label.grid(row=0, column=0, sticky="nsew")

    def update(self):
        self.update_progress_bar()
        self.update_pack_temp_graph()
        self.update_soc_label()
        self.update_current_value_and_battery_image()
        self.update_max_cell_value()
        self.update_min_cell_value()
        self.update_cell_delta_value()
        self.update_pack_voltage_value()
        self.update_burning_cells()

    def update_progress_bar(self):
        self.soc = (
            int(self.model.get_state_of_charge())
            if self.model.get_state_of_charge() is not None
            else 0
        )
        self.progress_bar["value"] = self.soc

    def update_burning_cells(self):
        is_burning = (
            self.model.get_burning_cells()
            if self.model.get_burning_cells() is not None
            else -1
        )

        if is_burning == -1:
            self.current_image_label.configure(image=self.default_image)
            return

        self.current_image_label.configure(
            image=self.burning_cells_image
        ) if is_burning == 1 else self.current_image_label.configure(
            image=self.voltage_image
        )

    def update_soc_label(self):
        self.soc_label.configure(text=str(self.soc) + "%")

    def update_max_cell_value(self):
        max_cell = (
            self.model.get_max_cell_voltage()
            if self.model.get_max_cell_voltage() is not None
            else "N/A"
        )
        max_cell_chip_number = (
            int(self.model.get_max_cell_voltage_chip_number())
            if self.model.get_max_cell_voltage_chip_number() is not None
            else "N/A"
        )
        max_cell_cell_number = (
            int(self.model.get_max_cell_voltage_cell_number())
            if self.model.get_max_cell_voltage_cell_number() is not None
            else "N/A"
        )
        self.max_cell_value.configure(
            text=str(max_cell)
            + "V, #"
            + str(max_cell_chip_number)
            + "-"
            + str(max_cell_cell_number)
        )

    def update_min_cell_value(self):
        min_cell = (
            self.model.get_min_cell_voltage()
            if self.model.get_min_cell_voltage() is not None
            else "N/A"
        )
        min_cell_chip_number = (
            int(self.model.get_min_cell_voltage_chip_number())
            if self.model.get_min_cell_voltage_chip_number() is not None
            else "N/A"
        )
        min_cell_cell_number = (
            int(self.model.get_min_cell_voltage_cell_number())
            if self.model.get_min_cell_voltage_cell_number() is not None
            else "N/A"
        )
        self.min_cell_value.configure(
            text=str(min_cell)
            + "V, #"
            + str(min_cell_chip_number)
            + "-"
            + str(min_cell_cell_number)
        )

    def update_cell_delta_value(self):
        cell_delta = (
            self.model.get_cell_delta()
            if self.model.get_ave_cell_voltage() is not None
            else "N/A"
        )
        self.cell_delta_value.configure(text=str(cell_delta) + "V")

    def update_pack_voltage_value(self):
        pack_voltage = (
            self.model.get_pack_voltage()
            if self.model.get_pack_voltage() is not None
            else "N/A"
        )
        self.pack_voltage_value.configure(text=str(pack_voltage) + "V")

    def update_current_value_and_battery_image(self):
        current = (
            self.model.get_current() if self.model.get_current() is not None else "N/A"
        )
        self.current_value.configure(text=str(current) + "A")
        self.charging_label.configure(
            image=BitmapImage(
                file="images/largeBatteryHorizontal.xbm", foreground="yellow"
            )
            if isinstance(current, float) and current <= -0.7
            else BitmapImage(
                file="images/largeBatteryHorizontal.xbm", foreground="white"
            )
        )

    def update_pack_temp_graph(self):
        # plotting the graph
        self.ax.clear()
        y = self.model.pack_temp_data if self.model.pack_temp_data is not None else []
        self.ax.plot(y[0:600] if len(y) > 600 else y, color="blue")
        self.ax.invert_xaxis()
        self.canvas.draw()
