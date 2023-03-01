from tkinter import Frame, Canvas, ttk
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

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # The top and bottom frame that compose the frame
        self.top_frame = Frame(self, width=1024, height=427.5, bg="black")
        self.bottom_frame = Frame(self, width=1024, height=142.5, bg="black",
                                  highlightbackground="gray", highlightthickness=1)

        self.top_frame.grid(row=0, column=0, sticky="s")
        self.top_frame.grid_propagate(False)

        self.bottom_frame.grid(row=1, column=0, sticky="n")
        self.bottom_frame.grid_propagate(False)

        # Create the three frames that compose the bottom frame
        self.left_frame = Frame(self.top_frame, width=341.33, height=427.5, bg="black",
                                highlightbackground="gray", highlightthickness=1)
        self.middle_frame = Frame(self.top_frame, width=341.33, height=427.5, bg="black",
                                  highlightbackground="gray", highlightthickness=1)
        self.right_frame = Frame(self.top_frame, width=341.33, height=427.5, bg="black",
                                 highlightbackground="gray", highlightthickness=1)

        self.left_frame.grid(row=0, column=0, sticky="s")
        self.left_frame.grid_propagate(False)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.middle_frame.grid(row=0, column=1, sticky="s")
        self.middle_frame.grid_propagate(False)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid(row=0, column=2, sticky="s")
        self.right_frame.grid_propagate(False)
        self.right_frame.grid_rowconfigure(3, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # the figure that will contain the plot
        # self.fig, self.ax = plt.subplots(facecolor="black", figsize=(10.24, 1.425), dpi=100)
        self.fig, self.ax = plt.subplots(facecolor="black", figsize=(5.12, .7125), dpi=100)
        self.ax.set_facecolor('black')
        self.fig.suptitle('Pack Temp', color='white', fontsize=5)
        self.ax.set_xlabel('Time [s]', color='white')
        self.ax.tick_params(labelcolor='white', labelsize=5)

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="w")

        # Create The top left frame
        self.current_frame = Frame(self.left_frame, width=341.33, height=250, bg="black")
        self.current_frame.grid(row=0, column=0, sticky="s")
        self.current_frame.grid_propagate(False)
        self.current_frame.grid_rowconfigure(0, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)

        self.current_value = customtkinter.CTkLabel(
            self.current_frame, text="N/A", font=customtkinter.CTkFont(size=125, weight="bold"))
        self.current_value.grid(row=0, column=0, sticky="s")

        self.current_label = customtkinter.CTkLabel(self.left_frame, text="Current", font=customtkinter.CTkFont(size=20))
        self.current_label.grid(row=1, column=0, sticky="n")

        # Create the top right frame
        self.max_cell_frame = Frame(self.right_frame, width=341.33, height=106.875, bg="black")

        self.min_cell_frame = Frame(self.right_frame, width=341.33, height=106.875, bg="black")

        self.cell_delta_frame = Frame(self.right_frame, width=341.33, height=106.875, bg="black")

        self.pack_voltage_frame = Frame(self.right_frame, width=341.33, height=106.875, bg="black")

        self.max_cell_frame.grid(row=0, column=0, sticky="s")
        self.max_cell_frame.grid_propagate(False)
        self.max_cell_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_frame.grid_columnconfigure(1, weight=1)

        self.min_cell_frame.grid(row=1, column=0, sticky="s")
        self.min_cell_frame.grid_propagate(False)
        self.min_cell_frame.grid_rowconfigure(0, weight=1)
        self.min_cell_frame.grid_columnconfigure(1, weight=1)

        self.cell_delta_frame.grid(row=2, column=0, sticky="s")
        self.cell_delta_frame.grid_propagate(False)
        self.cell_delta_frame.grid_rowconfigure(0, weight=1)
        self.cell_delta_frame.grid_columnconfigure(1, weight=1)

        self.pack_voltage_frame.grid(row=3, column=0, sticky="s")
        self.pack_voltage_frame.grid_propagate(False)
        self.pack_voltage_frame.grid_rowconfigure(0, weight=1)
        self.pack_voltage_frame.grid_columnconfigure(1, weight=1)

        self.max_cell_label = customtkinter.CTkLabel(
            self.max_cell_frame, text="Max Cell: ", font=customtkinter.CTkFont(size=30))
        self.max_cell_value = customtkinter.CTkLabel(
            self.max_cell_frame, text="N/A", font=customtkinter.CTkFont(size=50, weight="bold"))

        self.max_cell_label.grid(row=0, column=0, sticky="e", padx=15)
        self.max_cell_value.grid(row=0, column=1, sticky="w")

        self.min_cell_label = customtkinter.CTkLabel(
            self.min_cell_frame, text="Min Cell: ", font=customtkinter.CTkFont(size=30))
        self.min_cell_value = customtkinter.CTkLabel(
            self.min_cell_frame, text="N/A", font=customtkinter.CTkFont(size=50, weight="bold"))

        self.min_cell_label.grid(row=0, column=0, sticky="e", padx=15)
        self.min_cell_value.grid(row=0, column=1, sticky="w")

        self.cell_delta_label = customtkinter.CTkLabel(
            self.cell_delta_frame, text="Cell Delta: ", font=customtkinter.CTkFont(size=30))
        self.cell_delta_value = customtkinter.CTkLabel(
            self.cell_delta_frame, text="N/A", font=customtkinter.CTkFont(size=50, weight="bold"))

        self.cell_delta_label.grid(row=0, column=0, sticky="e", padx=15)
        self.cell_delta_value.grid(row=0, column=1, sticky="w")

        self.pack_voltage_label = customtkinter.CTkLabel(
            self.pack_voltage_frame, text="Pack Voltage: ", font=customtkinter.CTkFont(size=30))
        self.pack_voltage_value = customtkinter.CTkLabel(
            self.pack_voltage_frame, text="N/A", font=customtkinter.CTkFont(size=50, weight="bold"))

        self.pack_voltage_label.grid(row=0, column=0, sticky="e", padx=15)
        self.pack_voltage_value.grid(row=0, column=1, sticky="w")

        # Create the middle Frame
        self.circle_canvas = Canvas(self.middle_frame, width=341.33, height=427.5, bg="black")

        self.circle = self.circle_canvas.create_oval(10, 48.25, 331, 379.25, fill="black", outline="white", width=5)

        self.circle_canvas.grid(row=0, column=0, sticky="n")

        # Build the progress bar
        self.progress_bar_frame = Frame(self.middle_frame, width=200, height=50, bg="gray")
        self.progress_bar_frame.grid_propagate(False)
        self.progress_bar_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.progress_bar_frame.grid_rowconfigure(0, weight=1)
        self.progress_bar_frame.grid_columnconfigure(0, weight=1)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='green', background='green', border=16)
        self.progress_bar = ttk.Progressbar(self.progress_bar_frame, orient="horizontal",
                                            length=200, mode="determinate", style="red.Horizontal.TProgressbar")
        self.progress_bar.grid(row=0, column=0, sticky="nsew")

        # Build the SOC label
        self.soc_frame = Frame(self.middle_frame, width=200, height=50, bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.soc_frame.place(relx=0.5, rely=0.3, anchor='center')

        self.soc_label = customtkinter.CTkLabel(
            self.soc_frame, text="N/A", font=customtkinter.CTkFont(size=40))
        self.soc_label.grid(row=0, column=0, sticky="w")

        # Build the charging image
        self.charging_frame = Frame(self.middle_frame, width=200, height=50, bg="black")
        self.charging_frame.place(relx=0.5, rely=0.7, anchor='center')

        self.charging_frame.grid_rowconfigure(0, weight=1)
        self.charging_frame.grid_columnconfigure(0, weight=1)

        self.charging_image = BitmapImage(file="images/battery.xbm", foreground="yellow", background="black")

        self.charging_label = customtkinter.CTkLabel(self.charging_frame, image=self.charging_image, text="")
        self.charging_label.grid(row=0, column=0, sticky="nsew")

    def update(self):
        self.update_progress_bar()
        self.update_pack_temp_graph()
        self.update_soc_label()
        self.update_current_value()

    def update_progress_bar(self):
        self.soc = self.model.get_state_of_charge()
        self.progress_bar["value"] = self.soc

    def update_soc_label(self):
        self.soc_label.configure(text=str(self.soc) + "%")

    def update_current_value(self):
        current = self.model.get_current()
        self.current_value.configure(text=str(current) + "A")

    def update_pack_temp_graph(self):
        # plotting the graph
        self.ax.clear()
        y = self.model.pack_temp_data
        self.ax.plot(y[0: 600] if len(y) > 600 else y, color="blue")
        self.ax.invert_xaxis()
        self.canvas.draw()
