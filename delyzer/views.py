from .models import Departure
from .serializers import DepartureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def departure_list(request):
  if request.method == 'GET':
    departures = Departure.objects.all()
    serializer = DepartureSerializer(departures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def departure_detail(request, id):
  try:
    departure = Departure.objects.get(pk=id)
  except Departure.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = DepartureSerializer(departure)
    return Response(serializer.data)