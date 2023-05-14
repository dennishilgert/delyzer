import datetime
import json
from .models import Departure
from .serializers import DepartureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import pandas as pd
import logging


logger = logging.getLogger(__name__)

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
        try:
            departures = Departure.objects.all()
            serializer = DepartureSerializer(departures, many=True)
            return JsonResponse({'departures':serializer.data})
        except Exception as e:
            logger.info(e)
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
        try:
            departure = Departure.objects.get(pk=id)

            serializer = DepartureSerializer(departure)
            return JsonResponse(serializer.data)
        except Exception as e:
            logger.info(e)
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
        try:
            lines = pd.DataFrame(Departure.objects.values('line_number',
        'id',
        'direction',
        'line_name'))
            lines = lines.drop_duplicates(subset=['line_number','direction'])
            lines = lines.sort_values(['line_number','direction'])
            lines = lines[['line_number','direction']]
            logger.info(lines)
            lines = lines.to_dict('records')
            logger.info(type(lines))


            logger.info(lines)
            return JsonResponse({'lines':lines})
        except Exception as e:
            logger.info(e)
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
        try:
            delay = pd.DataFrame(Departure.objects.values('line_number',
        'id',
        'direction',
        'delay',
        'line_name'))
            delay = delay.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay = delay.sort_values('delay', ascending=False)
            logger.info(delay)
            delay = delay.to_dict('records')
            logger.info(type(delay))


            logger.info(delay)
            return JsonResponse({'delays':delay})
        except Exception as e:
            logger.info(e)
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
        try:
            delay = pd.DataFrame(Departure.objects.values('line_number',
        'id',
        'direction',
        'delay',
        'line_name',
        'planned_departure_time'))
            delay['planned_departure_time'] = delay['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
            delay.set_index('planned_departure_time', inplace=True)
            delay = delay['delay'].resample('30min').mean().round(2).reset_index().ffill()
            logger.info(delay)
            delay['delay'] = delay['delay']
            delay.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

            delay = delay.to_dict('records')
            

            logger.info(delay)
            return JsonResponse({'times':[delay]})
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def delay_at_station(request):

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
        try:
            delay = pd.DataFrame(Departure.objects.values('id',
            'station_id',
        'delay'))
            delay = delay.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay = delay.sort_values('delay', ascending=False)
            logger.info(delay)
            delay = delay.to_dict('records')
            logger.info(type(delay))

            logger.info(delay)
            return JsonResponse({'delays':delay})
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def delay_at_station(request):

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
        try:
            delay_df = pd.DataFrame(Departure.objects.values('id',
            'station_id',
            'delay'))
            delay_df = delay_df.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay_df = delay_df.sort_values('delay', ascending=False)

            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            print(stations_info_df)
            delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")
            delay_df = delay_df[['Name mit Ort', 'delay']]
            delay_df
            print(delay_df)
            delay_dic = delay_df.to_dict('records')
            logger.info(type(delay_dic))


            logger.info(delay_dic)
            return JsonResponse({'delays':delay_dic})
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def propability_at_station(request):

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
        try:
            delay_df = pd.DataFrame(Departure.objects.values('id',
            'station_id',
            'delay'))

            delay_df = delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
            delay_df = delay_df.sort_values('delay', ascending=False)

            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            delay_df = delay_df[['Name mit Ort', 'delay']]
            delay_df
            print(delay_df)
            delay_dic = delay_df.to_dict('records')
            logger.info(type(delay_dic))


            logger.info(delay_dic)
            return JsonResponse({'delays':delay_dic})
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)