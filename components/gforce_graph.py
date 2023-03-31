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
      # Plot direction lines
      self.ax.plot(g_direction, g_mag, 'o', color='red')

      # Set radial limits
      self.ax.set_rlim(np.floor(g_mag.min())-1, np.ceil(g_mag.max())+1)
      for spine in self.ax.spines.values():
         spine.set_edgecolor('white')
      # Set axis labels and title

      super().__init__(self.fig, master=parent)
      self.get_tk_widget().configure(background='black')
      self.draw()

   def set(self, x: int, y:int):
      if isinstance(x, str) or isinstance(y, str):
         return
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
      self.draw()