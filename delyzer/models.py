from django.db import models

class Departure(models.Model):
  line_number = models.CharField(max_length=5)
  line_name = models.CharField(max_length=40)
  planned_departure = models.DateTimeField()
  real_departure = models.DateTimeField()
  delay = models.IntegerField()

  def __str__(self):
    return self.line_number