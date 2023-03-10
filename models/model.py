from typing import List, Optional, Dict
from modes.debug_mode.debug_utils import DebugPlotValue
from ner_processing.master_mapping import DATA_IDS


class Model:
    def __init__(self) -> None:
        self.pinned_data: Dict[int, DebugPlotValue] = {}
        self.current_data: List[Optional[int]] = []
        pass

    def check_can(self) -> None:
        pass

    def get_mph(self) -> Optional[int]:
        pass

    def get_kph(self) -> Optional[int]:
        pass

    def get_status(self) -> Optional[int]:
        pass

    def get_dir(self) -> Optional[int]:
        pass

    def get_pack_temp(self) -> Optional[int]:
        pass

    def get_motor_temp(self) -> Optional[int]:
        pass

    def get_state_of_charge(self) -> Optional[int]:
        pass

    def get_lv_battery(self) -> Optional[int]:
        pass

    def get_by_id(self, id: int) -> Optional[int]:
        return self.current_data[id]

    def get_debug_table_values(self) -> List:
        pass

    def get_forward_button_pressed(self) -> Optional[str]:
        pass

    def get_backward_button_pressed(self) -> Optional[str]:
        pass

    def get_left_button_pressed(self) -> Optional[str]:
        pass

    def get_right_button_pressed(self) -> Optional[str]:
        pass

    def get_enter_button_pressed(self) -> Optional[str]:
        pass

    def get_up_button_pressed(self) -> Optional[str]:
        pass

    def get_down_button_pressed(self) -> Optional[str]:
        pass

    def get_mode_index(self):
        pass

    def add_pinned_data(self, id: int) -> None:
        self.pinned_data[id] = DebugPlotValue(name=DATA_IDS[id]['name'],
                                              data=[round(self.current_data[id], 1) if self.current_data[id] is not None else self.current_data[id]], unit=DATA_IDS[id]['units'])

    def remove_pinned_data(self, id: int) -> None:
        del self.pinned_data[id]

    def update_pinned_data(self) -> None:
        for id in self.pinned_data:
            if len(self.pinned_data[id].data) >= 600:
                self.pinned_data[id].data.pop()
            self.pinned_data[id].data.insert(0, round(self.current_data[id], 1)
                                             if self.current_data[id] is not None else self.current_data[id])
