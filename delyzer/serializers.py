from rest_framework import serializers
from .models import Departure

class DepartureSerializer(serializers.ModelSerializer):
  """
  Serializer to check if given data satisfies the required fields to save it to the database
  """

  class Meta:
    model = Departure
    fields = [
      'id',
      'station_id',
      'destination_id',
      'direction',
      'direction_from',
      'line_number',
      'line_name',
      'planned_departure_time',
      'delay',
      'current_date'
    ]
