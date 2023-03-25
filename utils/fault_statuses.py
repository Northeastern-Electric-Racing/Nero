from enum import Enum

class Fault_Statuses(Enum):
    Cells_Not_Balancing = 1
    Cell_Voltage_Too_High = 2
    Cell_Voltage_Too_Low = 3
    Pack_Too_High = 4
    Open_Wiring_Fault = 5
    Internal_Software_Fault = 6
    Internal_Thermal_Fault = 7
    Internal_Cell_Comm_Fault = 8
    Current_Sensor_Fault = 9
    Charge_Reading_Mismatch = 10
    Low_Cell_Voltage = 11
    Weak_Pack_Fault = 12
    External_Can_Fault = 13
    Discharge_Limit_Enforcement_Fault = 14
    Charger_Safety_Relay = 15
    Battery_Can_Fault = 16
    Charger_Can_Fault = 17
    Charge_Limit_Enforcement_Fault = 18