from tkinter import Frame, BitmapImage
import customtkinter
from modes.page import Page
from models.model import Model
from typing import Optional


class Home(Page):
    def __init__(self, parent: Frame, model: Model) -> None:
        super().__init__(parent, model, "Home")

        # configure the grid (configure is responsible for configuring
        # a specific row or column at the given index)
        self.grid_rowconfigure(0, weight=1, minsize=self.height / 2)
        self.grid_rowconfigure(1, weight=1, minsize=self.height / 2)
        self.grid_columnconfigure(0, weight=1, minsize=self.width)

        # create top and bottom frames
        self.top_frame = Frame(self)
        self.bottom_frame = Frame(self)

        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        # Configure grids for top and bottom frames
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1, minsize=self.width / 2)
        self.top_frame.grid_columnconfigure(1, weight=1, minsize=self.width / 2)

        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1, minsize=self.width / 3)
        self.bottom_frame.grid_columnconfigure(1, weight=1, minsize=self.width / 3)
        self.bottom_frame.grid_columnconfigure(2, weight=1, minsize=self.width / 3)

        # create the top two frames
        self.top_right_frame = Frame(
            self.top_frame, highlightbackground="gray", bg="black", highlightthickness=1
        )
        self.top_left_frame = Frame(
            self.top_frame, highlightbackground="gray", highlightthickness=1
        )

        self.top_right_frame.grid(row=0, column=1, sticky="nsew")
        self.top_left_frame.grid(row=0, column=0, sticky="nsew")

        self.top_left_frame.grid_rowconfigure(0, weight=1)
        self.top_left_frame.grid_rowconfigure(1, weight=1)
        self.top_left_frame.grid_columnconfigure(0, weight=1)

        self.top_right_frame.grid_rowconfigure(0, weight=1)
        self.top_right_frame.grid_rowconfigure(1, weight=1)
        self.top_right_frame.grid_columnconfigure(0, weight=1)

        # create the bottom three frames
        self.bottom_right_frame = Frame(
            self.bottom_frame,
            highlightbackground="gray",
            bg="black",
            highlightthickness=1,
        )
        self.bottom_left_frame = Frame(
            self.bottom_frame,
            highlightbackground="gray",
            bg="black",
            highlightthickness=1,
        )
        self.bottom_middle_frame = Frame(
            self.bottom_frame,
            highlightbackground="gray",
            bg="black",
            highlightthickness=1,
        )

        self.bottom_left_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_middle_frame.grid(row=0, column=1, sticky="nsew")
        self.bottom_right_frame.grid(row=0, column=2, sticky="nsew")

        self.bottom_left_frame.grid_rowconfigure(0, weight=1)
        self.bottom_left_frame.grid_rowconfigure(1, weight=1)
        self.bottom_left_frame.grid_columnconfigure(0, weight=1)

        self.bottom_middle_frame.grid_rowconfigure(0, weight=1)
        self.bottom_middle_frame.grid_rowconfigure(1, weight=1)
        self.bottom_middle_frame.grid_columnconfigure(0, weight=1)

        self.bottom_right_frame.grid_rowconfigure(0, weight=1)
        self.bottom_right_frame.grid_rowconfigure(1, weight=1)
        self.bottom_right_frame.grid_columnconfigure(0, weight=1)

        # create top left frame
        self.mph_frame = Frame(self.top_left_frame, bg="black")
        self.mph_frame.grid_rowconfigure(0, weight=1)
        self.mph_frame.grid_columnconfigure(0, weight=1)
        self.mph_frame.grid_columnconfigure(1, weight=1)

        self.mph = customtkinter.CTkLabel(
            master=self.mph_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=150, weight="bold"),
        )

        self.mph_label = customtkinter.CTkLabel(
            master=self.mph_frame, text=" mph", font=customtkinter.CTkFont(size=20)
        )

        self.mph_frame.grid(row=0, column=0, sticky="nsew")
        self.mph.grid(row=0, column=0, sticky="se")
        self.mph_label.grid(row=0, column=1, sticky="sw")

        self.kph_frame = Frame(self.top_left_frame, bg="black")
        self.kph_frame.grid_rowconfigure(0, weight=1)
        self.kph_frame.grid_columnconfigure(0, weight=1)
        self.kph_frame.grid_columnconfigure(1, weight=1)

        self.kph = customtkinter.CTkLabel(
            master=self.kph_frame, text="N/A", font=customtkinter.CTkFont(size=20)
        )
        self.kph_label = customtkinter.CTkLabel(
            master=self.kph_frame, text=" kmph", font=customtkinter.CTkFont(size=20)
        )

        self.kph_frame.grid(row=1, column=0, sticky="nsew")
        self.kph.grid(row=0, column=0, sticky="ne")
        self.kph_label.grid(row=0, column=1, sticky="nw")

        self.limit_image = customtkinter.CTkLabel(
            master=self.top_left_frame,
            image=BitmapImage(
                file="images/speedLimitIcon.xbm", foreground="white", background="black"
            ),
            text="",
        )
        self.limit_image.place(
            x=20, y=self.height / 2 - 90, relwidth=0.15, relheight=0.3
        )

        # create top right frame
        self.status = customtkinter.CTkLabel(
            master=self.top_right_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=100, weight="bold"),
        )

        self.dir = customtkinter.CTkLabel(
            master=self.top_right_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=75, weight="bold"),
        )

        self.status.grid(row=0, column=0, sticky="sew")
        self.dir.grid(row=1, column=0, sticky="new")

        # create bottom left frame
        self.pack_temp = customtkinter.CTkLabel(
            master=self.bottom_left_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=150, weight="bold"),
        )
        self.pack_temp_label = customtkinter.CTkLabel(
            master=self.bottom_left_frame,
            text="Pack Temperature",
            font=customtkinter.CTkFont(size=20),
        )

        self.pack_temp.grid(row=0, column=0, sticky="s")
        self.pack_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom middle frame
        self.motor_temp = customtkinter.CTkLabel(
            master=self.bottom_middle_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=150, weight="bold"),
        )
        self.motor_temp_label = customtkinter.CTkLabel(
            master=self.bottom_middle_frame,
            text="Motor Temperature",
            font=customtkinter.CTkFont(size=20),
        )

        self.motor_temp.grid(row=0, column=0, sticky="s")
        self.motor_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom right frame
        self.state_charge = customtkinter.CTkLabel(
            master=self.bottom_right_frame,
            text="N/A",
            font=customtkinter.CTkFont(size=150, weight="bold"),
        )
        self.state_charge_label = customtkinter.CTkLabel(
            master=self.bottom_right_frame,
            text="State of Charge",
            font=customtkinter.CTkFont(size=20),
        )

        self.state_charge.grid(row=0, column=0, sticky="s")
        self.state_charge_label.grid(row=1, column=0, sticky="n")

    # Updates for specific attributes
    def update_speed(self):
        new_mph: Optional[int] = self.model.get_mph()
        new_kph: Optional[int] = self.model.get_kph()

        new_mph_text = str(new_mph) if new_mph is not None else "N/A"
        new_kph_text = str(new_kph) if new_kph is not None else "N/A"

        self.mph.configure(text=new_mph_text)
        self.kph.configure(text=new_kph_text)

    def update_status(self):
        new_status: Optional[bool] = self.model.get_status()

        if new_status == True:
            self.status.configure(text="ON", text_color="green")
        elif new_status == False:
            self.status.configure(text="OFF", text_color="red")
        else:
            self.status.configure(text="N/A")

    def update_dir(self):
        new_dir: Optional[bool] = self.model.get_dir()

        if new_dir == True:
            self.dir.configure(text="FORWARD")
        elif new_dir == False:
            self.dir.configure(text="REVERSE")
        else:
            self.dir.configure(text="N/A")

    def update_pack_temp(self):
        new_pack_temp: Optional[int] = self.model.get_pack_temp()

        new_pack_temp_text = (
            str(new_pack_temp) + "°" if new_pack_temp is not None else "N/A"
        )

        self.pack_temp.configure(text=new_pack_temp_text)

    def update_motor_temp(self):
        new_motor_temp: Optional[int] = self.model.get_motor_temp()

        new_motor_temp_text = (
            str(new_motor_temp) + "°" if new_motor_temp is not None else "N/A"
        )

        self.motor_temp.configure(text=new_motor_temp_text)

    def update_state_charge(self):
        new_charge: Optional[int] = self.model.get_state_of_charge()

        new_charge_text = (
            str(int(new_charge)) + "%" if new_charge is not None else "N/A"
        )

        self.state_charge.configure(text=new_charge_text)

    def update(self):
        self.update_speed()
        self.update_status()
        self.update_dir()
        self.update_pack_temp()
        self.update_motor_temp()
        self.update_state_charge()
