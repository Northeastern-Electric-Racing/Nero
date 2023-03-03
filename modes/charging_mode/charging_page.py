import math
import tkinter as tk
from tkinter import Frame, Canvas, ttk, PhotoImage
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

        self.orbit_delay = 10
        self.circular_path_increment = 0

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
        self.middle_frame.grid_rowconfigure(2, weight=1)
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
      #   self.circle_canvas = Canvas(self.middle_frame, width=341.33, height=427.5, bg="black")

      #   self.circle = self.circle_canvas.create_oval(10, 48.25, 331, 379.25, fill="black", outline="white", width=5)

      #   self.circle_canvas.grid(row=0, column=0, sticky="n")

        self.battery_progress_frame = Frame(self.middle_frame, width=341.33, height=200, bg="black")
        self.battery_progress_frame.grid(row=0, column=0, sticky="n")
        self.battery_progress_frame.grid_propagate(False)
        self.battery_progress_frame.grid_rowconfigure(1, weight=1)
        self.battery_progress_frame.grid_columnconfigure(0, weight=1)

        # Build the progress bar
        self.progress_bar_frame = Frame(self.battery_progress_frame, height=200, bg="black")
        self.grid_propagate(False)
        self.progress_bar_frame.grid(row=0, column=0, sticky="ew")
        self.progress_bar_frame.grid_rowconfigure(0, weight=1)
        self.progress_bar_frame.grid_columnconfigure(0, weight=1)

        s = ttk.Style()
        s.theme_use('classic')
        s.configure("green.Vertical.TProgressbar", foreground='green', background='green')
        self.progress_bar = ttk.Progressbar(self.progress_bar_frame, orient="vertical",
                                            length=150, mode="determinate", style="green.Vertical.TProgressbar")
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(75, 25))

        # Build the SOC label
        self.soc_frame = Frame(self.middle_frame, width=341, height=50, bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.soc_frame.grid(row=1, column=0, sticky="n")

        self.soc_label = customtkinter.CTkLabel(
            self.soc_frame, text="N/A", font=customtkinter.CTkFont(size=40))
        self.soc_label.grid(row=0, column=0, sticky="n")

        # Build the battery image
        self.charging_frame = Frame(self.battery_progress_frame, width=341/2, height=200, bg="black")
        self.charging_frame.grid(row=0, column=1, sticky="nsew", padx=15)

        self.charging_frame.grid_rowconfigure(0, weight=1)
        self.charging_frame.grid_columnconfigure(0, weight=1)
        self.charging_frame.grid_propagate(False)

        self.charging_image = BitmapImage(
            file="images/largeBatteryHorizontal.xbm", foreground="white", background="black")
        self.charging_label = customtkinter.CTkLabel(self.charging_frame, image=self.charging_image, text="")
        self.charging_label.grid(row=0, column=0, sticky="ew")

        # Build the burning cells image
        self.burning_cells_frame = Frame(self.middle_frame, bg="black")
        self.burning_cells_frame.grid(row=2, column=0, sticky="nsew")
        self.burning_cells_frame.grid_rowconfigure(0, weight=1)
        self.burning_cells_frame.grid_columnconfigure(0, weight=1)
        self.burning_cells_frame.grid_propagate(False)

        self.burning_cells_image = BitmapImage(file="images/burningIcon.xbm", foreground="orange", background="black")

        self.voltage_image = BitmapImage(file="images/voltageIcon.xbm", foreground="green", background="black")

        self.default_image = None

        self.current_image_label = customtkinter.CTkLabel(
            self.burning_cells_frame, image=self.default_image, text="")
        self.current_image_label.grid(row=0, column=0, sticky="nsew")

    def update(self):
        self.update_progress_bar()
        self.update_pack_temp_graph()
        self.update_soc_label()
        self.update_current_value()
        self.update_max_cell_value()
        self.update_min_cell_value()
        self.update_cell_delta_value()
        self.update_pack_voltage_value()
        self.update_charging_image()
        self.update_burning_cells()

    def update_progress_bar(self):
        self.soc = self.model.get_state_of_charge() if self.model.get_state_of_charge() is not None else 0
        self.progress_bar["value"] = self.soc

    def update_burning_cells(self):
        is_burning = self.model.get_burning_cells() if self.model.get_burning_cells() is not None else -1

        if is_burning == -1:
            self.current_image_label.configure(image=self.default_image)
            return

        self.current_image_label.configure(
            image=self.burning_cells_image) if is_burning == 1 else self.current_image_label.configure(image=self.voltage_image)

    def update_charging_image(self):
        self.is_charging = self.model.get_charging() if self.model.get_charging() is not None else 0
        print(self.is_charging)
        self.charging_label.configure(image=BitmapImage(file="images/largeBatteryHorizontal.xbm",
                                                        foreground="yellow") if self.is_charging == 1 else BitmapImage(file="images/largeBatteryHorizontal.xbm",
                                                                                                                       foreground="white"))

    def update_soc_label(self):
        self.soc_label.configure(text=str(self.soc) + "%")

    def update_max_cell_value(self):
        max_cell = self.model.get_max_cell() if self.model.get_max_cell() is not None else "N/A"
        self.max_cell_value.configure(text=str(max_cell) + "V")

    def update_min_cell_value(self):
        min_cell = self.model.get_min_cell() if self.model.get_min_cell() is not None else "N/A"
        self.min_cell_value.configure(text=str(min_cell) + "V")

    def update_cell_delta_value(self):
        cell_delta = self.model.get_cell_delta() if self.model.get_cell_delta() is not None else "N/A"
        self.cell_delta_value.configure(text=str(cell_delta) + "V")

    def update_pack_voltage_value(self):
        pack_voltage = self.model.get_pack_voltage() if self.model.get_pack_voltage() is not None else "N/A"
        self.pack_voltage_value.configure(text=str(pack_voltage) + "V")

    def update_current_value(self):
        current = self.model.get_current() if self.model.get_current() is not None else "N/A"
        self.current_value.configure(text=str(current) + "A")
        #   self.circular_path_increment = current * 0.1

    def update_pack_temp_graph(self):
        # plotting the graph
        self.ax.clear()
        y = self.model.pack_temp_data if self.model.pack_temp_data is not None else []
        self.ax.plot(y[0: 600] if len(y) > 600 else y, color="blue")
        self.ax.invert_xaxis()
        self.canvas.draw()

#   # Create Animation Object
        #   self.sol_obj = Celestial(341/2, 427.5/2, 25)
        #   planet_obj1 = Celestial(341/2+160, 250, 5)
        #   self.planet1 = self.circle_canvas.create_oval(planet_obj1.bounds(), fill='gray', width=0)

        #   orbital_radius = math.hypot(self.sol_obj.x - planet_obj1.x, self.sol_obj.y - planet_obj1.y)
        #   path_iter = self.circular_path(self.sol_obj.x, self.sol_obj.y, orbital_radius, self.circular_path_increment)
        #   next(path_iter)  # prime generator
        #   self.after(self.orbit_delay, self.update_position, self.circle_canvas, self, self.planet1, path_iter)
#  def update_circle_color(self):
   #      self.is_balancing_cells = self.model.get_balancing_cells() if self.model.get_balancing_cells() is not None else False
   #      if self.is_charging:
   #          if self.is_balancing_cells:
   #              self.circle_canvas.itemconfig(self.circle, outline="orange")
   #              self.circle_canvas.itemconfig(self.planet1, fill="red")
   #          else:
   #              self.circle_canvas.itemconfig(self.circle, outline="green")
   #              self.circle_canvas.itemconfig(self.planet1, fill="cyan")
   #      else:
   #          self.circle_canvas.itemconfig(self.circle, outline="white")
   #          self.circle_canvas.itemconfig(self.planet1, fill="gray")

     #   self.update_circle_color()

   #  def circular_path(self, x, y, radius, delta_ang, start_ang=0):
   #      """ Endlessly generate coords of a circular path every delta angle degrees. """
   #      ang = start_ang % 360
   #      while True:
   #          yield x + radius*cos(ang), y + radius*sin(ang)
   #          ang = (ang+delta_ang) % 360

   #  def update_position(self, canvas, id, celestial_obj, path_iter):
   #      celestial_obj.x, celestial_obj.y = next(path_iter)  # iterate path and set new position
   #      # update the position of the corresponding canvas obj
   #      x0, y0, x1, y1 = canvas.coords(id)  # coordinates of canvas oval object
   #      oldx, oldy = (x0+x1) // 2, (y0+y1) // 2  # current center point
   #      dx, dy = celestial_obj.x - oldx, celestial_obj.y - oldy  # amount of movement
   #      canvas.move(id, dx, dy)  # move canvas oval object that much
   #      # repeat after delay
   #      orbital_radius = math.hypot(self.sol_obj.x - celestial_obj.x, self.sol_obj.y - celestial_obj.y)
   #      path_iter = self.circular_path(self.sol_obj.x, self.sol_obj.y, orbital_radius, self.circular_path_increment)
   #      canvas.after(self.orbit_delay, self.update_position, canvas, id, celestial_obj, path_iter)


# def sin(degs): return math.sin(math.radians(degs))
# def cos(degs): return math.cos(math.radians(degs))


# class Celestial(object):
#     # Constants
#     COS_0, COS_180 = cos(0), cos(180)
#     SIN_90, SIN_270 = sin(90), sin(270)

#     def __init__(self, x, y, radius):
#         self.x, self.y = x, y
#         self.radius = radius

#     def bounds(self):
#         """ Return coords of rectangle surrounding circlular object. """
#         return (self.x + self.radius*self.COS_0,   self.y + self.radius*self.SIN_270,
#                 self.x + self.radius*self.COS_180, self.y + self.radius*self.SIN_90)
