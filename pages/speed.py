from tkinter import Frame
import customtkinter


class Speed(Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.name = "Speed"

    def create_view(self):
        # configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create top and bottom frames
        self.top_frame = Frame(self, width=1100, height=300)
        self.bottom_frame = Frame(self, width=1100, height=300)

        self.top_frame.grid(row=0, column=0)
        self.bottom_frame.grid(row=1, column=0)

        # Configure grids for top and bottom frames
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(2, weight=1)

        # create the top two frames
        self.top_right_frame = Frame(self.top_frame, width=550, height=300, bg="black",
                                     highlightbackground="gray", highlightthickness=1)
        self.top_left_frame = Frame(self.top_frame, width=550, height=300, bg="black",
                                    highlightbackground="gray", highlightthickness=1)

        self.top_right_frame.grid(row=0, column=1)
        self.top_left_frame.grid(row=0, column=0)

        self.top_left_frame.grid_propagate(False)
        self.top_left_frame.grid_rowconfigure(1, weight=1)
        self.top_left_frame.grid_columnconfigure(0, weight=1)

        self.top_right_frame.grid_propagate(False)
        self.top_right_frame.grid_rowconfigure(1, weight=1)
        self.top_right_frame.grid_columnconfigure(0, weight=1)

        # create the bottom three frames
        self.bottom_right_frame = Frame(
            self.bottom_frame, width=367, height=300, bg="black", highlightbackground="gray", highlightthickness=1)
        self.bottom_left_frame = Frame(self.bottom_frame, width=367, height=300,
                                       bg="black", highlightbackground="gray", highlightthickness=1)
        self.bottom_middle_frame = Frame(
            self.bottom_frame, width=366, height=300, bg="black", highlightbackground="gray", highlightthickness=1)

        self.bottom_right_frame.grid(row=0, column=2)
        self.bottom_left_frame.grid(row=0, column=0)
        self.bottom_middle_frame.grid(row=0, column=1)

        self.bottom_left_frame.grid_propagate(False)
        self.bottom_left_frame.grid_rowconfigure(1, weight=1)
        self.bottom_left_frame.grid_columnconfigure(0, weight=1)

        self.bottom_middle_frame.grid_propagate(False)
        self.bottom_middle_frame.grid_rowconfigure(1, weight=1)
        self.bottom_middle_frame.grid_columnconfigure(0, weight=1)

        self.bottom_right_frame.grid_propagate(False)
        self.bottom_right_frame.grid_rowconfigure(1, weight=1)
        self.bottom_right_frame.grid_columnconfigure(0, weight=1)

        # create top left frame
        self.mph_frame = Frame(self.top_left_frame,
                               width=550, height=150, bg="black")
        self.mph = customtkinter.CTkLabel(
            master=self.mph_frame, text="N/A", font=customtkinter.CTkFont(size=150, weight="bold"))

        self.mph_label = customtkinter.CTkLabel(
            master=self.mph_frame, text="mph", font=customtkinter.CTkFont(size=20))

        self.mph_frame.grid(row=0, column=0, sticky="s")
        self.mph.grid(row=0, column=0)
        self.mph_label.grid(row=0, column=1, sticky="s")

        self.kph_frame = Frame(self.top_left_frame,
                               width=550, height=150, bg="black")
        self.kph = customtkinter.CTkLabel(
            master=self.kph_frame, text="N/A", font=customtkinter.CTkFont(size=25))
        self.kph_label = customtkinter.CTkLabel(
            master=self.kph_frame, text=" kmph", font=customtkinter.CTkFont(size=25))

        self.kph_frame.grid(row=1, column=0, sticky="n")
        self.kph.grid(row=0, column=0)
        self.kph_label.grid(row=0, column=1)

        # create top right frame
        self.status = customtkinter.CTkLabel(
            master=self.top_right_frame, text="N/A", font=customtkinter.CTkFont(size=100, weight="bold"))

        self.dir = customtkinter.CTkLabel(
            master=self.top_right_frame, text="N/A", font=customtkinter.CTkFont(size=75, weight="bold"))

        self.status.grid(row=0, column=0, sticky="s")
        self.dir.grid(row=1, column=0, sticky="n")

        # create bottom left frame
        self.pack_temp = customtkinter.CTkLabel(
            master=self.bottom_left_frame, text="N/A", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.pack_temp_label = customtkinter.CTkLabel(
            master=self.bottom_left_frame, text="Pack Temperature", font=customtkinter.CTkFont(size=20))

        self.pack_temp.grid(row=0, column=0, sticky="s")
        self.pack_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom middle frame
        self.motor_temp = customtkinter.CTkLabel(
            master=self.bottom_middle_frame, text="N/A", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.motor_temp_label = customtkinter.CTkLabel(
            master=self.bottom_middle_frame, text="SPEED", font=customtkinter.CTkFont(size=20))

        self.motor_temp.grid(row=0, column=0, sticky="s")
        self.motor_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom right frame
        self.state_charge = customtkinter.CTkLabel(
            master=self.bottom_right_frame, text="N/A", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.state_charge_label = customtkinter.CTkLabel(
            master=self.bottom_right_frame, text="State of Charge", font=customtkinter.CTkFont(size=20))

        self.state_charge.grid(row=0, column=0, sticky="s")
        self.state_charge_label.grid(row=1, column=0, sticky="n")

    def update(self):
        self.controller.update_speed()
        self.controller.update_status()
        self.controller.update_dir()
        self.controller.update_pack_temp()
        self.controller.update_motor_temp()
        self.controller.update_state_charge()

        self.after(100, self.update)

    def enter_button_pressed(self):
        return

    def up_button_pressed(self):
        return

    def down_button_pressed(self):
        return

    def run(self):
        self.mainloop()
