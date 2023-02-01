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

        self.right_frame.grid_propagate(False)
        self.right_frame.grid_rowconfigure(18, weight=1)
        self.right_frame.grid_columnconfigure(4, weight=1)

        self.left_frame.grid(row=0, column=0)
        self.right_frame.grid(row=0, column=1)

        self.table = []
        #create left table
        for i in range(0, 18):
            for j in range(0, 8):
               if (j <=3 ):
                  self.e = customtkinter.CTkEntry(self.left_frame, font=('Lato', 21), corner_radius=0, justify="center", text_color="white", placeholder_text_color="white")
                  id = i*2 - 1
               else:
                  self.e = customtkinter.CTkEntry(self.right_frame, font=('Lato', 21), corner_radius=0, justify="center", text_color="white", placeholder_text_color="white")
                  id = i*2
               match i, j:
                  case 0, 0:
                     self.e.configure(placeholder_text="ID")
                  case 0, 4:
                     self.e.configure(placeholder_text="ID")
                  case 0, 1:
                     self.e.configure(placeholder_text="Name")
                  case 0, 5:
                     self.e.configure(placeholder_text="Name")
                  case 0, 2:
                     self.e.configure(placeholder_text="Value")
                  case 0, 6:
                     self.e.configure(placeholder_text="Value")
                  case 0, 3:
                     self.e.configure(placeholder_text="Unit")
                  case 0, 7:
                     self.e.configure(placeholder_text="Unit")
                  case i, 0:
                     self.e.configure(placeholder_text=str(id))
                  case i, 4:
                     self.e.configure(placeholder_text=str(id))
                  case i, 1:
                     self.e.configure(placeholder_text="uhh")
                  case i, 5:
                     self.e.configure(placeholder_text="uhh")
                  case i, 2:
                     self.e.configure(placeholder_text=str(""))
                     self.table.insert(id - 1, self.e)
                  case i, 6:
                     self.e.configure(placeholder_text=str(""))
                     self.table.insert(id - 1, self.e)
               self.e.grid(row=i, column=j, sticky="nsew")
        print(self.table)
        self.update()
        self.controller.check_can()

    def update(self):
        for i in range(0, len(self.table)):
         self.table[i].configure(placeholder_text=str(self.controller.update_generic(i)))
        
        self.after(100, self.update)

    def run(self):
        self.mainloop()
