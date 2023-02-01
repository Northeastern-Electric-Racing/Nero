from tkinter import Frame, Entry
import customtkinter


class Debug(Frame):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller

    def create_view(self):
        # configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        #split the screen into two frames
        self.left_frame = Frame(width=550, height=600, bg="black", highlightbackground="gray", highlightthickness=1)
        self.right_frame = Frame(width=550, height=600, bg="black", highlightbackground="gray", highlightthickness=1)

        self.left_frame.grid_propagate(False)
        self.left_frame.grid_rowconfigure(18, weight=1)
        self.left_frame.grid_columnconfigure(4, weight=1)

        self.left_frame.grid(row=0, column=0)
        self.right_frame.grid(row=0, column=1)

        #create left table
        for i in range(0, 18):
            for j in range(0, 4):
               self.e = customtkinter.CTkEntry(self.left_frame, font=('Lato', 22), corner_radius=0, justify="center", text_color="white", placeholder_text_color="white")
               match i, j:
                  case 0, 0:
                     self.e.configure(placeholder_text="ID")
                  case 0, 1:
                     self.e.configure(placeholder_text="Name")
                  case 0, 2:
                     self.e.configure(placeholder_text="Value")
                  case 0, 3:
                     self.e.configure(placeholder_text="Unit")
                  case i, 0:
                     self.e.configure(placeholder_text=str(i*2 + 1))
               self.e.grid(row=i, column=j, sticky="nsew")

      #   self.update()
        self.controller.check_can()

    def update(self):
        self.controller.update_speed()
        self.controller.update_status()
        self.controller.update_dir()
        self.controller.update_pack_temp()
        self.controller.update_motor_temp()
        self.controller.update_state_charge()

        self.after(100, self.update)

    def run(self):
        self.mainloop()
