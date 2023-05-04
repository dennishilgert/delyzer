import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
from data_exporter import vvsData
import pandas as pd
import datetime
from interface.plotter_interface import PlotterInterface
from models.avg_time_delay_data import AvgTimeDelay


class Plotter(PlotterInterface):

    def __init__(self, ax):
        self.ax = ax

    def plot_avg_line_delay(self):
        data = vvsData.get_avg_line_delay()
        line_and_delay = [(obj.name, obj.delay) for obj in data]
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
        plt.show()


    def plot_avg_time_delay(self):
        data = vvsData.get_avg_time_delay()
        x_values = [datetime.datetime.fromtimestamp(obj.time) for obj in data]
        y_values = [t.delay for t in data]

        self.ax.plot(x_values, y_values)

        # Achsenbeschriftungen setzen
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Delay')

        # X-Achse auf 3 Stunden Interval setzen
        hours_3 = HourLocator(interval=3)
        self.ax.xaxis.set_major_locator(hours_3)

        # Datumsformat der X-Achse setzen
        date_formatter = DateFormatter('%H:00')
        self.ax.xaxis.set_major_formatter(date_formatter)
        # Titel setzen
        self.ax.set_title('Delay over Time')

        # Diagramm anzeigen
        plt.show()
