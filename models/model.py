from typing import List, Optional, Dict
from modes.debug_mode.debug_utils import DebugPlotLineData
from ner_processing.master_mapping import DATA_IDS
MAXIMUM_DATA_POINTS = 12000

class Model:
    def __init__(self) -> None:
        self.pinned_data: Dict[int, DebugPlotLineData] = {}
        self.current_data: List[Optional[int]] = []
        self.pack_temp_data: List[Optional[int]] = []
        self.page_height = 540
        self.page_width = 1024
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

    def get_BMS_fault(self) -> Optional[int]:
        pass

    def get_MPU_fault(self) -> Optional[int]:
        pass

    def get_by_id(self, id: int) -> Optional[int]:
        return self.current_data[id]

    def get_debug_table_values(self) -> List:
        pass

    def get_forward_button_pressed(self) -> Optional[str]:
        pass

    def get_backward_button_pressed(self) -> Optional[str]:
        pass

    def get_debug_pressed(self) -> Optional[str]:
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
        # if we already have 600 values, pop the last one and then insert the newest value at zero
        if len(self.pack_temp_data) >= 600:
            self.pack_temp_data.pop()
        self.pack_temp_data.insert(0, self.get_pack_temp())

    def add_pinned_data(self, id: int) -> None:
        # add the given id to all pinned data
        value = self.current_data[id]
        data = round(value, 1) if value is not None else value
        name = DATA_IDS[id]['name']
        unit = DATA_IDS[id]['units']
        self.pinned_data[id] = DebugPlotLineData(name=name, data=[data], unit=unit)

    def remove_pinned_data(self, id: int) -> None:
        # remove the given id from all pinned data
        del self.pinned_data[id]

    def update_pinned_data(self) -> None:
        # update the given pinned data, if we already have MAXIMUM_DATA_POINTS values, pop the last one and then insert the newest value at zero
        for id in self.pinned_data:
            if len(self.pinned_data[id].data) >= MAXIMUM_DATA_POINTS:
                self.pinned_data[id].data.pop()
            self.pinned_data[id].data.insert(0, round(self.current_data[id], 1)
                                      if self.current_data[id] is not None else self.current_data[id])
