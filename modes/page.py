from tkinter import Frame, Label
from models.model import Model


class Page(Frame):
    def __init__(self, parent: Frame, model: Model, name: str) -> None:
        super().__init__(parent)
        self.name = name
        self.model = model
        self.height = model.page_height
        self.width = model.page_width

    def enter_button_pressed(self):
        pass

    def up_button_pressed(self):
        pass

    def down_button_pressed(self):
        pass

    def update(self):
        pass
