import os
import sys

os.system('echo $PWD')
#/home/ner/Desktop/Nero/

# sudo python3 /home/ner/Desktop/Nero/minimum_gui.py

import tkinter
import customtkinter
import can
import time

from ner_processing.message import Message
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.master_mapping import DATA_IDS


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
customtkinter.set_default_color_theme("./themes/ner.json")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("NERO")
        self.geometry(f"{1100}x{580}")

        # create 2x2 grid system
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.logo_label = customtkinter.CTkLabel(
            master=self, text="NERO", font=customtkinter.CTkFont(size=36, weight="bold"), anchor="w")
        self.logo_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.button = customtkinter.CTkButton(
            master=self, command=self.button_callback)
        self.button.grid(row=1, column=0)

        self.speed = customtkinter.CTkLabel(
            master=self, text="Speed:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.speed.grid(row=1, column=1)
        self.mph = customtkinter.CTkLabel(
            master=self, text="69 mph", font=customtkinter.CTkFont(size=36, weight="bold"))
        
        self.mph.grid(row=2, column=1)

        self.check_can()
        self.update_speed()

    def check_can(self):
        msg = can0.recv(10.0)
        # if msg.arbitration_id in MESSAGE_IDS:
        if msg.arbitration_id == 165:
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

    def update_speed(self):
        self.mph.configure(text=str(current_data[45]))
        self.mph.after(100, self.update_speed)

    def button_callback(self):
        print("button pressed")
        print('Terminating can')
        os.system('sudo ifconfig can0 down')

if __name__ == "__main__":
    app = App()
    app.mainloop()
