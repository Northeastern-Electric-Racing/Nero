from typing import Optional, List
import random
from pynput.keyboard import Listener, Key
from models.model import Model
from modes.debug_mode.debug_table_page import DebugTableRowValue
from constants.modes import MODES
import socket
import os
import threading

class MockModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.mph = 60
        self.status = True
        self.dir = True
        self.pack_temp = 30
        self.motor_temp = 40
        self.state_of_charge = 55
        self.lv_battery = 88
        self.current = 7.6
        self.is_burning = 0
        self.is_debug = 0
        self.bms_faults = 0
        self.mpu_faults = 0
        self.max_cell_voltage = 3.5
        self.max_cell_voltage_chip_number = 1
        self.max_cell_voltage_cell_number = 10
        self.max_cell_temp = 30
        self.max_cell_temp_chip_number = 5
        self.max_cell_temp_cell_number = 8
        self.min_cell_voltage = 3.2
        self.min_cell_voltage_chip_number = 2
        self.min_cell_voltage_cell_number = 3
        self.min_cell_temp = 25
        self.min_cell_temp_chip_number = 3
        self.min_cell_temp_cell_number = 4
        self.average_cell_voltage = 3.3
        self.average_cell_temp = 27
        self.pack_voltage = 3.4
        self.bms_state = 0
        self.pack_current = 4.6
        self.dcl = 280
        self.ccl = 300
        self.gforce_x = .5
        self.gforce_y = -1
        self.gforce_z = .5
        self.sd_card_status = 4
        self.segement1_temp = 30
        self.segement2_temp = 50
        self.segement3_temp = 35
        self.segement4_temp = 15
        self.motor_power = 100
        self.fan_power = 100
        self.torque_power = 100
        self.regen_power = 1
        self.mode_index = 0
        self.state_of_charge_delta = -1
        self.inverter_temp = 30
        self.current_data = [self.mph, self.status, self.dir, self.pack_temp,
                             self.motor_temp, self.state_of_charge, self.lv_battery, self.current, self.bms_faults, self.mpu_faults, self.mode_index, self.max_cell_voltage, self.max_cell_voltage_chip_number, self.max_cell_voltage_cell_number, self.max_cell_temp, self.max_cell_temp_chip_number, self.max_cell_temp_cell_number, self.min_cell_voltage, self.min_cell_voltage_chip_number, self.min_cell_voltage_cell_number, self.min_cell_temp, self.min_cell_temp_chip_number, self.min_cell_temp_cell_number, self.average_cell_voltage, self.average_cell_temp, self.pack_voltage, self.bms_state, self.pack_current, self.dcl, self.ccl, self.gforce_x, self.gforce_y, self.gforce_z, self.sd_card_status, self.segement1_temp, self.segement2_temp, self.segement3_temp, self.segement4_temp, self.motor_power, self.fan_power, self.torque_power, self.regen_power, self.is_burning, self.state_of_charge_delta, self.inverter_temp]
        self.forward = 0
        self.backward = 0
        self.enter = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
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

        while True:
            conn, addr = s.accept()
            try:
                while True:
                    data = conn.recv(16)
                    if data:
                        print("received ", data)
            finally:
                conn.close()

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

        if rng > 70 and rng < 75:
            self.lv_battery += 1
        if rng > 60 and rng < 65:
            self.lv_battery -= 1

        if rng > 80 and rng < 85:
            self.current += .2
        if rng > 90 and rng < 95:
            self.current -= .3

        if rng > 100 and rng < 105:
            self.bms_faults = random.randint(0, 65536)  # 2^16
        if rng > 110 and rng < 115:
            self.bms_faults = 0

        if rng > 120 and rng < 125:
            self.mpu_faults = random.randint(0, 65536)  # 2^16
        if rng > 130 and rng < 135:
            self.mpu_faults = 0

        if rng > 140 and rng < 145:
            self.max_cell_voltage += 0.4
        if rng > 150 and rng < 155:
            self.max_cell_voltage -= 0.4

        if rng > 160 and rng < 165:
            self.max_cell_voltage_chip_number = random.randint(0, 8)  # 8 chips

        if rng > 170 and rng < 175:
            self.max_cell_voltage_cell_number = random.randint(0, 22)  # 22 thermistors

        if rng > 180 and rng < 185:
            self.max_cell_temp += 1
        if rng > 190 and rng < 195:
            self.max_cell_temp -= 1

        if rng > 200 and rng < 205:
            self.max_cell_temp_chip_number = random.randint(0, 8)

        if rng > 210 and rng < 215:
            self.max_cell_temp_cell_number = random.randint(0, 22)

        if rng > 220 and rng < 225:
            self.min_cell_voltage += 0.4
        if rng > 230 and rng < 235:
            self.min_cell_voltage -= 0.4

        if rng > 240 and rng < 245:
            self.min_cell_voltage_chip_number = random.randint(0, 8)

        if rng > 250 and rng < 255:
            self.min_cell_voltage_cell_number = random.randint(0, 22)

        if rng > 260 and rng < 265:
            self.min_cell_temp += 1
        if rng > 270 and rng < 275:
            self.min_cell_temp -= 1

        if rng > 280 and rng < 285:
            self.min_cell_temp_chip_number = random.randint(0, 8)

        if rng > 290 and rng < 295:
            self.min_cell_temp_cell_number = random.randint(0, 22)

        if rng > 300 and rng < 305:
            self.average_cell_voltage += 0.4
        if rng > 310 and rng < 315:
            self.average_cell_voltage -= 0.4

        if rng > 320 and rng < 325:
            self.average_cell_temp += 1
        if rng > 330 and rng < 335:
            self.average_cell_temp -= 1

        if rng > 340 and rng < 345:
            self.pack_voltage += 0.4
        if rng > 350 and rng < 355:
            self.pack_voltage -= 0.4

        if rng > 360 and rng < 365:
            self.pack_current += 0.2
        if rng > 370 and rng < 375:
            self.pack_current -= 0.2

        if rng > 380 and rng < 385:
            self.dcl += 10
        if rng > 390 and rng < 395:
            self.dcl -= 10

        if rng > 400 and rng < 405:
            self.ccl += 10
        if rng > 410 and rng < 415:
            self.ccl -= 10

        if rng > 420 and rng < 425:
            self.gforce_x += 0.1
        if rng > 430 and rng < 435:
            self.gforce_x -= 0.1

        if rng > 440 and rng < 445:
            self.gforce_y += 0.1
        if rng > 450 and rng < 455:
            self.gforce_y -= 0.1

        if rng > 460 and rng < 465:
            self.gforce_z += 0.1
        if rng > 470 and rng < 475:
            self.gforce_z -= 0.1

        if rng > 480 and rng < 485:
            self.sd_card_status = random.randint(0, 3)

        if rng > 490 and rng < 495:
            self.segement1_temp += 1
        if rng > 500 and rng < 505:
            self.segement1_temp -= 1

        if rng > 510 and rng < 515:
            self.segement2_temp += 1
        if rng > 520 and rng < 525:
            self.segement2_temp -= 1

        if rng > 530 and rng < 535:
            self.segement3_temp += 1
        if rng > 540 and rng < 545:
            self.segement3_temp -= 1

        if rng > 550 and rng < 555:
            self.segement4_temp += 1
        if rng > 560 and rng < 565:
            self.segement4_temp -= 1

        if rng > 570 and rng < 575:
            self.state_of_charge_delta += 1
        if rng > 580 and rng < 585:
            self.state_of_charge_delta -= 1

        if rng > 590 and rng < 595:
            self.inverter_temp += 1
        if rng > 600 and rng < 605:
            self.inverter_temp -= 1

        self.current_data = [self.mph, self.status, self.dir, self.pack_temp,
                             self.motor_temp, self.state_of_charge, self.lv_battery, self.current, self.bms_faults, self.mpu_faults, self.mode_index, self.max_cell_voltage, self.max_cell_voltage_chip_number, self.max_cell_voltage_cell_number, self.max_cell_temp, self.max_cell_temp_chip_number, self.max_cell_temp_cell_number, self.min_cell_voltage, self.min_cell_voltage_chip_number, self.min_cell_voltage_cell_number, self.min_cell_temp, self.min_cell_temp_chip_number, self.min_cell_temp_cell_number, self.average_cell_voltage, self.average_cell_temp, self.pack_voltage, self.bms_state, self.pack_current, self.dcl, self.ccl, self.gforce_x, self.gforce_y, self.gforce_z, self.sd_card_status, self.segement1_temp, self.segement2_temp, self.segement3_temp, self.segement4_temp, self.motor_power, self.fan_power, self.torque_power, self.regen_power, self.is_burning, self.state_of_charge_delta, self.inverter_temp]

    def on_press(self, key):
        match key:
            case Key.enter:
                self.enter = 1
            case Key.right:
                self.forward = 1
                self.mode_index = (self.mode_index + 1) if self.mode_index < len(MODES) - 1 else 0
            case Key.left:
                self.backward = 1
                self.mode_index = (self.mode_index - 1) if self.mode_index > 0 else len(MODES) - 1
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
        current = self.current_data[7]
        return (round(current, 1) if current is not None else current)

    def get_BMS_fault(self) -> Optional[int]:
        fault_status = self.current_data[8]
        if fault_status is not None and fault_status > 0:
            self.fault_instances.append(FaultInstance(fault_status, self.get_max_cell_temp(), self.get_max_cell_voltage(), self.get_ave_cell_temp(
            ), self.get_ave_cell_voltage(), self.get_min_cell_temp(), self.get_min_cell_voltage(), self.get_pack_current(), self.get_dcl(), self.get_ccl()))
        return fault_status

    def get_MPU_fault(self) -> Optional[int]:
        return self.current_data[9]

    def get_mode_index(self) -> int:
        return self.current_data[10]

    def get_max_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[11]
        return (round(voltage, 1) if voltage is not None else voltage)

    def get_max_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[12]

    def get_max_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[13]

    def get_max_cell_temp(self) -> Optional[int]:
        temp = self.current_data[14]
        return (round(temp) if temp is not None else temp)

    def get_max_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[15]

    def get_max_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[16]

    def get_min_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[17]
        return round(voltage, 1) if voltage is not None else voltage

    def get_min_cell_voltage_chip_number(self) -> Optional[int]:
        return self.current_data[18]

    def get_min_cell_voltage_cell_number(self) -> Optional[int]:
        return self.current_data[19]

    def get_min_cell_temp(self) -> Optional[int]:
        temp = self.current_data[20]
        return (round(temp) if temp is not None else temp)

    def get_min_cell_temp_chip_number(self) -> Optional[int]:
        return self.current_data[21]

    def get_min_cell_temp_cell_number(self) -> Optional[int]:
        return self.current_data[22]

    def get_ave_cell_temp(self) -> Optional[int]:
        temp = self.current_data[23]
        return (round(temp) if temp is not None else temp)

    def get_ave_cell_voltage(self) -> Optional[int]:
        voltage = self.current_data[24]
        return (round(voltage, 1) if voltage is not None else voltage)

    def get_pack_voltage(self) -> Optional[int]:
        voltage = self.current_data[25]
        return (round(voltage, 1) if voltage is not None else voltage)

    def get_BMS_state(self) -> Optional[int]:
        return self.current_data[26]

    def get_pack_current(self) -> Optional[int]:
        return self.current_data[27]

    def get_dcl(self) -> Optional[int]:
        return self.current_data[28]

    def get_ccl(self) -> Optional[int]:
        return self.current_data[29]

    def get_gforce_x(self) -> Optional[int]:
        x_force = self.current_data[30]
        return (round(x_force, 1) if x_force is not None else x_force)

    def get_gforce_y(self) -> Optional[int]:
        y_force = self.current_data[31]
        return (round(y_force, 1) if y_force is not None else y_force)

    def get_gforce_z(self) -> Optional[int]:
        z_force = self.current_data[32]
        return (round(z_force, 1) if z_force is not None else z_force)

    def get_sd_card_status(self) -> Optional[int]:
        return self.current_data[33]

    def get_segment1_temp(self) -> Optional[int]:
        return self.current_data[34]

    def get_segment2_temp(self) -> Optional[int]:
        return self.current_data[35]

    def get_segment3_temp(self) -> Optional[int]:
        return self.current_data[36]

    def get_segment4_temp(self) -> Optional[int]:
        return self.current_data[37]

    def get_motor_power(self) -> Optional[int]:
        return self.current_data[38]

    def get_fan_power(self) -> Optional[int]:
        return self.current_data[39]

    def get_torque_power(self) -> Optional[int]:
        return self.current_data[40]

    def get_regen_power(self) -> Optional[int]:
        return self.current_data[41]

    def get_burning_cells(self) -> Optional[int]:
        return self.current_data[42]

    def update_state_of_charge_deltas(self) -> None:
        self.state_of_charge_deltas.append(self.current_data[43])
        if len(self.state_of_charge_deltas) > 30:
            self.state_of_charge_deltas.pop(0)

    def get_inverter_temp(self) -> Optional[int]:
        return self.current_data[44]

    def get_debug_table_values(self) -> List[DebugTableRowValue]:
        table: List[DebugTableRowValue] = []
        for i in range(0, len(self.current_data)):
            value = self.current_data[i]
            table.append(DebugTableRowValue(i, DATA_IDS[i]["name"],
                         round(value, 3) if value is not None else "N/A", DATA_IDS[i]["units"]))
        return table

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

    def get_right_button_pressed(self) -> int:
        return self.right

    def get_debug_pressed(self) -> int:
        return self.is_debug
