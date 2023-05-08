import pandas as pd
from datetime import datetime, time, timedelta
import random
from typing import List
import requests

from models.avg_time_delay_data import AvgTimeDelay
from models.avg_line_delay_data import AvgLineDelay


# Erstelle Beispieldaten
class vvsData:

    def __init__(self):
        self.url = "http://127.0.0.1:8000/"

    def get_avg_line_delay(self) -> List[AvgLineDelay]:
        response = requests.get(self.url + "delay/lines", timeout=10)
        if response.status_code == 200:
            print("Anfrage erfolgreich")
            data = response.json()
            print(data)
            delay_data = data['delays']
            avg_line_delays = [AvgLineDelay(item['line_number'], item['direction'], item['delay']) for item in delay_data]
            return avg_line_delays
        else:
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None
    
    def get_avg_station_delay(self) -> List[AvgLineDelay]:
        response = requests.get(self.url + "delay/time", timeout=10)
        if response.status_code == 200:
            print("Anfrage erfolgreich")
            data = response.json()
            print(data)
            delay_data = data['delays']
            avg_line_delays = [AvgLineDelay(item['line_number'], item['direction'], item['delay']) for item in delay_data]
            return avg_line_delays
        else:
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None

    
    def get_avg_time_delay(self) -> List[AvgTimeDelay]:
        dataArray = [AvgTimeDelay(random.randint(0,10)) for i in range(48)]
        return sorted(dataArray, key=lambda x: x.time)

