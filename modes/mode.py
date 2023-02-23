from tkinter import Frame
from models.model import Model


class Mode(Frame):
    def __init__(self, parent: Frame, controller: Frame, model: Model, name: str, page_classes) -> None:
        super().__init__(parent)
        self.controller = controller
        self.name = name
        self.model = model

        # create the container frame that holds all pages
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = []
        self.page_index = 0

        for page_class in page_classes:
            page = page_class(parent=container, model=model)
            self.pages.append(page)
            page.grid(row=0, column=0, sticky="nsew")

        self.update_page()

    def update_page(self):
        self.current_page = self.pages[self.page_index]
        self.current_page.tkraise()

    def enter_button_pressed(self):
        self.current_page.enter_button_pressed()

    def up_button_pressed(self):
        self.current_page.up_button_pressed()

    def down_button_pressed(self):
        self.current_page.down_button_pressed()

    def left_button_pressed(self):
        self.decrement_page()

    def right_button_pressed(self):
        self.increment_page()

    def increment_page(self):
        self.page_index += 1
        if (self.page_index >= len(self.pages)):
            self.page_index = 0
        self.update_page()

    def decrement_page(self):
        self.page_index -= 1
        if (self.page_index < 0):
            self.page_index = len(self.pages) - 1
        self.update_page()

    def update(self):
        pass
