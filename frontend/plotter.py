from datetime import datetime
import matplotlib.dates as mdates
from data_exporter import vvsData
from interface.plotter_interface import PlotterInterface


class Plotter(PlotterInterface):

    def __init__(self, ax, button_list, initial_line, logger):
        self.current_line = initial_line
        self.ax = ax
        self.button_list = button_list
        self.data_getter = vvsData(logger)
        self.logger = logger

    def plot_avg_line_delay(self):
        """
    Plots the average delay per line using the data from the dataGetter.

    Args:
        Uses ax from the MainWindow

    Side Effects:
        * Retrieves average line delay data using the dataGetter.
        * Plots the average delay per line using matplotlib.
        * Sets the title, x-axis label, and y-axis label of the plot.

    Tests:
        * Test that the function correctly plots the average delay per line.
        * Test that the x-axis labels correspond to the line numbers.
        * Test that the y-axis values represent the average delay in minutes.
    """
        for btn in self.button_list:
            btn.set_visible(False)

        data = self.data_getter.get_avg_line_delay()

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
        self.logger.info('Ploted line delay data')


    def plot_avg_station_delay(self, new_line='no new line given'):
        """
        Plots the average delay per station using the data from the dataGetter.

        Args:
            Uses ax from the MainWindow

        Side Effects:
            * Retrieves average station delay data using the dataGetter.
            * Plots the average delay per station using matplotlib.

        Tests:
            * Test that the function correctly plots the average delay per station.
            * Test that the x-axis labels correspond to the station IDs.
            * Test that the y-axis values represent the average delay in minutes.
        """
        if new_line != 'no new line given':
            self.current_line = new_line        #Change the current line. Needed in every ploting function.

        for btn in self.button_list:
            btn.set_visible(True)
        data = self.data_getter.get_avg_station_delay(self.current_line)
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
        self.logger.info('Ploted station delay data')



    def plot_avg_time_delay(self, new_line='no new line given'):
        """
        Plots the average delay over the course of a day, with data points for each half-hour increment.

        Args:
            uses ax from the MainWindow

        Side Effects:
            * Plots the average delay over the course of a day using matplotlib.
            * Sets the title, x-axis label, and y-axis label of the plot.
            * Configures the x-axis ticks to display in 3-hour intervals and formats the tick labels.

        Tests:
            * Test that the function correctly plots the average delay over the course of a day.
            * Test that the x-axis ticks are displayed in 3-hour intervals.
            * Test that the x-axis tick labels are formatted correctly ("HH:MM").
        """

        if new_line != 'no new line given':
            self.current_line = new_line        #Change the current line. Needed in every ploting function.

        for btn in self.button_list:
            btn.set_visible(True)
        data = self.data_getter.get_avg_time_delay(self.current_line)
        time_and_delay = [(datetime.strptime(obj.time, '%Y-%m-%dT%H:%M:%S'), obj.delay) for obj in data]

        time_and_delay.sort(key=lambda x: x[0])  # Make sure, data is corectly sorted
        x = [time for time, _ in time_and_delay]
        y = [delay for _, delay in time_and_delay]

        self.ax.plot(x, y, marker='o', linestyle='-')
        self.ax.set_title("Durchschnittliche Verspätung im Tagesverlauf")
        self.ax.set_xlabel("Uhrzeit")
        self.ax.set_ylabel("Verspätung in Minuten")

        # X-axes to 3h steps
        hours = mdates.HourLocator(interval=3)
        self.ax.xaxis.set_major_locator(hours)

        # X-axes only shows hours and minutes
        hour_fmt = mdates.DateFormatter('%H:%M')
        self.ax.xaxis.set_major_formatter(hour_fmt)

        # Turn labels
        self.ax.tick_params(axis='x', rotation=45)

        self.ax.figure.canvas.draw()
        self.logger.info('Ploted time delay data')