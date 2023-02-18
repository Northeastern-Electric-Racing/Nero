from tkinter import Frame
import customtkinter
from typing import List
from pages.page import Page

class Debug_Table_Row_Frame(Frame):
    # The frame that holds the label of the row
    def __init__(self, parent: Frame, width: int):
        super().__init__(parent, bg="black", height=30, width=width)
        self.grid_propagate(False)


class Debug_Table_Row_Label(customtkinter.CTkLabel):
    # The label that displays the text of the row
    def __init__(self, parent: Frame, text: str, anchor: str, relx: float = 0.5):
        super().__init__(parent, font=('Lato', 20), text_color="white", text=text)
        self.place(relx=relx, rely=0.5, anchor=anchor)


class Debug_Table_Row_Value():
    # The values of each row
    def __init__(self, id, name, value, unit):
        self.id = id
        self.name = name
        self.value = value
        self.unit = unit


class Debug_Table_Row():
    # The row of the debug table
    def __init__(self, parent_frame: Frame, values: Debug_Table_Row_Value):
        self.id_frame = Debug_Table_Row_Frame(parent_frame, 70)
        self.id_label = Debug_Table_Row_Label(self.id_frame, str(values.id), "center")

        self.name_frame = Debug_Table_Row_Frame(parent_frame, 290)
        self.name_label = Debug_Table_Row_Label(self.name_frame, str(values.name), "w", 0)

        self.value_frame = Debug_Table_Row_Frame(parent_frame, 70)
        self.value_label = Debug_Table_Row_Label(self.value_frame, str(values.value), "e", 1)

        self.unit_frame = Debug_Table_Row_Frame(parent_frame, 75)
        self.unit_label = Debug_Table_Row_Label(self.unit_frame, str(values.unit), "w", 0.2)

    # highlights the row with the given color
    def highlight(self, color):
        self.id_frame.configure(bg=color)
        self.name_frame.configure(bg=color)
        self.value_frame.configure(bg=color)
        self.unit_frame.configure(bg=color)

    # determines if the row is highlighted
    def is_highlighted(self):
        return self.id_frame.cget("bg") == "gray" or self.id_frame.cget("bg") == "cyan"
    
    def is_pinned(self):
        return self.id_frame.cget("bg") == "cyan" or self.id_frame.cget("bg") == "blue"

class Debug_Table(Page):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller, "Debug Table")
        self.selected_id: int = 0

    # Creates the initial two frames
    def create_view(self):
        # configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # split the screen into two frames
        self.left_frame = Frame(self, width=525, height=600, bg="black", highlightbackground='gray', highlightthickness=2)
        self.right_frame = Frame(self, width=525, height=600, bg="black", highlightbackground='gray', highlightthickness=2)

        self.left_frame.grid_propagate(False)
        self.left_frame.grid_rowconfigure(19, weight=1)
        self.left_frame.grid_columnconfigure(4, weight=1)

        self.right_frame.grid_propagate(False)
        self.right_frame.grid_rowconfigure(19, weight=1)
        self.right_frame.grid_columnconfigure(4, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="ew")
        self.right_frame.grid(row=0, column=1, sticky="ew")

        # creates the table
        self.table: List[Debug_Table_Row] = self.controller.create_debug_table()
        self.create_table(0)

        # Updates the table values
        self.update()

    def create_table(self, baseId: int):
        # Empty values for rows that are not used
        debug_table_row_Empty_right = Debug_Table_Row(self.right_frame, Debug_Table_Row_Value("", "", "", ""))
        debug_table_row_Empty_left = Debug_Table_Row(self.left_frame, Debug_Table_Row_Value("", "", "", ""))

        # header rows for the table
        debug_table_row_top_right = Debug_Table_Row(self.right_frame, Debug_Table_Row_Value("ID", "Name", "Value", "Unit"))
        debug_table_row_top_right.name_label.place(relx=0.5, rely=0.5, anchor="center")
        debug_table_row_top_right.value_label.place(relx=0.5, rely=0.5, anchor="center")
        debug_table_row_top_right.unit_label.place(relx=0.5, rely=0.5, anchor="center")

        debug_table_row_top_left = Debug_Table_Row(self.left_frame, Debug_Table_Row_Value("ID", "Name", "Value", "Unit"))
        debug_table_row_top_left.name_label.place(relx=0.5, rely=0.5, anchor="center")
        debug_table_row_top_left.value_label.place(relx=0.5, rely=0.5, anchor="center")
        debug_table_row_top_left.unit_label.place(relx=0.5, rely=0.5, anchor="center")

        # Creates the rows, and places them in the table
        for i in range(0, 19):
            # determines the id for the rows
            left_id = baseId*2
            # if the leftid is out of range then the right id is also out of range so make the row empty
            if (left_id >= len(self.table)):
                debug_table_row_left = debug_table_row_Empty_left
                debug_table_row_right = debug_table_row_Empty_right
            # if the left id is the last id then the right id is out of range so make the right row empty
            elif (left_id >= len(self.table) - 1):
                debug_table_row_right = debug_table_row_Empty_right
                debug_table_row_left = self.table[left_id]
            # otherwise the left and right ids are in range
            else:
                debug_table_row_left = self.table[left_id]
                debug_table_row_right = self.table[left_id + 1]
            match i:
                # create the header row
                case 0:
                    debug_table_row_top_left.id_frame.grid(row=i, column=0, sticky="ew")
                    debug_table_row_top_right.id_frame.grid(row=i, column=4, sticky="ew")
                    debug_table_row_top_left.name_frame.grid(row=i, column=1, sticky="ew")
                    debug_table_row_top_right.name_frame.grid(row=i, column=5, sticky="ew")
                    debug_table_row_top_left.value_frame.grid(row=i, column=2, sticky="ew")
                    debug_table_row_top_right.value_frame.grid(row=i, column=6, sticky="ew")
                    debug_table_row_top_left.unit_frame.grid(row=i, column=3, sticky="ew")
                    debug_table_row_top_right.unit_frame.grid(row=i, column=7, sticky="ew")
                # Create the other rows. If they already exist, raise them to the top
                case i:
                    debug_table_row_left.id_frame.grid(row=i, column=0, sticky="ew")
                    debug_table_row_left.id_frame.tkraise()
                    debug_table_row_right.id_frame.grid(row=i, column=4, sticky="ew")
                    debug_table_row_right.id_frame.tkraise()

                    debug_table_row_left.name_frame.grid(row=i, column=1, sticky="ew")
                    debug_table_row_left.name_frame.tkraise()
                    debug_table_row_right.name_frame.grid(row=i, column=5, sticky="ew")
                    debug_table_row_right.name_frame.tkraise()

                    debug_table_row_left.value_frame.grid(row=i, column=2, sticky="ew")
                    debug_table_row_left.value_frame.tkraise()
                    debug_table_row_right.value_frame.grid(row=i, column=6, sticky="ew")
                    debug_table_row_right.value_frame.tkraise()

                    debug_table_row_left.unit_frame.grid(row=i, column=3, sticky="ew")
                    debug_table_row_left.unit_frame.tkraise()
                    debug_table_row_right.unit_frame.grid(row=i, column=7, sticky="ew")
                    debug_table_row_right.unit_frame.tkraise()
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
            self.table[self.selected_id].highlight("cyan")
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
            self.controller.pinned_data.pop(self.selected_id)
        # otherwise if the selected id is not pinned and there are less than 6 pinned then pin it
        elif len(self.controller.pinned_data.keys()) < 6:
            self.table[self.selected_id].highlight("cyan")
            self.controller.pinned_data[self.selected_id] = [self.table[self.selected_id].value_label.cget("text")]

    def up_button_pressed(self):
        # Determines if the table should reload to the prior table
        match self.selected_id:
            case 0:
                return
            case 36:
                self.create_table(0)
            case 72:
                self.create_table(18)
        # unhighlight the current selected row
        self.highlightItem()
        # change the selected id to the row above and highlight it
        self.selected_id -= 1
        self.highlightItem()

    def down_button_pressed(self):
        # Determines if the table should reload to the next table
        if len(self.table) - 1 == self.selected_id:
            return
        match self.selected_id:
            case 35:
                self.create_table(18)
            case 71:
                self.create_table(36)
            case 107:
                return
        # unhighlight the current selected row
        self.highlightItem()
        # change the selected id to the row below and highlight it
        self.selected_id += 1
        self.highlightItem()

    def update(self):
        # updates the values in the table every 100 ms
        for i in range(0, len(self.table)):
            self.controller.update_by_id(i)
        self.after(100, self.update)