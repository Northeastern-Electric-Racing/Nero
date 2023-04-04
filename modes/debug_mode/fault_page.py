from tkinter import Frame
from customtkinter import CTkLabel, CTkFont
from modes.page import Page
from models.model import Model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modes.debug_mode.debug_utils import FaultInstance


class Fault(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Fault")
        self.fault_index = 0
        self.prev_fault_index = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=self.width/4)
        self.grid_columnconfigure(1, weight=1, minsize=self.width/2)
        self.grid_columnconfigure(2, weight=1, minsize=self.width/4)

        # The left frame will contain the cell info
        self.cell_info_frame = Frame(self)
        self.cell_info_frame.grid(row=0, column=0, sticky="nsew")

        self.cell_info_frame.grid_rowconfigure(0, weight=1)
        self.cell_info_frame.grid_rowconfigure(1, weight=1)
        self.cell_info_frame.grid_rowconfigure(2, weight=1)
        self.cell_info_frame.grid_columnconfigure(0, weight=1)

        # The middle frame will contain the fault names
        self.fault_info_frame = Frame(self)
        self.fault_info_frame.grid(row=0, column=1, sticky="nsew")
        self.fault_info_frame.grid_rowconfigure(0, weight=1)
        self.fault_info_frame.grid_columnconfigure(0, weight=1)

        # The right frame will contain the current fault graphs
        self.current_info_frame = Frame(self)
        self.current_info_frame.grid(row=0, column=2, sticky="nsew")
        self.current_info_frame.grid_rowconfigure(0, weight=1)
        self.current_info_frame.grid_columnconfigure(0, weight=1)

        # The high cell temp and voltage
        self.high_cell_frame = CellInfoFrame(self.cell_info_frame, "⬆")
        self.high_cell_frame.grid(row=0, column=0, sticky="nsew")

        # The average cell temp and voltage
        self.avg_cell_frame = CellInfoFrame(self.cell_info_frame, "-")
        self.avg_cell_frame.grid(row=1, column=0, sticky="nsew")

        # The low cell temp and voltage
        self.low_cell_frame = CellInfoFrame(self.cell_info_frame, "⬇")
        self.low_cell_frame.grid(row=2, column=0, sticky="nsew")

        # The fault name list
        self.fault_list_frame = Frame(self.fault_info_frame, bg="black")
        self.fault_list_frame.grid(row=0, column=0, sticky="nsew")
        self.fault_list_frame.grid_rowconfigure(0, weight=1)
        self.fault_list_frame.grid_columnconfigure(0, weight=1)

        temp_fault_label = CTkLabel(self.fault_list_frame, text="No Faults Detected", font=CTkFont(size=50))
        temp_fault_label.grid(row=0, column=0, sticky="nsew")

        # The current fault graph
        # the figure that will contain the plot
        self.currents = ["CCL", "CUR", "DCL"]
        self.fig = plt.figure(facecolor="black")
        self.ax = self.fig.add_axes([0, 0.1, 0.9, 1])
        self.ax.set_facecolor('black')
        self.ax.bar(self.currents, [1, 2, 3], color="red")
        self.ax.set_xticklabels(self.currents, color="white")

        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.current_info_frame)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def update(self):
        if len(self.model.fault_instances) > 0:
            self.fault_instance: FaultInstance = self.model.fault_instances[self.fault_index]
            self.update_high_cell()
            self.update_avg_cell()
            self.update_low_cell()
            self.update_fault_list()
            self.update_current_graph()

    def up_button_pressed(self):
        self.prev_fault_index = self.fault_index
        self.fault_index = (self.fault_index + 1) if self.fault_index + 1 < len(self.model.fault_instances) else 0

    def down_button_pressed(self):
        self.prev_fault_index = self.fault_index
        self.fault_index = (self.fault_index - 1) if self.fault_index - 1 >= 0 else len(self.model.fault_instances) - 1

    def enter_button_pressed(self):
        self.fault_index = 0 if self.fault_index != 0 else self.prev_fault_index

    def update_high_cell(self):
        self.high_cell_frame.cell_temp_label.configure(text=(str(self.fault_instance.max_cell_temp) + "°"))
        self.high_cell_frame.cell_voltage_label.configure(text=(str(self.fault_instance.max_cell_voltage) + "V"))

    def update_avg_cell(self):
        self.avg_cell_frame.cell_temp_label.configure(text=(str(self.fault_instance.average_cell_temp) + "°"))
        self.avg_cell_frame.cell_voltage_label.configure(text=(str(self.fault_instance.average_cell_voltage) + "V"))

    def update_low_cell(self):
        self.low_cell_frame.cell_temp_label.configure(text=(str(self.fault_instance.min_cell_temp) + "°"))
        self.low_cell_frame.cell_voltage_label.configure(text=(str(self.fault_instance.min_cell_voltage) + "V"))

    def update_fault_list(self):
        for widget in self.fault_list_frame.winfo_children():
            widget.destroy()

        for i, fault in enumerate(self.fault_instance.faults):
            fault_label = CTkLabel(self.fault_list_frame, text=fault,
                                   font=CTkFont(size=30, weight="bold", family="Lato"))
            fault_label.grid(row=i, column=0, sticky="nsew")

    def update_current_graph(self):
        self.ax.clear()
        self.ax.bar(self.currents, [self.fault_instance.ccl, self.fault_instance.pack_current, self.fault_instance.dcl])
        self.ax.set_xticklabels(self.currents, color="white")
        self.canvas.draw()


class CellInfoFrame(Frame):
    def __init__(self, parent: Frame, icon: str):
        super().__init__(parent, background="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        cell_font = CTkFont(size=40, weight="bold", family="Lato")
        self.cell_icon = CTkLabel(self, text=icon, font=cell_font)
        self.cell_icon.grid(row=0, column=0, sticky="nsew")

        self.cell_temp_label = CTkLabel(self, text="N/A°", font=cell_font)
        self.cell_temp_label.grid(row=0, column=1, sticky="nsew")

        self.cell_voltage_label = CTkLabel(self, text="N/AV", font=cell_font)
        self.cell_voltage_label.grid(row=0, column=2, sticky="nsew")
