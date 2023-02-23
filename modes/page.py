from tkinter import Frame, Label
from models.model import Model


class Page(Frame):
    def __init__(self, parent: Frame, model: Model, name: str) -> None:
        super().__init__(parent)
        self.name = name
        self.model = model

        label = Label(self, text=self.name)
        label.grid(row=0, column=0, sticky="nsew")

    def enter_button_pressed(self):
        pass

    def up_button_pressed(self):
        pass

    def down_button_pressed(self):
        pass

    def update(self):
        pass
