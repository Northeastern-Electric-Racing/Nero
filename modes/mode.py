from tkinter import Frame
from modes.page import Page
from typing import List

class Mode(Frame):
    def __init__(self, parent: Frame, controller: Frame, model, name: str, page_classes: List[Page]) -> None:
        super().__init__(parent)
        self.controller = controller
        self.name = name
        self.model = model
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.page_index = 0
        self.pages: List[Page] = []
        for page_class in page_classes:
            page: Page = page_class(parent=self, model=model)
            self.pages.append(page)
            page.grid(row=0, column=0, sticky="nsew")

        self.update_page()

    def update_page(self):
        self.current_page: Page = self.pages[self.page_index]
        self.current_page.tkraise()

    def enter_button_pressed(self):
        self.current_page.enter_button_pressed()

    def up_button_pressed(self):
        self.current_page.up_button_pressed()

    def down_button_pressed(self):
        self.current_page.down_button_pressed()

    def right_button_pressed(self):
        self.increment_page()

    def increment_page(self):
        self.page_index += 1
        if (self.page_index >= len(self.pages)):
            self.page_index = 0
        self.update_page()

    def update(self):
        pass
