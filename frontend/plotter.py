"""
Get, plot and switch between plots.

Tests:
    *Test if all classes are correct and creatable.
    *Test if if switching between Plooter functions work with an Swapper object.
"""

from datetime import datetime
import matplotlib.dates as mdates
from interface.plotter_interface import PlotterInterface

from typing import List
import requests

from models.avg_time_delay_data import AvgTimeDelay
from models.avg_line_delay_data import AvgLineDelay
from models.avg_station_delay_data import AvgStationDelay
from models.avg_station_risk_data import AvgStationRisk
from models.line_data import Line



# Erstelle Beispieldaten
class VvsData:
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
        response = requests.get(self.url + "delay/stations/"+line.line_number + '/' + line.direction, timeout=10)
        if response.status_code == 200:
            self.logger.info('Request to backend was successful')
            data = response.json()
            delay_data = data['delays'][:10]
            try:
                avg_station_delays = [AvgStationDelay(item['Name mit Ort'], item['delay']) for item in delay_data]
            except ValueError:
                self.logger.error('Failed to create AvgStationDelay list. Propably wrong data format.')
            return avg_station_delays
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None
        
    def get_avg_station_risk(self, line) -> List[AvgStationRisk]:
        self.logger.info('Get station risk data')
        response = requests.get(self.url + "propability/stations/"+line.line_number + '/' + line.direction, timeout=10)
        if response.status_code == 200:
            print(response)
            self.logger.info('Request to backend was successful')
            data = response.json()
            delay_data = data['propability'][:10]
            try:
                avg_station_delays = [AvgStationRisk(item['Name mit Ort'], item['delay']) for item in delay_data]
            except ValueError:
                self.logger.error('Failed to create AvgStationRisk list. Propably wrong data format.')
            return avg_station_delays
        else:
            self.logger.error('Failed when trying to get data from backend')
            print("Fehler beim Abrufen von Daten. HTTP-Statuscode: ", response.status_code)
            return None



    
    def get_avg_time_delay(self, line) -> List[AvgLineDelay]:
        self.logger.info('Get time data')
        response = requests.get(self.url + "delay/times/" + line.line_number + '/' + line.direction, timeout=10)
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


class Plotter(PlotterInterface):

    """
    Plots different graphs and takes data from VvsData.

    Args:
    *ax: graph to plot in
    *button_list: buttons to switch lines
    *initial_line: line to plot first
    *logger: logger

    Tests:
    *Test if it is possible to plot test data to the graph.
    *Test if lists of the models are createt correctly.
    """

    def __init__(self, ax, button_list, initial_line, logger):
        self.current_line = initial_line
        self.ax = ax
        self.button_list = button_list
        self.data_getter = VvsData(logger)
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

    
    def plot_avg_station_risk(self, new_line='no new line given'):
        """
        Plots the average risk per station using the data from the dataGetter.
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
            self.current_line = new_line        #Change the current line. Needed in every line specific ploting function.

        for btn in self.button_list:
            btn.set_visible(True)
        data = self.data_getter.get_avg_station_risk(self.current_line)
        station_and_risk = [(obj.station, obj.risk) for obj in data]
        station_risk_dict = {}
        for station, risk in station_and_risk:
            if station in station_risk_dict:
                station_risk_dict[station].append(risk)
            else:
                station_risk_dict[station] = [risk]
        station_and_avg_risk = []
        for station, risk in station_risk_dict.items():
            avg_risk = sum(risk) / len(risk)
            station_and_avg_risk.append((station, avg_risk))
        station_and_avg_risk.sort(key=lambda x: x[1], reverse=True)
        x = [station_id for station_id, _ in station_and_avg_risk]
        for station in station_and_avg_risk:
            print(station)
        y = [avg_delay for _, avg_delay in station_and_avg_risk]
        self.ax.bar(x, y)
        self.ax.set_title("Durchschnittliches Verspätungsrisiko")
        self.ax.set_xlabel("Station")
        self.ax.set_ylabel("Risiko in %")
        self.ax.figure.canvas.draw()
        self.logger.info('Ploted station risk data')



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
        self.ax.tick_params(axis='x', rotation=90)

        self.ax.figure.canvas.draw()
        self.logger.info('Ploted time delay data')



class Swapper:

    """
    Swap between different Graphs.

    Args:
        Args:
        *ax: graph to plot in
        *button_list: buttons to switch lines
        *initial_line: line to plot first
        *logger: logger
    
    Tests:
        *Test if data is printable into ax
        *Test if functions are always called with the right args.
    """
    
    def __init__(self, ax, button_list, initial_line, logger) -> None:
        """
    Initializes the instance with a provided matplotlib axes and a Plotter object.

    Args:
        ax (matplotlib.axes.Axes): The matplotlib axes used for plotting.


    Side Effects:
        * Sets the 'ax' attribute to the provided matplotlib axes.

    Tests:
        * Test that the function initializes the attributes correctly.
        * Test that the 'plots' list is populated with callable methods from the Plotter object.
        * Test that the 'func_pointer' attribute is set to the length of the 'plots' list.
    """
        self.ax = ax
        self.func_pointer = 0
        self.plots = []
        self.plotter = Plotter(self.ax, button_list, initial_line, logger)

        for attr_name in dir(self.plotter):
            attr = getattr(self.plotter, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                self.plots.append(attr)
        self.func_pointer = len(self.plots)


    def call_left_func(self):
        """
        Calls the function to the left of the current 'func_pointer' in the 'plots' list.

        Tests:
            * Test that the function updates the 'func_pointer' attribute correctly when not at the beginning of the list.
            * Test that the function wraps around to the end of the list when the 'func_pointer' is at the beginning.
            * Test that the function at the updated 'func_pointer' index is called.
        """
        if self.func_pointer == 0:
            self.func_pointer = len(self.plots)-1
        else:
            self.func_pointer -= 1

        self.plots[self.func_pointer]()


    def call_right_func(self):
        """
        Calls the function to the right of the current 'func_pointer' in the 'plots' list.

        Tests:
            * Test that the function updates the 'func_pointer' attribute correctly when not at the end of the list.
            * Test that the function wraps around to the beginning of the list when the 'func_pointer' is at tend.
            * Test that the function at the updated 'func_pointer' index is called.
        """
        if self.func_pointer == len(self.plots)-1:
            self.func_pointer = 0
        else:
            self.func_pointer += 1

        self.plots[self.func_pointer]()

    def switch_line(self, new_line):
        self.plots[self.func_pointer](new_line)