import pandas as pd
from datetime import datetime, time, timedelta
import random

# Erstelle Beispieldaten
class vvsData:

    def getData():
        return {
            "station_id": [1, 2, 3, 1, 2],
            "destination_id": [4, 5, 6, 4, 5],
            "direction": ["Nord", "Ost", "Süd", "Nord", "Ost"],
            "direction_from": ["Süd", "West", "Nord", "Süd", "West"],
            "line_number": ["L1", "L2", "L3", "L1", "L2"],
            "line_name": ["Linie 1", "Linie 2", "Linie 3", "Linie 1", "Linie 2"],
            "planned_departure_time": [time(8, 0), time(8, 30), time(9, 0), time(9, 30), time(10, 0)],
            "delay": [0, 5, 0, 10, 0],
            "current_date": [datetime.now()] * 5
        }

