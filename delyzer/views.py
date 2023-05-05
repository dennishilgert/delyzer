import datetime
import json
from .models import Departure
from .serializers import DepartureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import pandas as pd


@api_view(['GET'])
def departure_list(request):

    """departure_list
    description:
        * GET: returns a list of all departures

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns a list of departures.
        * Test that the API returns the correct number of departures.
        * Test that the API returns the expected data for each departure.
    """

    if request.method == 'GET':
        departures = Departure.objects.all()
        serializer = DepartureSerializer(departures, many=True)
        return JsonResponse({'departures':serializer.data})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def departure_detail(request, id: int):

    """departure_list
    description:
        * GET: returns a departures by its id

    Args:
            id (number): Departure_ID

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns the correct departure for a given ID.
        * Test that the API returns a 404 error if the ID doesn't exist.
        * Test that the API returns the expected data for the departure.
    """
    
    if request.method == 'GET':
        departure = Departure.objects.get(pk=id)

        serializer = DepartureSerializer(departure)
        return JsonResponse(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def lines(request):

    """departure_list
    description:
        * GET: returns a list of all lines

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns a list of lines.
        * Test that the API returns the correct number of lines.
        * Test that the API returns the expected data for each line.
    """
    
    if request.method == 'GET':
        lines = pd.DataFrame(Departure.objects.values('line_number',
       'id',
      'direction',
      'line_name'))
        lines = lines.drop_duplicates(subset=['line_number','direction'])
        lines = lines.sort_values(['line_number','direction'])
        lines = lines[['line_number','direction']]
        print(lines)
        lines = lines.to_dict('records')
        print(type(lines))


        print(lines)
        return JsonResponse({'lines':lines})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lines_by_delay(request):

    """departure_list
    description:
        * GET: returns a list of all delays of trains

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns a list of lines.
        * Test that the API returns the correct number of lines.
        * Test that the API returns the expected data for each line.
    """
    
    if request.method == 'GET':
        delay = pd.DataFrame(Departure.objects.values('line_number',
       'id',
      'direction',
      'delay',
      'line_name'))
        delay = delay.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(0)
        delay = delay.sort_values('delay', ascending=False)
        print(delay)
        delay = delay.to_dict('records')
        print(type(delay))


        print(delay)
        return JsonResponse({'delays':delay})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def delay_at_time(request):

    """departure_list
    description:
        * GET: returns a list of all delays of trains

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns a list of lines.
        * Test that the API returns the correct number of lines.
        * Test that the API returns the expected data for each line.
    """
    
    if request.method == 'GET':
        delay = pd.DataFrame(Departure.objects.values('line_number',
       'id',
      'direction',
      'delay',
      'line_name',
      'planned_departure_time'))
        delay['planned_departure_time'] = delay['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
        delay.set_index('planned_departure_time', inplace=True)
        delay = delay['delay'].resample('30min').mean().round(2).reset_index().ffill()
        print(delay)
        delay['delay'] = delay['delay']
        delay.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

        delay = delay.to_dict('records')
        

        print(delay)
        return JsonResponse({'times':[delay]})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)