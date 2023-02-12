from tkinter import Frame
import customtkinter


class Table_Row_Frame(Frame):
    def __init__(self, parent: Frame, width: int):
        super().__init__(parent, bg="black", height=30, width=width)
        self.grid_propagate(False)


class Table_Row_Label(customtkinter.CTkLabel):
    def __init__(self, parent: Frame, text: str, anchor: str):
        super().__init__(parent, font=('Lato', 20),  justify="center", text_color="white", text=text)
        self.place(relx=0.5, rely=0.5, anchor=anchor)


class Table_Row_Value():
    def __init__(self, id, name, value, unit):
        self.id = id
        self.name = name
        self.value = value
        self.unit = unit


class Table_Row():
    def __init__(self, parent_frame: Frame, values: Table_Row_Value):
        self.id_frame = Table_Row_Frame(parent_frame, 70)
        self.id_label = Table_Row_Label(self.id_frame, str(values.id), "center")

        self.name_frame = Table_Row_Frame(parent_frame, 300)
        self.name_label = Table_Row_Label(self.name_frame, str(values.name), "w")

        self.value_frame = Table_Row_Frame(parent_frame, 70)
        self.value_label = Table_Row_Label(self.value_frame, str(values.value), "e")

        self.unit_frame = Table_Row_Frame(parent_frame, 100)
        self.unit_label = Table_Row_Label(self.unit_frame, str(values.unit), "w")

    def highlight(self, color):
        if self.is_highlighted():
            self.dehighlight()
        else:
            self.id_label.configure(bg_color=color)
            self.name_label.configure(bg_color=color)
            self.value_label.configure(bg_color=color)
            self.unit_label.configure(bg_color=color)

    def dehighlight(self):
        self.id_label.configure(bg_color="black")
        self.name_label.configure(bg_color="black")
        self.value_label.configure(bg_color="black")
        self.unit_label.configure(bg_color="black")

    def is_highlighted(self):
        return self.id_label.cget("bg_color") == "gray"

    def is_pinned(self):
        return self.id_label.cget("bg_color") == "green"


class Debug_Table(Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.selectedId = 0
        self.selectedIds = []
        self.table: list(Table_Row) = self.controller.create_debug_table()

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

        self.table.append(Table_Row(self.left_frame, Table_Row_Value("ID", "Name", "Value", "Unit")))
        self.table.append(Table_Row(self.right_frame, Table_Row_Value("ID", "Name", "Value", "Unit")))

        # create the table
        self.create_table(0)

        self.update()
        self.controller.check_can()

    def create_table(self, baseId: int):
        table_row_top_right = self.table[len(self.table) - 1]
        table_row_top_left = self.table[len(self.table) - 2]
        for i in range(0, 19):
            for j in range(0, 8):
                    self.frame = Frame(self.left_frame, bg="black", height=30)
                    self.label = customtkinter.CTkLabel(self.frame, font=('Lato', 20),  justify="center", text_color="white")
                    id = baseId*2 - 1
                else:
                    self.frame = Frame(self.right_frame, bg="black", height=30)
                    self.label = customtkinter.CTkLabel(self.frame, font=('Lato', 20), justify="center", text_color="white")
                    id = baseId*2

                self.frame.grid_propagate(False)

                self.frame.grid(row=i, column=j, sticky="ew", padx=5)
            left_id = baseId*2 + 1
            print(left_id)
            if (left_id > len(self.table) - 2):
                break
            table_row_left = self.table[left_id]
            table_row_right = self.table[left_id + 1]
            match i:
                case 0:
                    table_row_top_left.id_frame.grid(row=i, column=0, sticky="ew", padx=5)
                    table_row_top_right.id_frame.grid(row=i, column=4, sticky="ew", padx=5)
                    table_row_top_left.name_frame.grid(row=i, column=1, sticky="ew", padx=5)
                    table_row_top_right.name_frame.grid(row=i, column=5, sticky="ew", padx=5)
                    table_row_top_left.value_frame.grid(row=i, column=2, sticky="ew", padx=5)
                    table_row_top_right.value_frame.grid(row=i, column=6, sticky="ew", padx=5)
                    table_row_top_left.unit_frame.grid(row=i, column=3, sticky="ew", padx=5)
                    table_row_top_right.unit_frame.grid(row=i, column=7, sticky="ew", padx=5)
                case i:
                    table_row_left.id_frame.grid(row=i, column=0, sticky="ew", padx=5)
                    table_row_right.id_frame.grid(row=i, column=4, sticky="ew", padx=5)
                    table_row_left.name_frame.grid(row=i, column=1, sticky="ew", padx=5)
                    table_row_right.name_frame.grid(row=i, column=5, sticky="ew", padx=5)
                    table_row_left.value_frame.grid(row=i, column=2, sticky="ew", padx=5)
                    table_row_right.value_frame.grid(row=i, column=6, sticky="ew", padx=5)
                    table_row_left.unit_frame.grid(row=i, column=3, sticky="ew", padx=5)
                    table_row_right.unit_frame.grid(row=i, column=7, sticky="ew", padx=5)
            baseId += 1
        self.highlightItem()

    def highlightItem(self):
        if not self.table[self.selectedId].is_pinned():
            self.table[self.selectedId].highlight("gray")

    def enter_button_pressed(self):
        if self.table[self.selectedId].is_pinned():
            self.table[self.selectedId].highlight("gray")
        self.table[self.selectedId].highlight("green")

    def up_button_pressed(self):
        match self.selectedId:
            case 0:
                return
            case 36:
                self.create_table(0)
            case 72:
                self.create_table(18)
        self.highlightItem()
        self.selectedId -= 1
        self.highlightItem()

    def down_button_pressed(self):
        match self.selectedId:
            case 35:
                self.create_table(18)
            case 71:
                self.create_table(36)
            case 107:
                return
        self.highlightItem()
        self.selectedId += 1
        print(self.selectedId)
        print(len(self.table))
        self.highlightItem()

    def update(self):
        for i in range(0, len(self.table)):
            self.controller.update_generic(i)
        self.after(100, self.update)

    def run(self):
        self.mainloop()
