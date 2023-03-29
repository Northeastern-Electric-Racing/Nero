from typing import List
from utils.fault_statuses import Fault_Statuses

class DebugPlotValue:
    def __init__(self, name: str, unit: str, data: List[float]):
        self.data = data
        self.name = name
        self.unit = unit

class FaultInstance:
    def __init__(self, fault_decimal: int, max_cell_temp: int, max_cell_voltage: int, average_cell_temp: int, average_cell_voltage: int, min_cell_temp: int, min_cell_voltage: int, pack_current: int, dcl: int, ccl: int):
        self.faults: List[str] = []
        fault_bin = bin(fault_decimal)[2:]
        for i in range(0, len(fault_bin)):
            if fault_bin[i] == '1':
                self.faults.append(Fault_Statuses[i].name)
        self.max_cell_temp = max_cell_temp if max_cell_temp is not None else "N/A"
        self.max_cell_voltage = max_cell_voltage if max_cell_voltage is not None else "N/A"
        self.average_cell_temp = average_cell_temp if average_cell_temp is not None else "N/A"
        self.average_cell_voltage = average_cell_voltage if average_cell_voltage is not None else "N/A"
        self.min_cell_temp = min_cell_temp if min_cell_temp is not None else "N/A"
        self.min_cell_voltage = min_cell_voltage if min_cell_voltage is not None else "N/A"
        self.pack_current = pack_current if pack_current is not None else "N/A"
        self.dcl = dcl if dcl is not None else "N/A"
        self.ccl = ccl if ccl is not None else "N/A"