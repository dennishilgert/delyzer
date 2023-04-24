from rest_framework import serializers
from .models import Departure

class DepartureSerializer(serializers.ModelSerializer):
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
