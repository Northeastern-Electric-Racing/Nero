import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GForceGraph(FigureCanvasTkAgg): 
   def __init__(self, parent):
      x_accel = 0
      y_accel = 0

      # Calculate G-force magnitude and direction
      g_mag = np.sqrt(x_accel**2 + y_accel**2)
      g_direction = np.arctan2(y_accel, x_accel)

      # Create polar plot
      self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
      self.fig.set_facecolor('black')
      self.ax.set_facecolor('black')
      # Define coordinates for the ring of circles
      theta = np.linspace(0, 2*np.pi, 200)

      # Draw ring of circles at every whole number
      for i in range(int(np.floor(g_mag.min())), int(np.ceil(g_mag.max()))):
         self.ax.plot(theta, i * np.ones_like(theta), color='gray', linestyle='--')

      # Plot direction lines
      self.ax.plot(g_direction, g_mag, 'o')

      # Set radial limits
      self.ax.set_rlim(np.floor(g_mag.min())-1, np.ceil(g_mag.max())+1)

      # Set axis labels and title
      self.ax.set_title('G-force Direction')

      super().__init__(self.fig, master=parent)
      self.get_tk_widget().configure(background='black')
      self.draw()

   def set(self, x: int, y:int):
      self.ax.clear()
      x_accel = x
      y_accel = y

      # Calculate G-force magnitude and direction
      g_mag = np.sqrt(x_accel**2 + y_accel**2)
      g_direction = np.arctan2(y_accel, x_accel)

      # Plot direction lines
      self.ax.plot(g_direction, g_mag, 'o')

      # Set radial limits
      self.ax.set_rlim(np.floor(g_mag.min())-1, np.ceil(g_mag.max())+1)

      # Set axis labels and title
      self.ax.set_xlabel('X G-force direction (radians)')
      self.ax.set_ylabel('Y G-force direction (radians)')
      self.ax.set_title('G-force Direction')
      self.draw()