from tkinter import Frame
import customtkinter


class Debug(Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.selectedId = 0

    def create_view(self):
        # configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # split the screen into two frames
        self.left_frame = Frame(self, width=550, height=600, bg="black", highlightbackground='gray', highlightthickness=2)
        self.right_frame = Frame(self, width=550, height=600, bg="black", highlightbackground='gray', highlightthickness=2)

        self.left_frame.grid_propagate(False)
        self.left_frame.grid_rowconfigure(19, weight=1)
        self.left_frame.grid_columnconfigure(4, weight=1)

        self.right_frame.grid_propagate(False)
        self.right_frame.grid_rowconfigure(19, weight=1)
        self.right_frame.grid_columnconfigure(4, weight=1)

        self.left_frame.grid(row=0, column=0)
        self.right_frame.grid(row=0, column=1)

        self.table = []
        # create the table
        self.create_table(0)
        self.update()
        self.controller.check_can()

    def create_table(self, baseId=0):
        for i in range(0, 19):
            for j in range(0, 8):
                if (j <= 3):
                    self.frame = Frame(self.left_frame, bg="black", height=30)
                    self.label = customtkinter.CTkLabel(self.frame, font=('Lato', 20),  justify="center", text_color="white")
                    id = baseId*2 - 1
                else:
                    self.frame = Frame(self.right_frame, bg="black", height=30)
                    self.label = customtkinter.CTkLabel(self.frame, font=('Lato', 20), justify="center", text_color="white")
                    id = baseId*2

                self.frame.grid_propagate(False)

                self.frame.grid(row=i, column=j, sticky="ew", padx=5)
                self.label.place(relx=0.5, rely=0.5, anchor="center")

                match i, j:
                    # create the id headers
                    case 0, 0:
                        self.label.configure(text="ID")
                        self.frame.configure(width=70)
                    case 0, 4:
                        self.label.configure(text="ID")
                        self.frame.configure(width=70)
                    # create the name headers
                    case 0, 1:
                        self.label.configure(text="Name")
                        self.frame.configure(width=300)
                    case 0, 5:
                        self.label.configure(text="Name")
                        self.frame.configure(width=300)
                    # creaet the value headers
                    case 0, 2:
                        self.label.configure(text="Value")
                        self.frame.configure(width=70)
                    case 0, 6:
                        self.label.configure(text="Value")
                        self.frame.configure(width=70)
                    # create the unit headers
                    case 0, 3:
                        self.label.configure(text="Unit")
                        self.frame.configure(width=100)
                    case 0, 7:
                        self.label.configure(text="Unit")
                        self.frame.configure(width=100)
                    # create the id columns
                    case i, 0:
                        self.label.configure(text=str(id))
                        self.frame.configure(width=70)
                    case i, 4:
                        self.label.configure(text=str(id))
                        self.frame.configure(width=70)
                    # create the name columns
                    case i, 1:
                        self.label.configure(text="N/A")
                        self.frame.configure(width=300)
                        self.label.place(relx=0, rely=0.5, anchor="w")
                    case i, 5:
                        self.label.configure(text="N/A")
                        self.frame.configure(width=300)
                        self.label.place(relx=0, rely=0.5, anchor="w")
                    # create the value columns
                    case i, 2:
                        self.label.configure(text="N/A")
                        self.table.insert(id - 1, self.label)
                        self.frame.configure(width=70)
                        self.label.place(relx=1, rely=0.5, anchor="e")
                    case i, 6:
                        self.label.configure(text="N/A")
                        self.table.insert(id - 1, self.label)
                        self.frame.configure(width=70)
                        self.label.place(relx=1, rely=0.5, anchor="e")
                    # create the unit columns
                    case i, 3:
                        self.label.configure(text="N/A")
                        self.frame.configure(width=100)
                        self.label.place(relx=0, rely=0.5, anchor="w")
                    case i, 7:
                        self.label.configure(text="N/A")
                        self.frame.configure(width=100)
                        self.label.place(relx=0, rely=0.5, anchor="w")
            baseId += 1
        self.selectItem()

    def selectItem(self):
        self.table[self.selectedId].configure(bg_color="red")

    def deselectItem(self, id):
        self.table[id].configure(bg_color="black")

    def enter_button_pressed(self):
        self.table[self.selectedId].configure(fg_color="green")

    def up_button_pressed(self):
        match self.selectedId:
            case 0:
                return
            case 36:
                self.create_table(0)
            case 72:
                self.create_table(18)
        self.deselectItem(self.selectedId)
        self.selectedId -= 1
        self.selectItem()

    def down_button_pressed(self):
        match self.selectedId:
            case 35:
                self.create_table(18)
            case 71:
                self.create_table(36)
            case 107:
                return
        self.deselectItem(self.selectedId)
        self.selectedId += 1
        print(self.selectedId)
        print(len(self.table))
        self.selectItem()

    def update(self):
        for i in range(0, len(self.table)):
            self.controller.update_generic(i)
        self.after(100, self.update)

    def run(self):
        self.mainloop()
