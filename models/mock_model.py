from typing import Optional, List
import random
from pynput.keyboard import Listener, Key
from modes.debug_mode.debug_table_page import DebugTableRowValue
from models.model import Model


class MockModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.mph = 60
        self.status = True
        self.dir = True
        self.pack_temp = 47
        self.motor_temp = 122
        self.state_of_charge = 55
        self.lv_battery = 88
        self.current = 7.6
        self.is_burning = 0
        self.is_charging = 0
        self.is_debug = 0
        self.bms_faults = 0
        self.mpu_faults = 0
        self.current_data = [self.mph, self.status, self.dir, self.pack_temp,
                             self.motor_temp, self.state_of_charge, self.lv_battery, self.current, self.is_burning, self.is_charging]
        self.table = [DebugTableRowValue(0, "speed", self.current_data[0], "mph"), DebugTableRowValue(1, "status", self.current_data[1], "bool"), DebugTableRowValue(2, "dir", self.current_data[2], "bool"), DebugTableRowValue(
            3, "pack temp", self.current_data[3], "C"), DebugTableRowValue(4, "motor temp", self.current_data[4], "C"), DebugTableRowValue(5, "state of charge", self.current_data[5], "%"), DebugTableRowValue(6, "lv battery", self.current_data[6], "V"), DebugTableRowValue(7, "current", self.current_data[7], "A"), DebugTableRowValue(8, "is burning", self.current_data[8], "bool")]
        self.forward = 0
        self.backward = 0
        self.enter = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.mode_index = 0
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        pass

    def check_can(self) -> None:
        rng = random.randint(0, 10000)
        if rng < 5 and rng >= 0:
            self.mph += 1
        elif rng >= 5 and rng <= 10:
            self.mph -= 1

        if rng < 3:
            self.motor_temp += 1
        elif rng >= 985 and rng < 988:
            self.motor_temp -= 1

        if rng < 2:
            self.pack_temp += 1
        elif rng >= 990 and rng < 992:
            self.pack_temp -= 1

        if rng < 5:
            self.state_of_charge += 1
        elif rng >= 100 and rng < 105:
            self.state_of_charge -= 1

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

        if rng == 400:
            self.is_burning = 0
        if rng > 50 and rng < 55:
            self.is_burning = 1

        if rng == 100:
            self.is_charging = 1
        if rng > 48 and rng < 53:
            self.is_charging = 0

        self.current_data = [self.mph, self.status, self.dir, self.pack_temp,
                             self.motor_temp, self.state_of_charge, self.lv_battery, self.current, self.is_burning, self.is_charging]

    def on_press(self, key):
        match key:
            case Key.enter:
                self.enter = 1
            case Key.right:
                self.forward = 1
                self.mode_index = (self.mode_index + 1) if self.mode_index < 5 else 0
            case Key.left:
                self.backward = 1
                self.mode_index = (self.mode_index - 1) if self.mode_index > 0 else 5
            case Key.up:
                self.up = 1
            case Key.down:
                self.down = 1
            case Key.shift_l:
                self.is_debug = 1
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
                self.is_debug = 0
            case Key.shift_r:
                self.right = 0

    def get_burning_cells(self) -> Optional[int]:
        return self.is_burning

    def get_mph(self) -> Optional[int]:
        return self.current_data[0]

    def get_kph(self) -> Optional[int]:
        return round(self.current_data[0] * 1.609)

    def get_status(self) -> Optional[bool]:
        return self.current_data[1]

    def get_dir(self) -> Optional[bool]:
        return self.current_data[2]

    def get_pack_temp(self) -> Optional[int]:
        return self.current_data[3]

    def get_motor_temp(self) -> Optional[int]:
        return self.current_data[4]

    def get_state_of_charge(self) -> Optional[int]:
        return self.current_data[5]

    def get_lv_battery(self) -> Optional[int]:
        return self.current_data[6]

    def get_current(self) -> Optional[float]:
        return self.current_data[7]

    def get_BMS_fault(self) -> Optional[int]:
        return self.bms_faults

    def get_MPU_fault(self) -> Optional[int]:
        return self.mpu_faults

    def get_debug_table_values(self) -> List[DebugTableRowValue]:
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

    def get_debug_pressed(self) -> int:
        return self.is_debug

    def get_right_button_pressed(self) -> int:
        return self.right

    def get_mode_index(self) -> int:
        return self.mode_index
