from django.db import models
from django.utils import timezone

class Departure(models.Model):
  station_id = models.IntegerField(default=-1)
  destination_id = models.IntegerField(default=-1)
  direction = models.CharField(max_length=128, default='')
  direction_from = models.CharField(max_length=128, default='')
  line_number = models.CharField(max_length=8, default='')
  line_name = models.CharField(max_length=64, default='')
  planned_departure_time = models.TimeField(default=timezone.now)
  delay = models.IntegerField(default=0)
  current_date = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.line_number