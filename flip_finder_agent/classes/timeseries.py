from typing import List
from flip_finder_agent.classes.time_interval import TimeInterval
class TimeSeries:
    def __init__(self, time_intervals: List[TimeInterval]):
        self.time_intervals = time_intervals