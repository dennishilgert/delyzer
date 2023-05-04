import datetime
import random

class AvgTimeDelay:
    def __init__(self, delay):
        _today = datetime.datetime.now().date()  # heutiges Datum erfassen
        _random_time = datetime.datetime.combine(_today, datetime.time.min) + \
                      datetime.timedelta(minutes=random.randint(0, 1439)) # zufällige Zeit innerhalb des heutigen Tages erstellen
        self.time = _random_time.timestamp()  # Zeitstempel aus der zufälligen Zeit erstellen
        self.delay = delay