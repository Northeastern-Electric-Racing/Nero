from ner_processing.master_mapping import DATA_IDS
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.message import Message
from typing import Optional
import can
import os


class RaspberryModel:
    def __init__(self) -> None:
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
                print(str(data.id) +
                      " (" + str(DATA_IDS[data.id]) + "): " + str(data.value))

        if msg is None:
            print('Timeout occurred, no message.')

    def get_mph(self) -> Optional[int]:
        mph = self.current_data[45]
        return (round(mph * 0.01272) if mph is not None else mph)

    def get_kph(self) -> Optional[int]:
        kph = self.current_data[45]
        return (round(kph * 0.02047) if kph is not None else kph)

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
    
    def get_generic(self, id: int) -> Optional[int]:
        return self.current_data[id]
