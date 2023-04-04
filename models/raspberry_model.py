from ner_processing.master_mapping import DATA_IDS
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.message import Message
from typing import Optional, List
import can
import os
from modes.debug_mode.debug_table_page import DebugTableRowValue
from models.model import Model
from modes.debug_mode.debug_utils import FaultInstance


class RaspberryModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.current_data = [None] * len(DATA_IDS)
        os.chdir("/home/ner/Desktop/Nero/")

        os.environ.__setitem__('DISPLAY', ':0.0')

        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')

        # socketcan_native
        self.can0 = can.interface.Bus(channel='can0', bustype='socketcan')

    def check_can(self) -> None:
        msg = self.can0.recv(10.0)

        if msg.arbitration_id in MESSAGE_IDS:
            timestamp = int(float(msg.timestamp)*1000)
            id = int(msg.arbitration_id)
            data = [int(x) for x in msg.data]
            msg = Message(timestamp, id, data)
            decodedList = msg.decode()
            for data in decodedList:
                self.current_data[data.id] = data.value

        if msg is None:
            print('Timeout occurred, no message.')

    def get_mph(self) -> Optional[int]:
        mph = self.current_data[101]
        return (round(mph) if mph is not None else mph)

    def get_kph(self) -> Optional[int]:
        kph = self.current_data[101]
        return (round(kph * 1.601) if kph is not None else kph)

    def get_status(self) -> Optional[int]:
        status: Optional[int] = self.current_data[85]
        return (status == 1 if status is not None else None)

    def get_dir(self) -> Optional[int]:
        dir = self.current_data[84]
        return (dir == 1 if dir is not None else None)

    def get_pack_temp(self) -> Optional[int]:
        pack_temp = self.current_data[10]
        return (round(pack_temp) if pack_temp is not None else pack_temp)

    def get_motor_temp(self) -> Optional[int]:
        motor_temp = self.current_data[28]
        return (round(motor_temp) if motor_temp is not None else motor_temp)

    def get_state_of_charge(self) -> Optional[int]:
        return self.current_data[4]

    def get_lv_battery(self) -> Optional[int]:
        return self.current_data[63]

    def get_current(self) -> Optional[int]:
        return self.current_data[2]

    def get_max_cell_voltage(self) -> Optional[int]:
        return self.current_data[13]

    def get_max_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[121]

    def get_max_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[122]

    def get_max_cell_temp(self) -> Optional[int]:
        return self.current_data[114]

    def get_max_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[115]

    def get_max_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[116]

    def get_min_cell_voltage(self) -> Optional[int]:
        return self.current_data[15]

    def get_min_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[123]

    def get_min_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[124]

    def get_min_cell_temp(self) -> Optional[int]:
        return self.current_data[117]

    def get_min_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[118]

    def get_min_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[119]

    def get_ave_cell_temp(self) -> Optional[int]:
        return self.current_data[120]

    def get_ave_cell_voltage(self) -> Optional[int]:
        return self.current_data[17]

    def get_pack_voltage(self) -> Optional[int]:
        return self.current_data[1]

    def get_BMS_state(self) -> Optional[int]:
        return self.current_data[106]

    def get_pack_current(self) -> Optional[int]:
        return self.current_data[2]

    def get_dcl(self) -> Optional[int]:
        return self.current_data[89]

    def get_ccl(self) -> Optional[int]:
        return self.current_data[90]
    
    def get_gforce_x(self) -> Optional[int]:
        return self.current_data[91]
    
    def get_gforce_y(self) -> Optional[int]:
        return self.current_data[92]
    
    def get_gforce_z(self) -> Optional[int]:
        return self.current_data[93]
    
    def get_precharge(self) -> Optional[int]:
        return self.current_data[125]

    def get_BMS_fault(self) -> Optional[int]:
        fault_status = self.current_data[107]
        if fault_status is not None and fault_status > 0:
            self.fault_instances.append(FaultInstance(fault_status, self.get_max_cell_temp(), self.get_max_cell_voltage(), self.get_ave_cell_temp(
            ), self.get_ave_cell_voltage(), self.get_min_cell_temp(), self.get_min_cell_voltage(), self.get_pack_current(), self.get_dcl(), self.get_ccl()))
        return self.current_data[107]

    def get_debug_table_values(self) -> List[DebugTableRowValue]:
        table: List[DebugTableRowValue] = []
        for i in range(0, len(self.current_data)):
            value = self.current_data[i]
            table.append(DebugTableRowValue(i, DATA_IDS[i]["name"],
                         value if value is not None else "N/A", DATA_IDS[i]["units"]))
        return table

    # The way we get button data is by separating the data into binary and then parsing the bit that represents each button out,
    # if the binary string is too short then we know the button wasnt pressed so we can return 0
    def get_forward_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[6] if len(binary) >= 7 else 0
        return value

    def get_backward_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[7] if len(binary) >= 8 else 0
        return value

    def get_debug_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[2] if len(binary) >= 3 else 0
        return value

    def get_right_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[1] if len(binary) >= 2 else 0
        return value

    def get_enter_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[0]
        return value

    def get_up_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[5] if len(binary) >= 6 else 0
        return value

    def get_down_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(value)
            binary = binary[2:][::-1]
            value = binary[4] if len(binary) >= 5 else 0
        return value

    def get_mode_index(self):
        return self.current_data[105]
