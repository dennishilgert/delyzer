from django.core.management.base import BaseCommand, CommandParser
from vvspy import get_departures
from delyzer.models import Departure
from delyzer.serializers import DepartureSerializer
from datetime import datetime
import sched, time, logging, pandas as pd

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Start collecting data of a given station in an time intervall'


    def __init__(self) -> None:
        self.observe_line: str = ''
        self.station_ids: list

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.intervall = 12



    def add_arguments(self, parser: CommandParser) -> None:
        """
        Adds the allowed arguments for the data collection command

        Args:
            parser (CommandParser): Django command parser
        """

        parser.add_argument(
            '--observe-station',
            help='Observe and collect departure data of the given station id',
            required=False
        )
        parser.add_argument(
            '--observe-line',
            help='Observe and collect departure data from all stations of the given line',
            required=False
        )
        parser.add_argument(
            '--clear',
            default=False,
            help='Clear database before collecting new data',
            required=False
        )



    def handle(self, *args, **options) -> None:
        """
        Handles the execution of the data collection command. This means:

        * Set the arguments given with the command execution to the local variables
        * Start the scheduler to collect data of the departures in the specified time intervall
        * Stop the scheduler on keyboard interrupt or program exit

        Tests:
            * Provide invalid parameters: Command should not be executed - instead show help
            * Provide not enough parameters (wether observe-line and observe-station): Program should exit with a hint
            * Provide matching parameters: Program should run until it is terminated
        """

        observe_line = options.get('observe_line')
        if observe_line:
            self.observe_line = observe_line
            station_ids = self.get_stations(observe_line)
            if not station_ids:
                logger.error('Please provide a valid line number')
                return
            self.station_ids = station_ids
        
        observe_station = options.get('observe_station')
        if observe_station:
            station_valid = self.validate_station_id(observe_station)
            if not station_valid:
                logger.error('Please provide a valid station id')
                return
            self.station_ids = [observe_station]

        if not self.station_ids:
            logger.error('Please provide a line or specific station id')
            return

        clear = options.get('clear')
        if clear:
            Departure.objects.all().delete()

        logger.info('Data collection has been started')
        logger.info(f'Clear: ' + clear)
        logger.info('Observe line: -' if not observe_line else 'Observe line: ' + observe_line)
        logger.info('Observe station: -' if not observe_station else 'Observe station: ' + observe_station)

        try:
            self.event = self.scheduler.enter(0, 1, self.fetch_data, (self.scheduler,))
            self.scheduler.run()
        except KeyboardInterrupt:
            logger.info('Data collection has been stopped')



    def get_stations(self, line: str) -> list:
        """
        Returns a data frame with all stops of the line. This means:

        * Load the csv file which contains all information regarding the lines and stations
        * Filter all stations by the given line and return the data

        Args:
            line (str): Line to get the stations from

        Returns:
            pd.DataFrame: DataFrame with the stations of the given line

        Tests:
            * Pass in a inexistent line: Function should return an empty list
            * Pass in a valid line: Function should return filled list
        """

        # Load the file in cp1252 encoding because it contains umlauts
        line_stations_df = pd.read_csv('vvs_haltestellen.csv', sep=';', encoding='cp1252')
        # Filter stations by given line
        stations = line_stations_df.loc[line_stations_df['Linien (EFA)'].str.match(line)]
        # Convert all station numbers into the format that is needed for the api requests
        stations['Nummer (API)'] = stations['Nummer'].apply(lambda nummer: 5000000 + nummer)
        return stations['Nummer (API)'].tolist()
    

    def validate_station_id(self, station_id: str) -> bool:
        """
        Checks if a given station id is existent

        Args:
            station_id (str): Id of the station

        Returns:
            bool: Wether the station id exists or not

        Tests:
            * Pass in an inexistent station id: Function should return false
            * Pass in an existent station id: Function should return true
        """
        stations_df = pd.read_csv('vvs_data.csv')
        station = stations_df.loc[stations_df['Nummer'].astype(str).str.match(station_id)]
        print(station)
        return station['Nummer'].tolist().__len__() > 0



    def fetch_data(self, scheduler: sched.scheduler) -> None:
        """
        Fetchs data from the vvs api for the given stations in the specified time intervall. This means:

        * Iterate through all station ids and request the departure information for each station id
        * Iterate through all departures and check if the data is in real time and if the departure belongs to the observed line if set
        * Map the data to the fields needed for serialization
        * Save the data to the database

        Args:
            scheduler (sched.scheduler): Scheduler

        Tests:
            * On observe-station - provide an invalid station-id: Function should 
            * Set the station_ids
        """

        logger.debug('Data collection: Running fetch')
        self.current_scheduler_event = scheduler.enter(self.intervall, 1, self.fetch_data, (scheduler,))

        for station_id in self.station_ids:
            departures = get_departures(station_id, limit=100)
            logger.debug('Data collection: Mapping fetched data')
            for departure in departures:
                # If departure is not in real time skip this entry
                if departure.serving_line.real_time == False:
                    continue
                # If departure does not belong to the observed line skip this entry
                if self.observe_line and not departure.serving_line.number == self.observe_line:
                    continue
                # Map the data of the departure to the data fields to be saved
                data = self.map_data(departure)
                # Check if the data matches the required types and save it to the database
                self.serialize_data(data)



    def map_data(self, departure) -> dict:
        """
        Maps the given data to the fields needed for serialization

        Args:
            departure (_type_): Departure object from the vvs api

        Returns:
            dict: Object with all data needed for the serialization

        Tests:
            * Pass in a departure that doesn't have the required fields: Function should throw an error
            * Pass in a departure that satisfies the required fields: Function should return the mapped object
        """
        data = {}
        data['station_id'] = departure.stop_id
        data['destination_id'] = departure.serving_line.dest_id
        data['direction'] = departure.serving_line.direction
        data['direction_from'] = departure.serving_line.direction_from
        data['line_number'] = departure.serving_line.number
        data['line_name'] = departure.serving_line.name
        data['planned_departure_time'] = departure.datetime.time()
        data['delay'] = 0 if departure.serving_line.delay == None else departure.serving_line.delay
        data['current_date'] = datetime.now()
        return data



    def serialize_data(self, data: dict) -> None:
        """
        Checks if the data has all required fields to save to the database

        Args:
            data (dict): Data to be serialized

        Tests:
            * Pass in data that doesn't have the required fields: Function should throw an error
            * Pass in data that does have all required fields: Function should save the data to the database
        """
        serializer = DepartureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            logger.warn('Data does not satisfy the departure serializer')
            logger.warn(data)
