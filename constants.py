from modes.efficiency_mode.efficiency_mode import EfficiencyMode
from modes.off_mode.off_mode import OffMode
from modes.charging_mode.charging_mode import ChargingMode
from modes.pit_lane_mode.pit_lane_mode import PitLaneMode
from modes.reverse_mode.reverse_mode import ReverseMode
from modes.speed_mode.speed_mode import SpeedMode
MODES = (OffMode, PitLaneMode, EfficiencyMode, SpeedMode, ReverseMode, ChargingMode)
FAULTS = ["Cells_Not_Balancing",
          "Cell_Voltage_Too_High",
          "Cell_Voltage_Too_Low",
          "Pack_Too_High",
          "Open_Wiring_Fault",
          "Internal_Software_Fault",
          "Internal_Thermal_Fault",
          "Internal_Cell_Comm_Fault",
          "Current_Sensor_Fault",
          "Charge_Reading_Mismatch",
          "Low_Cell_Voltage",
          "Weak_Pack_Fault",
          "External_Can_Fault",
          "Discharge_Limit_Enforcement_Fault",
          "Charger_Safety_Relay",
          "Battery_Can_Fault",
          "Charger_Can_Fault",
          "Charge_Limit_Enforcement_Fault"]
