from typing import List
import requests

from models.avg_time_delay_data import AvgTimeDelay
from models.avg_line_delay_data import AvgLineDelay
from models.avg_station_delay_data import AvgStationDelay
from models.line_data import Line

from logger import setup_logger


# Erstelle Beispieldaten
class vvsData:
    """
    Sets up communication to the backend. One method for every Endpoint. Exports Data.

    Test:
        * Ensure that objects of the class can be created

    Tests for every method:
        * Test if data is exported correctly as a list of the correct objects.
        * Test if wrong incoming data format throws errors
        * Test if error occures if the endpoint cant be found.
    """

    def __init__(self, logger):
        self.url = "http://127.0.0.1:8000/"
        self.logger = logger

    def get_avg_line_delay(self) -> List[AvgLineDelay]:
        self.logger.info('Get line data')
        response = requests.get(self.url + "delay/lines", timeout=10)
        if response.status_code == 200:
            self.logger.info('Request to backend was successful')
            data = response.json()
            delay_data = data['delays']
            try:
                avg_line_delays = [AvgLineDelay(item['line_number'], item['direction'], item['delay']) for item in delay_data]
            except ValueError:
                self.logger.error('Failed to create AvgLineDelay list. Propably wrong data format.')
            return avg_line_delays
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None

    def get_avg_station_delay(self, line) -> List[AvgLineDelay]:
        self.logger.info('Get station data')
        response = requests.get(self.url + "delay/stations", timeout=10)
        if response.status_code == 200:
            self.logger.info('Request to backend was successful')
            data = response.json()
            delay_data = data['delays'][:10]
            try:
                avg_station_delays = [AvgStationDelay(item['Station'], item['delay']) for item in delay_data]
            except ValueError:
                self.logger.error('Failed to create AvgStationDelay list. Propably wrong data format.')
            return avg_station_delays
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None

    
    def get_avg_time_delay(self, line) -> List[AvgLineDelay]:
        self.logger.info('Get time data')
        response = requests.get(self.url + "delay/times", timeout=10)
        if response.status_code == 200:
            self.logger.info('Request to backend was successful')
            data = response.json()
            delay_data = data['times']
            print(delay_data)
            try:
                avg_time_delays = [AvgTimeDelay(item['timeslot_start'], item['delay']) for inner_list in delay_data for item in inner_list]
            except ValueError:
                self.logger.error('Failed to create AvgTimeDelay list. Propably wrong data format.')
            return avg_time_delays
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None


def get_lines(self) -> List[AvgLineDelay]:
        self.logger.info('Get lines')
        response = requests.get(self.url + "lines", timeout=10)
        if response.status_code == 200:
            self.logger.info('Request to backend was successful')
            data = response.json()['lines']
            try:
                lines = [Line(item['line_number'], item['direction']) for item in data]
            except ValueError:
                self.logger.error('Failed to create AvgStationDelay list. Propably wrong data format.')
            return lines
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None
