from tkinter import Frame
import customtkinter
from typing import List
from modes.page import Page
from models.model import Model
import time
MAX_ITEMS_PINNED = 6

class DebugTableRowFrame(Frame):
    # The frame that holds the label of the row
    def __init__(self, parent: Frame):
        super().__init__(parent, bg="black")


class DebugTableRowLabel(customtkinter.CTkLabel):
    # The label that displays the text of the row
    def __init__(self, parent: Frame, text: str, anchor: str):
        super().__init__(parent, font=('Lato', 20), text_color="white", text=text, anchor=anchor)


class DebugTableRowValue():
    # The values of each row
    def __init__(self, id, name, value, unit):
        self.id = id
        self.name = name
        self.value = value
        self.unit = unit


class DebugTableRow(Frame):
    # The row of the debug table
    def __init__(self, parent: Frame, values: DebugTableRowValue, width: int):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1, minsize=30)
        self.grid_columnconfigure(0, weight=1, minsize=width/14)
        self.grid_columnconfigure(1, weight=1, minsize=width/3.7)
        self.grid_columnconfigure(2, weight=1, minsize=width/14)
        self.grid_columnconfigure(3, weight=1, minsize=width/13.7)

        self.id_frame = DebugTableRowFrame(self)
        self.id_label = DebugTableRowLabel(self.id_frame, str(values.id), "center")

        self.id_frame.grid(row=0, column=0, sticky="nsew")
        self.id_label.grid(row=0, column=0, sticky="nsew")

        self.name_frame = DebugTableRowFrame(self)
        self.name_label = DebugTableRowLabel(self.name_frame, str(values.name), "w")

        self.name_frame.grid(row=0, column=1, sticky="nsew")
        self.name_label.grid(row=0, column=0, sticky="nsew")

        self.value_frame = DebugTableRowFrame(self)
        self.value_label = DebugTableRowLabel(self.value_frame, str(values.value), "e")

        self.value_frame.grid(row=0, column=2, sticky="nsew")
        self.value_label.grid(row=0, column=0, sticky="nsew")

        self.unit_frame = DebugTableRowFrame(self)
        self.unit_label = DebugTableRowLabel(self.unit_frame, str(values.unit), "w")

        self.unit_frame.grid(row=0, column=3, sticky="nsew")
        self.unit_label.grid(row=0, column=0, sticky="nsew")

    # highlights the row with the given color
    def highlight(self, color):
        self.id_frame.configure(bg=color)
        self.name_frame.configure(bg=color)
        self.value_frame.configure(bg=color)
        self.unit_frame.configure(bg=color)

    # determines if the row is highlighted
    def is_highlighted(self):
        return self.id_frame.cget("bg") == "gray" or self.id_frame.cget("bg") == "purple"

    def is_pinned(self):
        return self.id_frame.cget("bg") == "purple" or self.id_frame.cget("bg") == "blue"


class DebugTable(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Debug Table")
        self.selected_id: int = 0
        self.max_row_count: int = int(self.height/30)

        # configure the grid
        self.grid_rowconfigure(0, weight=1, minsize=self.height)
        self.grid_columnconfigure(0, weight=1, minsize=self.width/2)
        self.grid_columnconfigure(1, weight=1, minsize=self.width/2)

        # split the screen into two frames
        self.left_frame = Frame(self, bg="black", highlightbackground='gray', highlightthickness=2)
        self.right_frame = Frame(self, bg="black", highlightbackground='gray', highlightthickness=2)

        for x in range(self.max_row_count):
            self.left_frame.grid_rowconfigure(x, weight=1, minsize=30)
            self.right_frame.grid_rowconfigure(x, weight=1, minsize=30)

        self.left_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # creates the table (self.selected_id is 0)
        self.table: List[DebugTableRow] = self.create_debug_table()
        self.create_table(self.selected_id)

        self.start_time = time.time()

    def create_table(self, baseId: int):
        # Empty values for rows that are not used
        debug_table_row_empty_right = DebugTableRow(self.right_frame, DebugTableRowValue("", "", "", ""), self.width)
        debug_table_row_empty_left = DebugTableRow(self.left_frame, DebugTableRowValue("", "", "", ""), self.width)

        # header rows for the table
        debug_table_row_top_left = DebugTableRow(
            self.left_frame, DebugTableRowValue("ID", "Name", "Value", "Unit"), self.width)

        debug_table_row_top_right = DebugTableRow(
            self.right_frame, DebugTableRowValue("ID", "Name", "Value", "Unit"), self.width)

        # Creates the rows, and places them in the table
        for i in range(self.max_row_count):
            # determines the id for the rows
            left_id = baseId*2
            # if the leftid is out of range then the right id is also out of range so make the row empty
            if (left_id >= len(self.table)):
                debug_table_row_left = debug_table_row_empty_left
                debug_table_row_right = debug_table_row_empty_right
            # if the left id is the last id then the right id is out of range so make the right row empty
            elif (left_id >= len(self.table) - 1):
                debug_table_row_right = debug_table_row_empty_right
                debug_table_row_left = self.table[left_id]
            # otherwise the left and right ids are in range
            else:
                debug_table_row_left = self.table[left_id]
                debug_table_row_right = self.table[left_id + 1]
            match i:
                # create the header row
                case 0:
                    debug_table_row_top_left.grid(row=0, column=0, sticky="nsew", padx=5)
                    debug_table_row_top_right.grid(row=0, column=0, sticky="nsew", padx=5)
                # Create the other rows. If they already exist, raise them to the top
                case i:
                    debug_table_row_left.grid(row=i, column=0, sticky="nsew", padx=5)
                    debug_table_row_left.tkraise()
                    debug_table_row_right.grid(row=i, column=0, sticky="nsew", padx=5)
                    debug_table_row_right.tkraise()
            # if were making the header row, dont increase the baseid yet
            if not i == 0:
                baseId += 1
        # highlight the initial selected row
        if (self.selected_id == 0):
            self.highlightItem()

    def highlightItem(self):
        # if the selected id is pinned and highlighted then unhighlight it
        if self.table[self.selected_id].is_pinned() and self.table[self.selected_id].is_highlighted():
            self.table[self.selected_id].highlight("blue")
        # otherwise if its pinned and not highlighted then highlight it cyan
        elif self.table[self.selected_id].is_pinned():
            self.table[self.selected_id].highlight("purple")
        # otherwise if its not pinned and highlighted then unhighlight it
        elif self.table[self.selected_id].is_highlighted():
            self.table[self.selected_id].highlight("black")
        # otherwise its not pinned and not highlighted, so highlight it
        else:
            self.table[self.selected_id].highlight("gray")

    def enter_button_pressed(self):
        # if the selected id is already pinned then unpin it
        if self.table[self.selected_id].is_pinned():
            self.table[self.selected_id].highlight("gray")
            self.model.remove_pinned_data(self.selected_id)
        # otherwise if the selected id is not pinned and there are less than MAX_ITEMS_PINNED pinned then pin it
        elif len(self.model.pinned_data) < MAX_ITEMS_PINNED:
            self.table[self.selected_id].highlight("purple")
            self.model.add_pinned_data(self.selected_id)

    def up_button_pressed(self):
        # unhighlight the current selected row
        self.highlightItem()
        # Determines if the table should reload to the prior table
        if self.selected_id == 0:
            new_base_id = int(len(self.table) / 2) - self.max_row_count + \
                1 if int(len(self.table) / 2) - self.max_row_count + 1 > 0 else 0
            self.selected_id = len(self.table) - 1
            self.create_table(new_base_id)
        elif int(self.selected_id / 2) % (self.max_row_count - 1) == 0 and self.selected_id % 2 == 0:
            self.create_table(int(self.selected_id / 2) - (self.max_row_count - 1))
            self.selected_id -= 1
        else:
            self.selected_id -= 1
        self.highlightItem()

    def down_button_pressed(self):
        # unhighlight the current selected row
        self.highlightItem()
        # Determines if the table should reload to the next table
        if len(self.table) - 1 == self.selected_id:
            self.create_table(0)
            self.selected_id = 0
        elif int(self.selected_id / 2) % (self.max_row_count - 1) == self.max_row_count - 2 and self.selected_id % 2 == 1:
            self.create_table(int(self.selected_id / 2) + 1)
            self.selected_id += 1
        else:
            self.selected_id += 1
        self.highlightItem()

    def create_debug_table(self):
        values: List[DebugTableRowValue] = self.model.get_debug_table_values()
        table: List[DebugTableRow] = []
        for i in range(len(values)):
            parent: Frame = self.left_frame if i % 2 == 0 else self.right_frame
            table.append(DebugTableRow(parent, values[i], width=self.width))
        return table

    def update_by_id(self, id: int):
        generic_text = self.model.get_by_id(id)
        self.table[id].value_label.configure(text=generic_text)

    def update(self):
        # updates the values in the table every 100 ms
        if time.time() - self.start_time >= 1:
            for i in range(0, len(self.table)):
                self.update_by_id(i)
            self.start_time = time.time()
