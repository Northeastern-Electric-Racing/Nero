from raspberry_model import RaspberryModel
from mock_model import MockModel
from nero_view import NeroView
from typing import Optional
import platform


class NeroController:
    def __init__(self) -> None:
        self.model = RaspberryModel() if platform.platform()[0:5] == "Linux" else MockModel()

    def run(self) -> None:
        view = NeroView(self)
        view.mainloop()

    def check_can(self) -> None:
        self.model.check_can()

    def get_mph(self) -> Optional[int]:
        return self.model.get_mph()

    def get_kph(self) -> Optional[int]:
        return self.model.get_kph()

    def get_status(self) -> Optional[bool]:
        return self.model.get_status()

    def get_dir(self) -> Optional[bool]:
        return self.model.get_dir()

    def get_pack_temp(self) -> Optional[int]:
        return self.model.get_pack_temp()

    def get_motor_temp(self) -> Optional[int]:
        return self.model.get_motor_temp()

    def get_state_of_charge(self) -> Optional[int]:
        return self.model.get_state_of_charge()

    def get_lv_battery(self) -> Optional[int]:
        return self.model.get_lv_battery()
