from django.core.management.base import BaseCommand, CommandParser
from vvspy import get_departures
from delyzer.serializers import DepartureSerializer
from datetime import datetime
import sched, time

class Command(BaseCommand):
  help = 'Start collecting data of a given station in an intervall'



  def __init__(self) -> None:
    self.station_id = ''
    self.limit = 20
    self.scheduler = sched.scheduler(time.time, time.sleep)
    self.intervall = 20



  def add_arguments(self, parser: CommandParser) -> None:
    parser.add_argument(
      '--station-id',
      default=self.station_id,
      help='ID of the station to collect departure data'
    )
    parser.add_argument(
      '--limit',
      default=self.limit,
      help='Limit of the entries per collection call'
    )



  def handle(self, *args, **options) -> None:
    self.station_id = options.get('station_id')
    self.limit = options.get('limit')

    try:
      self.event = self.scheduler.enter(0, 1, self.fetch_data, (self.scheduler,))
      self.scheduler.run()
    except KeyboardInterrupt:
      print('Data collection has been stopped')



  def fetch_data(self, scheduler: sched.scheduler) -> None:
    print('Data collection: Running fetch')

    self.current_scheduler_event = scheduler.enter(self.intervall, 1, self.fetch_data, (scheduler,))

    departures = get_departures(self.station_id, limit=self.limit)
    print('Data collection: Mapping fetched data')
    for departure in departures:
      if departure.serving_line.real_time == False:
        continue
      
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

      serializer = DepartureSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        print('Data collection: Data saved')
      else:
        print('Data not valid')
        print(data)
        print()