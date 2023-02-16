from tkinter import Frame
from typing import List
from pages.debug_plot import Debug_Plot
from pages.debug_table import Debug_Table, Debug_Table_Row, Debug_Table_Row_Value
from pages.page import Page

class Debug(Page):
    def __init__(self, controller, parent):
        super().__init__(parent, controller, "Debug")

    def create_view(self):
        self.view_index = 0
        self.view_dict = {0: "Debug Table", 1: "Debug Plot"}

        # create the container frame that holds all views
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create the views that the container will hold
        self.frames = {}
        for page in (Debug_Table, Debug_Plot):
            frame = page(parent=container, controller=self)
            name = frame.name
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        for frame in self.frames.values():
            frame.create_view()

        self.update_frame()

    def update_frame(self):
        frame = self.frames[self.view_dict[self.view_index]]
        frame.tkraise()

    def create_debug_table(self):
        values: List[Debug_Table_Row_Value] = self.controller.get_debug_table_values()
        table: List[Debug_Table_Row] = []
        for i in range(len(values)):
            parent: Frame
            if i % 2 == 0:
                parent = self.frames["Debug Table"].left_frame
            else:
                parent = self.frames["Debug Table"].right_frame
            table.append(Debug_Table_Row(parent, values[i]))
        return table

    def update_by_id(self, id: int):
        generic_text = self.controller.get_by_id(id)
        self.frames["Debug Table"].table[id].value_label.configure(text=generic_text)

    def enter_button_pressed(self):
        self.frames[self.view_dict[self.view_index]].enter_button_pressed()

    def up_button_pressed(self):
        self.frames[self.view_dict[self.view_index]].up_button_pressed()

    def down_button_pressed(self):
        self.frames[self.view_dict[self.view_index]].down_button_pressed()

    def left_button_pressed(self):
        self.decrement_view()

    def right_button_pressed(self):
        self.increment_view()

    def increment_view(self):
        self.view_index += 1
        if (self.view_index >= len(self.frames)):
            self.view_index = 0
        self.update_frame()

    def decrement_view(self):
        self.view_index -= 1
        if (self.view_index < 0):
            self.view_index = len(self.frames) - 1
        self.update_frame()
