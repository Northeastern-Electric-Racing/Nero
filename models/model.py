from typing import List, Optional, Dict
from modes.debug_mode.debug_utils import DebugPlotValue
from ner_processing.master_mapping import DATA_IDS
from modes.debug_mode.debug_utils import FaultInstance


class Model:
    def __init__(self) -> None:
        self.pinned_data: Dict[int, DebugPlotValue] = {}
        self.current_data: List[Optional[int]] = []
        self.pack_temp_data: List[Optional[int]] = []
        self.fault_instances: List[FaultInstance] = []
        self.average_cell_temps: List[Optional[int]] = []
        self.state_of_charge_deltas: List[Optional[int]] = []
        self.page_height = 540
        self.page_width = 1024
        pass

    def check_can(self) -> None:
        pass

    def get_precharge(self) -> Optional[int]:
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

    def get_max_cell_temp(self) -> Optional[int]:
        pass

    def get_max_cell_temp_chip_number(self) -> Optional[int]:
        pass

    def get_max_cell_temp_cell_number(self) -> Optional[int]:
        pass

    def get_max_cell_voltage(self) -> Optional[int]:
        pass

    def get_max_cell_voltage_chip_number(self) -> Optional[int]:
        pass

    def get_max_cell_voltage_cell_number(self) -> Optional[int]:
        pass

    def get_min_cell_temp(self) -> Optional[int]:
        pass

    def get_min_cell_temp_chip_number(self) -> Optional[int]:
        pass

    def get_min_cell_temp_cell_number(self) -> Optional[int]:
        pass

    def get_min_cell_voltage(self) -> Optional[int]:
        pass

    def get_min_cell_voltage_chip_number(self) -> Optional[int]:
        pass

    def get_min_cell_voltage_cell_number(self) -> Optional[int]:
        pass

    def get_ave_cell_temp(self) -> Optional[int]:
        pass

    def get_ave_cell_voltage(self) -> Optional[int]:
        pass

    def get_cell_delta(self) -> Optional[int]:
        pass

    def get_burning_cells(self) -> Optional[int]:
        pass

    def get_inverter_temp(self) -> Optional[int]:
        pass

    def get_motor_power(self) -> Optional[int]:
        pass

    def get_fan_power(self) -> Optional[int]:
        pass

    def get_torque_power(self) -> Optional[int]:
        pass

    def get_regen_power(self) -> Optional[int]:
        pass

    def get_BMS_state(self) -> Optional[int]:
        pass

    def get_BMS_fault(self) -> Optional[int]:
        pass

    def get_MPU_fault(self) -> Optional[int]:
        pass

    def get_dcl(self) -> Optional[int]:
        pass

    def get_ccl(self) -> Optional[int]:
        pass

    def get_pack_current(self) -> Optional[int]:
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

    def get_gforce_x(self) -> Optional[int]:
        pass

    def get_gforce_y(self) -> Optional[int]:
        pass

    def get_gforce_z(self) -> Optional[int]:
        pass

    def get_segment1_temp(self) -> Optional[int]:
        pass

    def get_segment2_temp(self) -> Optional[int]:
        pass

    def get_segment3_temp(self) -> Optional[int]:
        pass

    def get_segment4_temp(self) -> Optional[int]:
        pass

    def get_sd_card_status(self) -> Optional[int]:
        pass

    def update_pack_temp_data(self) -> None:
        if len(self.pack_temp_data) >= 600:
            self.pack_temp_data.pop()
        self.pack_temp_data.insert(0, self.get_pack_temp())

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

    def update_average_cell_temps(self) -> None:
        if len(self.average_cell_temps) >= 30:
            self.average_cell_temps.pop()
        self.average_cell_temps.insert(0, self.get_ave_cell_temp())

    def update_state_of_charge_deltas(self) -> None:
        if len(self.state_of_charge_deltas) >= 30:
            self.state_of_charge_deltas.pop()
        self.state_of_charge_deltas.insert(0, self.get_cell_delta())

