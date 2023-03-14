from tkinter import Frame
import customtkinter
from modes.page import Page
from models.model import Model


class Header(Frame):
    def __init__(self, parent: Frame) -> None:
        super().__init__(parent)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)

        self.left_frame = Frame(self, width=800, height=30, bg="black",
                                 highlightbackground="gray", highlightthickness=1)
        self.right_frame = Frame(self, width=224, height=30, bg="black", highlightbackground="gray", highlightthickness=1)

        self.left_frame.grid_propagate(False)
        self.right_frame.grid_propagate(False)

        self.left_frame.grid(row=0, column=0)
        self.right_frame.grid(row=0, column=1)

        self.current_mode_label = customtkinter.CTkLabel(self.left_frame, text="Current Mode: ")
        self.current_mode_label.grid(row=0, column=0, sticky="w")






