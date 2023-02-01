from typing import Optional
import random


class MockModel:
    def __init__(self) -> None:
        self.mph = 60
        self.status = True
        self.dir = True
        self.pack_temp = 47
        self.motor_temp = 122
        self.state_of_charge = 88
        self.lv_battery = 88
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
    
    def get_generic(self, id: int) -> any:
        return "N/A"