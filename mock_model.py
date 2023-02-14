from typing import Optional, List
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
        self.forward = False
        self.enter = False
        self.up = False
        self.down = False
        self.view_index = 0
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
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
                self.enter = True
            case Key.right:
                self.forward = True
                self.view_index += 1
            case Key.up:
                self.up = True
            case Key.down:
                self.down = True

    def on_release(self, key):
        match key:
            case Key.enter:
                self.enter = False
            case Key.right:
                self.forward = False
            case Key.up:
                self.up = False
            case Key.down:
                self.down = False

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

    def get_by_id(self, id: int) -> Optional[int]:
        return None

    def get_debug_table_values(self) -> List[debug.Debug_Table_Row_Value]:
        return [debug.Debug_Table_Row_Value(0, "speed", self.mph, "mph"), debug.Debug_Table_Row_Value(1, "status", self.status, "bool"), debug.Debug_Table_Row_Value(2, "dir", self.dir, "bool"), debug.Debug_Table_Row_Value(3, "pack temp", self.pack_temp, "C"), debug.Debug_Table_Row_Value(4, "motor temp", self.motor_temp, "C"), debug.Debug_Table_Row_Value(5, "state of charge", self.state_of_charge, "%"), debug.Debug_Table_Row_Value(6, "lv battery", self.lv_battery, "V")]

    def get_forward_button_pressed(self) -> bool:
        return self.forward

    def get_enter_button_pressed(self) -> bool:
        return self.enter

    def get_up_button_pressed(self) -> bool:
        return self.up

    def get_down_button_pressed(self) -> bool:
        return self.down

    def get_view_index(self) -> int:
        if self.view_index == 3:
            self.view_index = 0
        return self.view_index
