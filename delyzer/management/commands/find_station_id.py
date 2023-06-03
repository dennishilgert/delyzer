# Dennis Hilgert

from django.core.management.base import BaseCommand, CommandParser
import logging, pandas as pd

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Find a station id by the name of the station'



    def add_arguments(self, parser: CommandParser) -> None:
        """
        Adds the allowed arguments for the find station id command

        Args:
            parser (CommandParser): Django command parser
        """

        parser.add_argument(
            '--station-name',
            help='Name of the station to receive the station id from',
            required=True
        )



    def handle(self, *args, **options) -> None:
        """
        Handles the execution of the find station id command.

        Tests:
            * Provide an invalid station name: Command should show a message that there is no station with the given name
            * Provide a valid station name: Command should show a data frame of the results
        """

        station_name = options.get('station_name')
        stations_df = pd.read_csv('vvs_data.csv')
        stations_result = stations_df.loc[stations_df['Name mit Ort'].str.contains(station_name)]
        if stations_result.empty:
            logger.info(f'Es existiert keine Station mit dem Namen "{station_name}".')
            return

        logger.info(f'Folgende Stationen enthalten den Namen "{station_name}":')
        print(stations_result[['Nummer', 'Name mit Ort']])