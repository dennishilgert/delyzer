from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
from data_exporter import vvsData
from interface.plotter_interface import PlotterInterface
from models.avg_time_delay_data import AvgTimeDelay


class Plotter(PlotterInterface):

    def __init__(self, ax):
        self.ax = ax
        self.dataGetter = vvsData()

    def plot_avg_line_delay(self):
        data = self.dataGetter.get_avg_line_delay()
        line_and_delay = [(obj.line_number, obj.delay) for obj in data]
        line_delay_dict = {}
        for line, delay in line_and_delay:
            if line in line_delay_dict:
                line_delay_dict[line].append(delay)
            else:
                line_delay_dict[line] = [delay]
        line_and_avg_delay = []
        for line, delays in line_delay_dict.items():
            avg_delay = sum(delays) / len(delays)
            line_and_avg_delay.append((line, avg_delay))
        line_and_avg_delay.sort(key=lambda x: x[1])
        x = [line for line, _ in line_and_avg_delay]
        y = [avg_delay for _, avg_delay in line_and_avg_delay]
        self.ax.bar(x, y)
        self.ax.set_title("Durchschnittliche Verspätung")
        self.ax.set_xlabel("Linie")
        self.ax.set_ylabel("Verspätung in Minuten")
        self.ax.figure.canvas.draw()


    def plot_avg_station_delay(self):
        data = self.dataGetter.get_avg_station_delay()
        station_and_delay = [(obj.station, obj.delay) for obj in data]
        station_delay_dict = {}
        for station, delay in station_and_delay:
            if station in station_delay_dict:
                station_delay_dict[station].append(delay)
            else:
                station_delay_dict[station] = [delay]
        station_and_avg_delay = []
        for station, delays in station_delay_dict.items():
            avg_delay = sum(delays) / len(delays)
            station_and_avg_delay.append((station, avg_delay))
        station_and_avg_delay.sort(key=lambda x: x[1], reverse=True)
        x = [station_id for station_id, _ in station_and_avg_delay]
        for station in station_and_avg_delay:
            print(station)
        y = [avg_delay for _, avg_delay in station_and_avg_delay]
        self.ax.bar(x, y)
        self.ax.set_title("Durchschnittliche Verspätung pro Station")
        self.ax.set_xlabel("Station")
        self.ax.set_ylabel("Verspätung in Minuten")
        self.ax.figure.canvas.draw()



    def plot_avg_time_delay(self):
        
        data = self.dataGetter.get_avg_time_delay()
        time_and_delay = [(datetime.strptime(obj.time, '%Y-%m-%dT%H:%M:%S'), obj.delay) for obj in data]

        time_and_delay.sort(key=lambda x: x[0])  # Sortiere nach Zeit, um sicherzustellen, dass die Daten in der richtigen Reihenfolge angezeigt werden
        x = [time for time, _ in time_and_delay]
        y = [delay for _, delay in time_and_delay]

        self.ax.plot(x, y, marker='o', linestyle='-')
        self.ax.set_title("Durchschnittliche Verspätung im Tagesverlauf")
        self.ax.set_xlabel("Uhrzeit")
        self.ax.set_ylabel("Verspätung in Minuten")

        # Setze die x-Achsen-Ticks in 3-Stunden-Schritten
        hours = mdates.HourLocator(interval=3)
        self.ax.xaxis.set_major_locator(hours)

        # Format für die x-Achsen-Ticks (nur Stunden anzeigen)
        hour_fmt = mdates.DateFormatter('%H:%M')
        self.ax.xaxis.set_major_formatter(hour_fmt)

        # Drehen der x-Achsen-Ticks für bessere Lesbarkeit
        self.ax.tick_params(axis='x', rotation=45)

        self.ax.figure.canvas.draw()