from typing import Optional, List
import random
from pynput.keyboard import Listener, Key
from pages.debug_table import Debug_Table_Row_Value


class MockModel:
    def __init__(self) -> None:
        self.mph = 60
        self.status = True
        self.dir = True
        self.pack_temp = 47
        self.motor_temp = 122
        self.state_of_charge = 88
        self.lv_battery = 88
        self.data = [self.mph, self.status, self.dir, self.pack_temp, self.motor_temp, self.state_of_charge, self.lv_battery]
        self.table = [Debug_Table_Row_Value(0, "speed", self.data[0], "mph"), Debug_Table_Row_Value(1, "status", self.data[1], "bool"), Debug_Table_Row_Value(2, "dir", self.data[2], "bool"), Debug_Table_Row_Value(
            3, "pack temp", self.data[3], "C"), Debug_Table_Row_Value(4, "motor temp", self.data[4], "C"), Debug_Table_Row_Value(5, "state of charge", self.data[5], "%"), Debug_Table_Row_Value(6, "lv battery", self.data[6], "V")]
        self.forward = 0
        self.backward = 0
        self.enter = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
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
                self.enter = 1
            case Key.right:
                self.forward = 1
                self.view_index += 1
            case Key.left:
                self.backward = 1
                self.view_index -= 1
            case Key.up:
                self.up = 1
            case Key.down:
                self.down = 1
            case Key.shift_l:
                self.left = 1
            case Key.shift_r:
                self.right = 1

    def on_release(self, key):
        match key:
            case Key.enter:
                self.enter = 0
            case Key.right:
                self.forward = 0
            case Key.left:
                self.backward = 0
            case Key.up:
                self.up = 0
            case Key.down:
                self.down = 0
            case Key.shift_l:
                self.left = 0
            case Key.shift_r:
                self.right = 0

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
        return self.data[id]

    def get_debug_table_values(self) -> List[Debug_Table_Row_Value]:
        return self.table

    def get_forward_button_pressed(self) -> int:
        return self.forward

    def get_enter_button_pressed(self) -> int:
        return self.enter

    def get_up_button_pressed(self) -> int:
        return self.up

    def get_down_button_pressed(self) -> int:
        return self.down

    def get_backward_button_pressed(self) -> int:
        return self.backward

    def get_left_button_pressed(self) -> int:
        return self.left

    def get_right_button_pressed(self) -> int:
        return self.right

    def get_view_index(self) -> int:
        if self.view_index == 3:
            self.view_index = 0
        return self.view_index
