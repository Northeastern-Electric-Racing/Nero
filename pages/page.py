from tkinter import Frame, Label

class Page(Frame):
    def __init__(self, parent: Frame, controller: Frame, name: str) -> None:
         super().__init__(parent)
         self.controller = controller
         self.name = name

    def create_view(self):
        label = Label(self, text=self.name)
        label.grid(row=0, column=0, sticky="nsew")

    def enter_button_pressed(self):
        pass

    def up_button_pressed(self):
        pass

    def down_button_pressed(self):
        pass

    def left_button_pressed(self):
        pass

    def right_button_pressed(self):
        pass

    def update(self):
        pass
