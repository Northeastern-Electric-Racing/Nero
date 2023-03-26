from typing import List, Optional, Dict
from modes.debug_mode.debug_utils import DebugPlotValue
from ner_processing.master_mapping import DATA_IDS


class Model:
    def __init__(self) -> None:
        self.pinned_data_600: Dict[int, DebugPlotValue] = {}
        self.pinned_data_300: Dict[int, DebugPlotValue] = {}
        self.pinned_data_120: Dict[int, DebugPlotValue] = {}
        self.pinned_data_60: Dict[int, DebugPlotValue] = {}
        self.pinned_data_30: Dict[int, DebugPlotValue] = {}
        self.pinned_data = [self.pinned_data_30, self.pinned_data_60,
                            self.pinned_data_120, self.pinned_data_300, self.pinned_data_600]
        self.current_data: List[Optional[int]] = []
        self.pack_temp_data: List[Optional[int]] = []
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

    def get_current(self) -> Optional[int]:
        pass

    def get_balancing_cells(self) -> Optional[int]:
        pass

    def get_pack_voltage(self) -> Optional[int]:
        pass

    def get_max_cell_voltage(self) -> Optional[int]:
        pass

    def get_max_cell_id(self) -> Optional[int]:
        pass

    def get_min_cell_voltage(self) -> Optional[int]:
        pass

    def get_min_cell_id(self) -> Optional[int]:
        pass

    def get_cell_delta(self) -> Optional[int]:
        pass

    def get_burning_cells(self) -> Optional[int]:
        pass

    def get_BMS_state(self) -> Optional[int]:
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

    def update_pack_temp_data(self) -> None:
        if len(self.pack_temp_data) >= 600:
            self.pack_temp_data.pop()
        self.pack_temp_data.insert(0, self.get_pack_temp())

    def add_pinned_data(self, id: int) -> None:
        data = [round(self.current_data[id], 1) if self.current_data[id] is not None else self.current_data[id]]
        name = DATA_IDS[id]['name']
        unit = DATA_IDS[id]['units']
        for pinned_data in self.pinned_data:
            pinned_data[id] = DebugPlotValue(name=name, data=data, unit=unit)

    def remove_pinned_data(self, id: int) -> None:
        for pinned_data in self.pinned_data:
            if id in pinned_data:
                del pinned_data[id]

    def update_pinned_data(self, data_dict: Dict[int, DebugPlotValue]) -> None:
        for id in data_dict:
            if len(data_dict[id].data) >= 600:
                data_dict[id].data.pop()
            data_dict[id].data.insert(0, round(self.current_data[id], 1)
                                        if self.current_data[id] is not None else self.current_data[id])
