from ner_processing.master_mapping import DATA_IDS
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.message import Message
from typing import Optional
import can
import os
import platform


class NeroModel:
    def __init__(self) -> None:
        self.current_data = [None] * len(DATA_IDS)

        if not self.is_linux():
            return

        os.chdir("/home/ner/Desktop/Nero/")

        os.environ.__setitem__('DISPLAY', ':0.0')

        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')

        # socketcan_native
        self.can0 = can.interface.Bus(channel='can0', bustype='socketcan')

    def check_can(self):
        if not self.is_linux():
            return

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

    def get_status(self) -> Optional[bool]:
        status = self.current_data[85]
        if status is None:
            return None
        else:
            return status == 1

    def is_linux(self) -> bool:
        return platform.platform()[0:5] == "Linux"
