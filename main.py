import os
import can

from PyQt6.QtCore import QDateTime
from ner_processing.message import Message
from ner_processing.master_mapping import MESSAGE_IDS
from ner_processing.master_mapping import DATA_IDS

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(
    channel='can0', bustype='socketcan')  # socketcan_native

try:
    while True:
        msg = can0.recv(10.0)

        if msg.arbitration_id in MESSAGE_IDS:
            timestamp = QDateTime.fromMSecsSinceEpoch(
                int(float(msg.timestamp)*1000))
            id = int(msg.arbitration_id)
            length = int(msg.dlc)
            data = [int(x) for x in msg.data]
            msg = Message(timestamp, id, data)
            decodedList = msg.decode()
            for data in decodedList:
                print(data.id + " (" + DATA_IDS[data.id] + "): " + data.value)

        if msg is None:
            print('Timeout occurred, no message.')
except KeyboardInterrupt:
    print('Terminating script')
    os.system('sudo ifconfig can0 down')
