from ner_processing.master_mapping import DATA_IDS
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.message import Message
import time
import can
import customtkinter
from tkinter import Frame
import os
import sys
import platform

if (platform.platform()[0:5] == "Linux"):
    os.system('echo $PWD')
    os.chdir("/home/ner/Desktop/Nero/")
    os.system("echo $PWD")
    # /home/ner/Desktop/Nero/

    # sudo python3 /home/ner/Desktop/Nero/minimum_gui.py

    os.environ.__setitem__('DISPLAY', ':0.0')

    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system('sudo ifconfig can0 up')

    can0 = can.interface.Bus(
        channel='can0', bustype='socketcan')  # socketcan_native

current_data = [None] * len(DATA_IDS)

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("themes/ner.json")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        # configure the grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create top and bottom frames
        self.top_frame = Frame(width=1100, height=300)
        self.bottom_frame = Frame(width=1100, height=300)

        self.top_frame.grid(row=0, column=0)
        self.bottom_frame.grid(row=1, column=0)

        # Configure grids for top and bottom frames
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # create the top two frames
        self.top_right_frame = Frame(self.top_frame, width=550, height=300,
                                     bg="black", highlightbackground="gray", highlightthickness=1)
        self.top_left_frame = Frame(self.top_frame, width=550, height=300,
                                    bg="black", highlightbackground="gray", highlightthickness=1)

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
            master=self.mph_frame, text="NO DATA", font=customtkinter.CTkFont(size=150, weight="bold"))

        self.mph_label = customtkinter.CTkLabel(
            master=self.mph_frame, text="mph", font=customtkinter.CTkFont(size=20))

        self.mph_frame.grid(row=0, column=0, sticky="s")
        self.mph.grid(row=0, column=0)
        self.mph_label.grid(row=0, column=1, sticky="s")

        self.km_frame = Frame(self.top_left_frame,
                              width=550, height=150, bg="black")
        self.km = customtkinter.CTkLabel(
            master=self.km_frame, text=self.calculate_kph(), font=customtkinter.CTkFont(size=25))
        self.km_label = customtkinter.CTkLabel(
            master=self.km_frame, text=" kmph", font=customtkinter.CTkFont(size=25))

        self.km_frame.grid(row=1, column=0, sticky="n")
        self.km.grid(row=0, column=0)
        self.km_label.grid(row=0, column=1)

        # create top right frame
        self.status = customtkinter.CTkLabel(
            master=self.top_right_frame, text="NO DATA", font=customtkinter.CTkFont(size=100, weight="bold"))

        self.dir = customtkinter.CTkLabel(
            master=self.top_right_frame, text="NO DATA", font=customtkinter.CTkFont(size=100, weight="bold"))

        self.status.grid(row=0, column=0, sticky="s")
        self.dir.grid(row=1, column=0, sticky="n")

        # create bottom left frame
        self.pack_temp = customtkinter.CTkLabel(
            master=self.bottom_left_frame, text="NO DATA", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.pack_temp_label = customtkinter.CTkLabel(
            master=self.bottom_left_frame, text="Pack Temperature", font=customtkinter.CTkFont(size=20))

        self.pack_temp.grid(row=0, column=0, sticky="s")
        self.pack_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom middle frame
        self.motor_temp = customtkinter.CTkLabel(
            master=self.bottom_middle_frame, text="NO DATA", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.motor_temp_label = customtkinter.CTkLabel(
            master=self.bottom_middle_frame, text="Motor Temperature", font=customtkinter.CTkFont(size=20))

        self.motor_temp.grid(row=0, column=0, sticky="s")
        self.motor_temp_label.grid(row=1, column=0, sticky="n")

        # create bottom right frame
        self.state_charge = customtkinter.CTkLabel(
            master=self.bottom_right_frame, text="NO DATA", font=customtkinter.CTkFont(size=150, weight="bold"))
        self.state_charge_label = customtkinter.CTkLabel(
            master=self.bottom_right_frame, text="State of Charge", font=customtkinter.CTkFont(size=20))

        self.state_charge.grid(row=0, column=0, sticky="s")
        self.state_charge_label.grid(row=1, column=0, sticky="n")

        if (platform.platform()[0:5] == "Linux"):
            self.check_can()
            self.update_speed()
            self.update_status()
            self.update_dir()
            self.update_motor_temp()
            self.update_pack_temp()
            self.update_state_charge()

    def check_can(self):
        msg = can0.recv(10.0)

        if msg.arbitration_id in MESSAGE_IDS:
            # if msg.arbitration_id == 165:
            timestamp = int(float(msg.timestamp)*1000)
            id = int(msg.arbitration_id)
            length = int(msg.dlc)
            data = [int(x) for x in msg.data]
            msg = Message(timestamp, id, data)
            decodedList = msg.decode()
            for data in decodedList:
                current_data[data.id] = data.value
                print(str(data.id) +
                      " (" + str(DATA_IDS[data.id]) + "): " + str(data.value))

        if msg is None:
            print('Timeout occurred, no message.')

        self.after(1, self.check_can)

    def calculate_kph(self):
        if self.mph._text != "NO DATA":
            return int(int(self.mph._text) * 1.60934)
        return "NO DATA"

    def update_speed(self):
        if current_data[45] is not None:
            self.mph.configure(text=str(round(current_data[45] * 0.01272)))
            self.km.configure(text=str(self.calculate_kph()))
        self.mph.after(100, self.update_speed)

    def update_status(self):
        if current_data[85] is not None:
            if current_data[85] == 1:
                self.status.configure(text="ON", text_color="green")
            else:
                self.status.configure(text="OFF", text_color="red")
        self.status.after(100, self.update_status)

    def update_dir(self):
        if current_data[84] is not None:
            if current_data[84] == 1:
                self.dir.configure(text="FORWARD")
            else:
                self.dir.configure(text="REVERSE")
        self.dir.after(100, self.update_dir)

    def update_pack_temp(self):
        if current_data[10] is not None:
            self.pack_temp.configure(text=str(current_data[4]) + "°")
        self.pack_temp.after(100, self.update_pack_temp)

    def update_motor_temp(self):
        if current_data[28] is not None:
            self.motor_temp.configure(text=str(current_data[5]) + "°")
        self.motor_temp.after(100, self.update_motor_temp)

    def update_state_charge(self):
        if current_data[4] is not None:
            self.state_charge.configure(text=str(current_data[6]) + "%")
        self.state_charge.after(100, self.update_state_charge)

    def update_curr(self):
        if current_data[2] is not None:
            self.current.configure(text=str(current_data[2]))
        self.current.after(100, self.update_curr)

    def update_LVBatt(self):
        if current_data[63] is not None:
            self.LVBatt.configure(text=str(current_data[63]))
        self.LVBatt.after(100, self.update_LVBatt)


if __name__ == "__main__":
    app = App()
    app.mainloop()
