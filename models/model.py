from typing import List, Optional, Dict


class Model:
    def __init__(self) -> None:
        self.pinned_data: Dict[int, List[float]] = {}
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
        self.pinned_data[id] = [self.current_data[id]]

    def update_pinned_data(self) -> None:
        for id in self.pinned_data:
            self.pinned_data[id].append(self.current_data[id])
    
    def remove_pinned_data(self, id: int) -> None:
        self.pinned_data[id].pop()