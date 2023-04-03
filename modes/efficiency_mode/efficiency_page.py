from tkinter import Frame
from modes.page import Page
from models.model import Model
from components.thermometer_progress import ThermometerProgress
from components.battery_progress import BatteryProgress
from components.circular_progress import CircularProgressbar
from customtkinter import CTkLabel, CTkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Efficiency(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Efficiency")

        self.grid_rowconfigure(0, weight=1, minsize=self.height/4)
        self.grid_rowconfigure(1, weight=2, minsize=self.height/2)
        self.grid_rowconfigure(3, weight=1, minsize=self.height/4)
        self.grid_columnconfigure(0, weight=1)

        self.power_control_frame = Frame(self)
        self.power_control_frame.grid_rowconfigure(0, weight=1)
        self.power_control_frame.grid_columnconfigure(0, weight=1)
        self.power_control_frame.grid_columnconfigure(1, weight=1)
        self.power_control_frame.grid_columnconfigure(2, weight=1)
        self.power_control_frame.grid_columnconfigure(3, weight=1)
        self.power_control_frame.grid(row=0, column=0, sticky="nsew")

        self.temperatures_frame = Frame(self)
        self.temperatures_frame.grid_rowconfigure(0, weight=1)
        self.temperatures_frame.grid_columnconfigure(0, weight=1, minsize=self.width/4)
        self.temperatures_frame.grid_columnconfigure(1, weight=1, minsize=self.width/4)
        self.temperatures_frame.grid_columnconfigure(2, weight=1, minsize=self.width/4)
        self.temperatures_frame.grid_columnconfigure(3, weight=1, minsize=self.width/4)
        self.temperatures_frame.grid(row=1, column=0, sticky="nsew")

        self.graphs_frame = Frame(self)
        self.graphs_frame.grid_rowconfigure(0, weight=1)
        self.graphs_frame.grid_columnconfigure(0, weight=1, minsize=self.width/2)
        self.graphs_frame.grid_columnconfigure(1, weight=1, minsize=self.width/2)
        self.graphs_frame.grid(row=3, column=0, sticky="nsew")

        # Configure the power control frame
        # configure the fan speed control frame
        self.accumulator_power_control = Frame(self.power_control_frame, bg="black")
        self.accumulator_power_control.grid(row=0, column=0, sticky="nsew")
        self.accumulator_power_control.grid_rowconfigure(0, weight=1)
        self.accumulator_power_control.grid_columnconfigure(0, weight=2)
        self.accumulator_power_control.grid_columnconfigure(2, weight=1)

        self.accumulator_circular_progress = CircularProgressbar(self.accumulator_power_control, 25, 25, 100, 100)
        self.accumulator_circular_progress.grid(row=0, column=0, sticky="nsew")

        self.accumulator_power_control_label = CTkLabel(
            self.accumulator_power_control, text="Accumulator Max Cooling", wraplength=self.width/8, font=CTkFont(size=20, weight="bold"))
        self.accumulator_power_control_label.grid(row=0, column=2, sticky="nsew")

        # Configure the torque frame
        self.torque_power_control = Frame(self.power_control_frame, bg="black")
        self.torque_power_control.grid(row=0, column=1, sticky="nsew")
        self.torque_power_control.grid_rowconfigure(0, weight=1)
        self.torque_power_control.grid_columnconfigure(0, weight=2)
        self.torque_power_control.grid_columnconfigure(2, weight=1)

        self.torque_circular_progress = CircularProgressbar(self.torque_power_control, 25, 25, 100, 100)
        self.torque_circular_progress.grid(row=0, column=0, sticky="nsew")

        self.torque_power_control_label = CTkLabel(self.torque_power_control, text="Max Torque", font=CTkFont(
            size=20, weight="bold"), wraplength=self.width/10)
        self.torque_power_control_label.grid(row=0, column=2, sticky="nsew")

        # Configure the regen frame
        self.regen_power_control = Frame(self.power_control_frame, bg="black")
        self.regen_power_control.grid(row=0, column=2, sticky="nsew")
        self.regen_power_control.grid_rowconfigure(0, weight=1)
        self.regen_power_control.grid_columnconfigure(0, weight=2)
        self.regen_power_control.grid_columnconfigure(2, weight=1)

        self.regen_circular_progress = CircularProgressbar(self.regen_power_control, 25, 25, 100, 100)
        self.regen_circular_progress.grid(row=0, column=0, sticky="nsew")

        self.regen_power_control_label = CTkLabel(self.regen_power_control, text="Max Regen", font=CTkFont(
            size=20, weight="bold"), wraplength=self.width/10)
        self.regen_power_control_label.grid(row=0, column=2, sticky="nsew")

        # configure the motor cooling frame
        self.motor_power_control = Frame(self.power_control_frame, bg="black")
        self.motor_power_control.grid(row=0, column=3, sticky="nsew")
        self.motor_power_control.grid_rowconfigure(0, weight=1)
        self.motor_power_control.grid_columnconfigure(0, weight=2)
        self.motor_power_control.grid_columnconfigure(2, weight=1)

        self.motor_circular_progress = CircularProgressbar(self.motor_power_control, 25, 25, 100, 100)
        self.motor_circular_progress.grid(row=0, column=0, sticky="nsew")

        self.motor_power_control_label = CTkLabel(self.motor_power_control, text="Motor Max Cooling", font=CTkFont(
            size=20, weight="bold"), wraplength=self.width/10)
        self.motor_power_control_label.grid(row=0, column=2, sticky="nsew")

        # Configure the temperatures frame
        self.segment_temperature_bar_graph_frame = Frame(self.temperatures_frame)
        self.segment_temperature_bar_graph_frame.grid_rowconfigure(0, weight=1, minsize=self.height/8)
        self.segment_temperature_bar_graph_frame.grid_columnconfigure(0, weight=1)
        self.segment_temperature_bar_graph_frame.grid(row=0, column=0, sticky="nsew")

        self.segments = ["1", "2", "3", "4"]
        self.segment_temp_fig = plt.figure(facecolor="black")
        self.segment_temp_ax = self.segment_temp_fig.add_axes([0, 0.2, 0.8, 1])
        self.segment_temp_ax.set_facecolor('black')
        self.segment_temp_ax.bar(self.segments, [0, 0, 0, 0], color=["red", "orange", "yellow", "green"])
        self.segment_temp_ax.set_xticklabels(self.segments, color="white")

        self.segment_temp_canvas = FigureCanvasTkAgg(self.segment_temp_fig, master=self.segment_temperature_bar_graph_frame)
        self.segment_temp_canvas.draw()
        self.segment_temp_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # configure the max cell temperature frame
        self.max_cell_temp_frame = Frame(self.temperatures_frame)
        self.max_cell_temp_frame.grid(row=0, column=1, sticky="nsew")
        self.max_cell_temp_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_temp_frame.grid_columnconfigure(0, weight=1)
        self.max_cell_temp_frame.grid_columnconfigure(1, weight=1)

        self.max_cell_temp_thermometer = ThermometerProgress(self.max_cell_temp_frame, 0, 50, 100, 250, high=65, low=-15)
        self.max_cell_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.max_cell_value_frame = Frame(self.max_cell_temp_frame, background="black")
        self.max_cell_value_frame.grid(row=0, column=1, sticky="nsew")
        self.max_cell_value_frame.grid_rowconfigure(0, weight=1)
        self.max_cell_value_frame.grid_rowconfigure(1, weight=1)
        self.max_cell_value_frame.grid_columnconfigure(0, weight=1)

        self.max_cell_temp_value = CTkLabel(self.max_cell_value_frame, text="0", font=(CTkFont(size=50)))
        self.max_cell_temp_value.grid(row=0, column=0, sticky="sew")

        self.max_cell_temp_label = CTkLabel(self.max_cell_value_frame, text="Max Cell Temp",
                                            font=(CTkFont(size=25)), wraplength=self.width/8)
        self.max_cell_temp_label.grid(row=1, column=0, sticky="new")

        # configure the state of charge frame
        self.state_of_charge_frame = Frame(self.temperatures_frame)
        self.state_of_charge_frame.grid(row=0, column=2, sticky="nsew")
        self.state_of_charge_frame.grid_rowconfigure(0, weight=1)
        self.state_of_charge_frame.grid_columnconfigure(0, weight=1)

        self.state_of_charge_battery = BatteryProgress(self.state_of_charge_frame, 50, 50, 150, 250)
        self.state_of_charge_battery.grid(row=0, column=0, sticky="nsew")

        # configure the motor and inverter temperature frames
        self.motor_inverter_temp_frame = Frame(self.temperatures_frame)
        self.motor_inverter_temp_frame.grid(row=0, column=3, sticky="nsew")
        self.motor_inverter_temp_frame.grid_rowconfigure(0, weight=1)
        self.motor_inverter_temp_frame.grid_rowconfigure(1, weight=1)
        self.motor_inverter_temp_frame.grid_columnconfigure(0, weight=1)

        self.motor_temp_frame = Frame(self.motor_inverter_temp_frame)
        self.motor_temp_frame.grid(row=0, column=0, sticky="nsew")
        self.motor_temp_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_frame.grid_columnconfigure(0, weight=1)
        self.motor_temp_frame.grid_columnconfigure(1, weight=1)

        self.motor_temp_thermometer = ThermometerProgress(self.motor_temp_frame, 0, 50, 100, 125)
        self.motor_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.motor_temp_value_frame = Frame(self.motor_temp_frame, background="black")
        self.motor_temp_value_frame.grid(row=0, column=1, sticky="nsew")
        self.motor_temp_value_frame.grid_rowconfigure(0, weight=1)
        self.motor_temp_value_frame.grid_rowconfigure(1, weight=1)
        self.motor_temp_value_frame.grid_columnconfigure(0, weight=1)

        self.motor_temp_value = CTkLabel(self.motor_temp_value_frame, text="0", font=(CTkFont(size=50)))
        self.motor_temp_value.grid(row=0, column=0, sticky="sew")

        self.motor_temp_label = CTkLabel(self.motor_temp_value_frame, text="Motor Temp",
                                         font=(CTkFont(size=25)), wraplength=self.width/8)
        self.motor_temp_label.grid(row=1, column=0, sticky="new")

        self.inverter_temp_frame = Frame(self.motor_inverter_temp_frame)
        self.inverter_temp_frame.grid(row=1, column=0, sticky="nsew")
        self.inverter_temp_frame.grid_rowconfigure(0, weight=1)
        self.inverter_temp_frame.grid_columnconfigure(0, weight=1)
        self.inverter_temp_frame.grid_columnconfigure(1, weight=1)

        self.inverter_temp_thermometer = ThermometerProgress(self.inverter_temp_frame, 0, 50, 100, 125, -30, 80)
        self.inverter_temp_thermometer.grid(row=0, column=0, sticky="nsew")

        self.inverter_temp_value_frame = Frame(self.inverter_temp_frame, background="black")
        self.inverter_temp_value_frame.grid(row=0, column=1, sticky="nsew")
        self.inverter_temp_value_frame.grid_rowconfigure(0, weight=1)
        self.inverter_temp_value_frame.grid_rowconfigure(1, weight=1)
        self.inverter_temp_value_frame.grid_columnconfigure(0, weight=1)

        self.inverter_temp_value = CTkLabel(self.inverter_temp_value_frame, text="0", font=CTkFont(size=50))
        self.inverter_temp_value.grid(row=0, column=0, sticky="sew")

        self.inverter_temp_label = CTkLabel(self.inverter_temp_value_frame,
                                            text="Inverter Temp", font=CTkFont(size=25), wraplength=self.width/8)
        self.inverter_temp_label.grid(row=1, column=0, sticky="new")

        # Configure the graphs frame
        self.ave_cell_temp_graph_frame = Frame(self.graphs_frame)
        self.ave_cell_temp_graph_frame.grid(row=0, column=0, sticky="nsew")
        self.ave_cell_temp_graph_frame.grid_rowconfigure(0, weight=1)
        self.ave_cell_temp_graph_frame.grid_columnconfigure(0, weight=1)

        self.ave_temp_fig, self.ave_temp_ax = plt.subplots(facecolor="black", dpi=100)
        self.ave_temp_ax.set_facecolor('black')
        self.ave_temp_fig.suptitle('Average Cell Temp', color='white', fontsize=6)
        self.ave_temp_ax.set_xlabel('Time [s]', color='white')
        self.ave_temp_ax.tick_params(labelcolor='white')

        # creating the Tkinter canvas containing the Matplotlib figure
        self.ave_temp_canvas = FigureCanvasTkAgg(self.ave_temp_fig, master=self.ave_cell_temp_graph_frame)
        self.ave_temp_canvas.draw()

        # placing the canvas on the Tkinter window
        self.ave_temp_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.state_of_charge_delta_graph_frame = Frame(self.graphs_frame)
        self.state_of_charge_delta_graph_frame.grid(row=0, column=1, sticky="nsew")
        self.state_of_charge_delta_graph_frame.grid_rowconfigure(0, weight=1)
        self.state_of_charge_delta_graph_frame.grid_columnconfigure(0, weight=1)

        self.soc_delta_fig, self.soc_delta_ax = plt.subplots(facecolor="black", dpi=100)
        self.soc_delta_ax.set_facecolor('black')
        self.soc_delta_fig.suptitle('Change in State of Charge', color='white', fontsize=6)
        self.soc_delta_ax.set_xlabel('Time [s]', color='white')
        self.soc_delta_ax.tick_params(labelcolor='white')

        # creating the Tkinter canvas containing the Matplotlib figure
        self.ave_temp_canvas = FigureCanvasTkAgg(self.soc_delta_fig, master=self.state_of_charge_delta_graph_frame)
        self.ave_temp_canvas.draw()

        # placing the canvas on the Tkinter window
        self.ave_temp_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def color_transformer(self, value):
        if isinstance(value, str):
            return "white"
        if value < 0:
            return "purple"
        if value <= 20:
            return "blue"
        if value <= 30:
            return "green"
        if value <= 40:
            return "yellow"
        if value <= 50:
            return "orange"
        if value > 50:
            return "red"

    def update(self):
        self.update_fan_cooling()
        self.update_torque_power()
        self.update_regen_power()
        self.update_motor_power()
        self.update_motor_temp()
        self.update_max_cell_temp()
        self.update_state_of_charge()
        self.update_inverter_temp()
        self.update_ave_cell_temp()
        self.update_state_of_charge_delta()
        self.update_pack_segments()

    def update_fan_cooling(self):
        percentage = self.model.get_fan_power() if self.model.get_fan_power() is not None else "N/A"
        self.accumulator_circular_progress.set(percentage)

    def update_torque_power(self):
        percentage = self.model.get_torque_power() if self.model.get_torque_power() is not None else "N/A"
        self.torque_circular_progress.set(percentage)

    def update_regen_power(self):
        percentage = self.model.get_regen_power() if self.model.get_regen_power() is not None else "N/A"
        self.regen_circular_progress.set(percentage)

    def update_motor_power(self):
        percentage = self.model.get_motor_power() if self.model.get_motor_power() is not None else "N/A"
        self.motor_circular_progress.set(percentage)

    def update_pack_segments(self):
        segment1_temp = self.model.get_segment1_temp() if self.model.get_segment1_temp() is not None else "N/A"
        segment2_temp = self.model.get_segment2_temp() if self.model.get_segment2_temp() is not None else "N/A"
        segment3_temp = self.model.get_segment3_temp() if self.model.get_segment3_temp() is not None else "N/A"
        segment4_temp = self.model.get_segment4_temp() if self.model.get_segment4_temp() is not None else "N/A"
        self.segment_temp_ax.clear()
        self.segment_temp_ax.bar(self.segments, [segment1_temp,
                                 segment2_temp, segment3_temp, segment4_temp], color=[self.color_transformer(segment1_temp), self.color_transformer(segment2_temp), self.color_transformer(segment3_temp), self.color_transformer(segment4_temp)])
        self.segment_temp_ax.set_xticklabels(self.segments, color="white")
        self.segment_temp_canvas.draw()

    def update_max_cell_temp(self):
        temp = self.model.get_max_cell_temp() if self.model.get_max_cell_temp() is not None else "N/A"
        self.max_cell_temp_thermometer.set(temp)
        self.max_cell_temp_value.configure(text=str(temp))

    def update_state_of_charge(self):
        soc = self.model.get_state_of_charge() if self.model.get_state_of_charge() is not None else "N/A"
        self.state_of_charge_battery.set(soc)

    def update_inverter_temp(self):
        temp = self.model.get_inverter_temp() if self.model.get_inverter_temp() is not None else "N/A"
        self.inverter_temp_thermometer.set(temp)
        self.inverter_temp_value.configure(text=str(temp))

    def update_motor_temp(self):
        temp = self.model.get_motor_temp() if self.model.get_motor_temp() is not None else "N/A"
        self.motor_temp_thermometer.set(temp)
        self.motor_temp_value.configure(text=str(temp))

    def update_ave_cell_temp(self):
        temps = self.model.average_cell_temps
        self.ave_temp_ax.clear()
        self.ave_temp_ax.plot(temps, color='red')

    def update_state_of_charge_delta(self):
        soc_deltas = self.model.state_of_charge_deltas
        self.soc_delta_ax.clear()
        self.soc_delta_ax.plot(soc_deltas, color='purple')
