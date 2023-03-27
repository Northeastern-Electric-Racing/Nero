from typing import List


class DebugPlotLineData:
    def __init__(self, name: str, unit: str, data: List[float]):
        self.data = data
        self.name = name
        self.unit = unit
