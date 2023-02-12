from typing import Optional
import random
from pynput.keyboard import Listener, Key
from pages import debug


class MockModel:
    def __init__(self) -> None:
        self.mph = 60
        self.status = True
        self.dir = True
        self.pack_temp = 47
        self.motor_temp = 122
        self.state_of_charge = 88
        self.lv_battery = 88
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        pass

    def check_can(self) -> None:
        rng = random.randint(0, 10000)

        if rng < 5 and rng >= 0:
            self.mph += 1
        elif rng >= 5 and rng <= 10:
            self.mph -= 1

        if rng == 100:
            self.status = False
        elif rng == 101:
            self.status = None
        elif rng < 5:
            self.status = True

        if rng == 200:
            self.dir = False
        if rng > 40 and rng < 45:
            self.dir = True

    def on_press(self, key):
        match key:
            case Key.enter:
                self.enter_button_pressed()
            case Key.right:
                self.forward_button_pressed()
                print("right pressed")
            case Key.up:
                self.up_button_pressed()
            case Key.down:
                self.down_button_pressed()

    def get_mph(self) -> Optional[int]:
        return self.mph

    def get_kph(self) -> Optional[int]:
        return round(self.mph * 1.609)

    def get_status(self) -> Optional[bool]:
        return self.status

    def get_dir(self) -> Optional[bool]:
        return self.dir

    def get_pack_temp(self) -> Optional[int]:
        return self.pack_temp

    def get_motor_temp(self) -> Optional[int]:
        return self.motor_temp

    def get_state_of_charge(self) -> Optional[int]:
        return self.state_of_charge

    def get_lv_battery(self) -> Optional[int]:
        return self.lv_battery

    def get_generic(self, id: int) -> Optional[int]:
        return None

    def get_debug_table_values(self) -> list():
        return []

    def forward_button_pressed(self):
        self.forward_button_action()

    def enter_button_pressed(self):
        self.enter_button_action()

    def up_button_pressed(self):
        self.up_button_action()

    def down_button_pressed(self):
        self.down_button_action()

    def set_forward_button_action(self, func):
        self.forward_button_action = func

    def set_enter_button_action(self, func):
        self.enter_button_action = func

    def set_up_button_action(self, func):
        self.up_button_action = func

    def set_down_button_action(self, func):
        self.down_button_action = func
