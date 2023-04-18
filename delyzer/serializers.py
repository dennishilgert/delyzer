from rest_framework import serializers
from .models import Departure

class DepartureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Departure
    fields = ['id', 'line_number', 'line_name', 'planned_departure', 'real_departure', 'delay']