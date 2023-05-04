import pandas as pd
from datetime import datetime, time, timedelta
import random
from typing import List

from models.avg_time_delay_data import AvgTimeDelay
from models.avg_line_delay_data import AvgLineDelay

# Erstelle Beispieldaten
class vvsData:

    def get_avg_line_delay() -> List[AvgLineDelay]:
        names = ["U1", "U2", "U3", "U4", "U5"]
        directions = ["N", "S", "E", "W"]
        objects = []
        for i in range(30):
            name = random.choice(names)
            direction = random.choice(directions)
            delay = random.randint(0, 15)
            obj = AvgLineDelay(name, direction, delay)
            objects.append(obj)
        dataArray = sorted(objects, key=lambda x: x.delay)
        return dataArray
    
    def get_avg_time_delay() -> List[AvgTimeDelay]:
        dataArray = [AvgTimeDelay(random.randint(0,10)) for i in range(48)]
        return sorted(dataArray, key=lambda x: x.time)

