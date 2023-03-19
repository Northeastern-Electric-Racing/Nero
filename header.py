from tkinter import Frame
import customtkinter
from modes.page import Page
from models.model import Model


class Header(Frame):
    def __init__(self, parent: Frame) -> None:
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1, minsize=30)
        self.grid_columnconfigure(0, weight=1, minsize=parent.model.page_width * 0.8)
        self.grid_columnconfigure(1, weight=1, minsize=parent.model.page_width * 0.2)

        self.left_frame = Frame(self, bg="black",
                                highlightbackground="gray", highlightthickness=1)
        self.right_frame = Frame(self, bg="black", highlightbackground="gray", highlightthickness=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.current_mode_label = customtkinter.CTkLabel(self.left_frame, text="Current Mode: ")
        self.current_mode_label.grid(row=0, column=0, sticky="w")
