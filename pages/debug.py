from tkinter import Frame
import customtkinter
from typing import List


class Debug_Table_Row_Frame(Frame):
    def __init__(self, parent: Frame, width: int):
        super().__init__(parent, bg="black", height=30, width=width)
        self.grid_propagate(False)


class Debug_Table_Row_Label(customtkinter.CTkLabel):
    def __init__(self, parent: Frame, text: str, anchor: str, relx: float = 0.5):
        super().__init__(parent, font=('Lato', 20), text_color="white", text=text)
        self.place(relx=relx, rely=0.5, anchor=anchor)


class Debug_Table_Row_Value():
    def __init__(self, id, name, value, unit):
        self.id = id
        self.name = name
        self.value = value
        self.unit = unit


class Debug_Table_Row():
    def __init__(self, parent_frame: Frame, values: Debug_Table_Row_Value):
        self.id_frame = Debug_Table_Row_Frame(parent_frame, 70)
        self.id_label = Debug_Table_Row_Label(self.id_frame, str(values.id), "center")

        self.name_frame = Debug_Table_Row_Frame(parent_frame, 300)
        self.name_label = Debug_Table_Row_Label(self.name_frame, str(values.name), "w", 0)

        self.value_frame = Debug_Table_Row_Frame(parent_frame, 70)
        self.value_label = Debug_Table_Row_Label(self.value_frame, str(values.value), "e", 1)

        self.unit_frame = Debug_Table_Row_Frame(parent_frame, 100)
        self.unit_label = Debug_Table_Row_Label(self.unit_frame, str(values.unit), "w", 0)

    def highlight(self, color):
        self.id_frame.configure(bg=color)
        self.name_frame.configure(bg=color)
        self.value_frame.configure(bg=color)
        self.unit_frame.configure(bg=color)

    def is_highlighted(self):
        return self.id_frame.cget("bg") == "gray"

    def is_pinned(self):
        return self.id_frame.cget("bg") == "blue"


class Debug_Table(Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller: Frame = controller
        self.selectedId: int = 0
        self.selectedIds: List[int] = []

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

        # create the table
        self.table: List[Debug_Table_Row] = self.controller.create_debug_table()
        self.create_table(0)

        self.update()
        self.controller.check_can()

    def create_table(self, baseId: int):
        Debug_Table_Row_top_right = Debug_Table_Row(self.right_frame, Debug_Table_Row_Value("ID", "Name", "Value", "Unit"))
        Debug_Table_Row_top_right.name_label.place(relx=0.5, rely=0.5, anchor="center")
        Debug_Table_Row_top_right.value_label.place(relx=0.5, rely=0.5, anchor="center")
        Debug_Table_Row_top_right.unit_label.place(relx=0.5, rely=0.5, anchor="center")

        Debug_Table_Row_top_left = Debug_Table_Row(self.left_frame, Debug_Table_Row_Value("ID", "Name", "Value", "Unit"))
        Debug_Table_Row_top_left.name_label.place(relx=0.5, rely=0.5, anchor="center")
        Debug_Table_Row_top_left.value_label.place(relx=0.5, rely=0.5, anchor="center")
        Debug_Table_Row_top_left.unit_label.place(relx=0.5, rely=0.5, anchor="center")

        for i in range(0, 19):
            left_id = baseId*2 - 1
            if (left_id > len(self.table) - 1):
                break
            Debug_Table_Row_left = self.table[left_id + 1]
            Debug_Table_Row_right = self.table[left_id]
            match i:
                case 0:
                    Debug_Table_Row_top_left.id_frame.grid(row=i, column=0, sticky="ew")
                    Debug_Table_Row_top_right.id_frame.grid(row=i, column=4, sticky="ew")
                    Debug_Table_Row_top_left.name_frame.grid(row=i, column=1, sticky="ew")
                    Debug_Table_Row_top_right.name_frame.grid(row=i, column=5, sticky="ew")
                    Debug_Table_Row_top_left.value_frame.grid(row=i, column=2, sticky="ew")
                    Debug_Table_Row_top_right.value_frame.grid(row=i, column=6, sticky="ew")
                    Debug_Table_Row_top_left.unit_frame.grid(row=i, column=3, sticky="ew")
                    Debug_Table_Row_top_right.unit_frame.grid(row=i, column=7, sticky="ew")
                case i:
                    Debug_Table_Row_left.id_frame.grid(row=i, column=0, sticky="ew")
                    Debug_Table_Row_right.id_frame.grid(row=i, column=4, sticky="ew")
                    Debug_Table_Row_left.name_frame.grid(row=i, column=1, sticky="ew")
                    Debug_Table_Row_right.name_frame.grid(row=i, column=5, sticky="ew")
                    Debug_Table_Row_left.value_frame.grid(row=i, column=2, sticky="ew")
                    Debug_Table_Row_right.value_frame.grid(row=i, column=6, sticky="ew")
                    Debug_Table_Row_left.unit_frame.grid(row=i, column=3, sticky="ew")
                    Debug_Table_Row_right.unit_frame.grid(row=i, column=7, sticky="ew")
            if not i == 0:
                baseId += 1
        self.highlightItem()

    def highlightItem(self):
        if not self.table[self.selectedId].is_pinned() and not self.table[self.selectedId].is_highlighted():
            self.table[self.selectedId].highlight("gray")
        elif not self.table[self.selectedId].is_pinned():
            self.table[self.selectedId].highlight("black")

    def enter_button_pressed(self):
        if self.table[self.selectedId].is_pinned():
            self.table[self.selectedId].highlight("gray")
            self.selectedIds.remove(self.selectedId)
        elif len(self.selectedIds) < 6:
            self.table[self.selectedId].highlight("blue")
            self.selectedIds.append(self.selectedId)

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
        if len(self.table) - 1 == self.selectedId:
            return
        match self.selectedId:
            case 35:
                self.create_table(18)
            case 71:
                self.create_table(36)
            case 107:
                return

        self.highlightItem()
        self.selectedId += 1
        self.highlightItem()

    def update(self):
        for i in range(0, len(self.table)):
            self.controller.update_by_id(i)
        self.after(100, self.update)

    def run(self):
        self.mainloop()
