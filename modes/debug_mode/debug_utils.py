from typing import List


class DebugPlotValue:
    def __init__(self, name: str, unit: str, data: List[float]):
        self.data = data
        self.name = name
        self.unit = unit
