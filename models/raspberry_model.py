from typing import Optional, List
import socket
import os
import sys
from modes.debug_mode.debug_table_page import DebugTableRowValue
from models.model import Model
from modes.debug_mode.debug_utils import FaultInstance
from constants.data_ids import DATA_IDS
import threading


class RaspberryModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.current_data = [None] * len(DATA_IDS)
        os.chdir("/home/ner/Desktop/Nero/")

        os.environ.__setitem__("DISPLAY", ":0.0")

        threading.Thread(target=self.connect_to_ipc).start()
        pass

    def connect_to_ipc(self):
        socket_path = "/tmp/ipc.sock"
        try:
            os.unlink(socket_path)
        except OSError:
            pass

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(socket_path)

        s.listen()

        conn, addr = s.accept()
        os.system("/home/ner/Desktop/Ner_Processing/target/release/ner_processing")
        try:
            while True:
                data = conn.recv(1024)
                if data:
                    # print("BYTES: ", data)
                    data = data.decode()
                    data = data.split("index:")
                    try:
                        data.pop(0)
                        # print("STRING: ", data)
                        for i in range(len(data)):
                            values = data[i].split(",")
                            index = int(values[0])
                            split_value = values[1].split("}")
                            value = float(split_value[0])
                            test = split_value[1]
                            self.current_data[index] = value
                    except:
                        print("ERROR: ", sys.exc_info()[0])
        finally:
            conn.close()

    def get_mph(self) -> Optional[int]:
        mph = self.current_data[101]
        return round(mph) if mph is not None else mph

    def get_kph(self) -> Optional[int]:
        kph = self.current_data[101]
        return round(kph * 1.601) if kph is not None else kph

    def get_status(self) -> Optional[int]:
        status: Optional[int] = self.current_data[85]
        return int(status) == 1 if status is not None else None

    def get_dir(self) -> Optional[int]:
        dir = self.current_data[84]
        return int(dir) == 1 if dir is not None else None

    def get_pack_temp(self) -> Optional[int]:
        pack_temp = self.current_data[10]
        return round(pack_temp) if pack_temp is not None else pack_temp

    def get_motor_temp(self) -> Optional[int]:
        motor_temp = self.current_data[28]
        return round(motor_temp) if motor_temp is not None else motor_temp

    def get_state_of_charge(self) -> Optional[int]:
        return self.current_data[4]

    def get_lv_battery(self) -> Optional[int]:
        return self.current_data[63]

    def get_current(self) -> Optional[int]:
        return self.current_data[2]

    def get_max_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[13]
        return round(voltage, 3) if voltage is not None else voltage

    def get_max_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[121]

    def get_max_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[122]

    def get_max_cell_temp(self) -> Optional[int]:
        temp = self.current_data[114]
        return round(temp) if temp is not None else temp

    def get_max_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[115]

    def get_max_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[116]

    def get_min_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[15]
        return round(voltage, 3) if voltage is not None else voltage

    def get_min_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[123]

    def get_min_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[124]

    def get_min_cell_temp(self) -> Optional[int]:
        temp = self.current_data[117]
        return round(temp) if temp is not None else temp

    def get_min_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[118]

    def get_min_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[119]

    def get_ave_cell_temp(self) -> Optional[int]:
        temp = self.current_data[120]
        return round(temp) if temp is not None else temp

    def get_ave_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[17]
        return round(voltage, 3) if voltage is not None else voltage

    def get_cell_delta(self) -> Optional[int]:
        max = self.get_max_cell_voltage()
        min = self.get_min_cell_voltage()
        return round(max - min, 3) if max is not None and min is not None else None

    def get_pack_voltage(self) -> Optional[int]:
        voltage = self.current_data[1]
        return int(voltage) if voltage is not None else voltage

    def get_BMS_state(self) -> Optional[int]:
        return self.current_data[106]

    def get_pack_current(self) -> Optional[int]:
        return self.current_data[2]

    def get_dcl(self) -> Optional[int]:
        return self.current_data[89]

    def get_ccl(self) -> Optional[int]:
        return self.current_data[90]

    def get_gforce_x(self) -> Optional[int]:
        x_force = self.current_data[91]
        return round(x_force, 1) if x_force is not None else x_force

    def get_gforce_y(self) -> Optional[int]:
        y_force = self.current_data[92]
        return round(y_force, 1) if y_force is not None else y_force

    def get_gforce_z(self) -> Optional[int]:
        z_force = self.current_data[93]
        return round(z_force, 1) if z_force is not None else z_force

    def get_vbat(self) -> Optional[int]:
        vbat = self.current_data[139]
        return round(vbat, 1) if vbat is not None else vbat

    def get_balancing_cells(self) -> Optional[int]:
        return self.current_data[143]

    def get_sd_card_status(self) -> Optional[int]:
        return self.current_data[129]

    def get_segment1_temp(self) -> Optional[int]:
        return self.current_data[125]

    def get_segment2_temp(self) -> Optional[int]:
        return self.current_data[126]

    def get_segment3_temp(self) -> Optional[int]:
        return self.current_data[127]

    def get_segment4_temp(self) -> Optional[int]:
        return self.current_data[128]

    def get_motor_power(self) -> Optional[int]:
        return self.current_data[131]

    def get_fan_power(self) -> Optional[int]:
        return self.current_data[130]

    def get_torque_power(self) -> Optional[int]:
        return self.current_data[132]

    def get_regen_power(self) -> Optional[int]:
        return self.current_data[133]

    def get_traction_control(self) -> Optional[int]:
        return self.current_data[144]

    def get_BMS_fault(self) -> Optional[int]:
        fault_status = self.current_data[107]
        if fault_status is not None and int(fault_status) > 0:
            self.fault_instances.append(
                FaultInstance(
                    fault_status,
                    self.get_max_cell_temp(),
                    self.get_max_cell_voltage(),
                    self.get_ave_cell_temp(),
                    self.get_ave_cell_voltage(),
                    self.get_min_cell_temp(),
                    self.get_min_cell_voltage(),
                    self.get_pack_current(),
                    self.get_dcl(),
                    self.get_ccl(),
                )
            )
        return self.current_data[107]

    def get_debug_table_values(self) -> List[DebugTableRowValue]:
        table: List[DebugTableRowValue] = []
        for i in range(0, len(self.current_data)):
            value = self.current_data[i]
            table.append(
                DebugTableRowValue(
                    i,
                    DATA_IDS[i]["name"],
                    round(value, 3) if value is not None else "N/A",
                    DATA_IDS[i]["units"],
                )
            )
        return table

    # The way we get button data is by separating the data into binary and then parsing the bit that represents each button out,
    # if the binary string is too short then we know the button wasnt pressed so we can return 0
    def get_forward_button_pressed(self) -> Optional[str]:
        print(self.current_data[104])
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[6] if len(binary) >= 7 else 0
        return value

    def get_backward_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[7] if len(binary) >= 8 else 0
        return value

    def get_debug_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[2] if len(binary) >= 3 else 0
        return value

    def get_right_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[1] if len(binary) >= 2 else 0
        return value

    def get_enter_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[0]
        return value

    def get_up_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[5] if len(binary) >= 6 else 0
        return value

    def get_down_button_pressed(self) -> Optional[str]:
        value = self.current_data[104]
        if value is not None:
            binary = bin(int(value))
            binary = binary[2:][::-1]
            value = binary[4] if len(binary) >= 5 else 0
        return value

    def get_mode_index(self) -> Optional[float]:
        return self.current_data[105]
