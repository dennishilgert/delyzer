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
            departures_data = Departure.objects.all()
            serializer = DepartureSerializer(departures_data, many=True)
            return JsonResponse({'departures':serializer.data})
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def departure_detail(request, id: int):

    """departure_detail
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
            departure_data = Departure.objects.get(pk=id)

            serializer = DepartureSerializer(departure_data)
            return JsonResponse(serializer.data)
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def lines(request):

    """lines
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
            lines_data = Departure.objects.values('line_number',
            'id',
            'direction',
            'line_name')

            lines_df = pd.DataFrame(lines_data)

            lines_df = lines_df.drop_duplicates(subset=['line_number','direction'])
            lines_df = lines_df.sort_values(['line_number','direction'])

            lines_df_selection = lines_df[['line_number','direction']]
            
            lines_dict = lines_df_selection.to_dict('records')
            
            return JsonResponse({'lines':lines_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def stations(request):

    """stations
    description:
        * GET: returns a list of all stations

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns a list of lines.
        * Test that the API returns the correct number of lines.
        * Test that the API returns the expected data for each line.
    """
    
    if request.method == 'GET':
        try:
            stations_df = pd.DataFrame(Departure.objects.values('station_id'))

            stations_df_unique = stations_df.drop_duplicates(subset='station_id')
            stations_df_unique = stations_df_unique.reset_index(drop = True)
            
            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            stations_df_unique = stations_df_unique.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            stations_df_sub = stations_df_unique['Name mit Ort']

            stations_dict = stations_df_sub.to_dict()

            return JsonResponse({'stations':stations_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lines_by_delay(request):

    """lines_by_delay
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
            delay_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'delay',
            'line_name'))

            delay_df = delay_df.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay_df = delay_df.sort_values('delay', ascending=False)
            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

api_view(['GET'])
def line_by_delay(request, line, direction):

    """lines_by_delay
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
            delay_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'delay',
            'line_name'))
            
            delay_df = pd.DataFrame(delay_df.loc[delay_df['line_number'] == line])
            delay_df = pd.DataFrame(delay_df.loc[delay_df['direction'] == direction])

            delay_df = delay_df.groupby(['line_number','direction'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay_df = delay_df.sort_values('delay', ascending=False)

            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def delay_at_time(request):

    """delay_at_time
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
            delay_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'delay',
            'line_name',
            'planned_departure_time'))
            
            delay_df['planned_departure_time'] = delay_df['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
            delay_df.set_index('planned_departure_time', inplace=True)

            delay_df = delay_df['delay'].resample('30min').mean().round(2).reset_index().ffill()
            
            delay_df.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

            delay_dict = delay_df.to_dict('records')
            
            return JsonResponse({'times':[delay_dict]})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def line_delay_at_time(request, line, direction):

    """delay_at_time
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
            delay_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'delay',
            'line_name',
            'planned_departure_time'))
            
            delay_df = pd.DataFrame(delay_df.loc[delay_df['line_number'] == line])
            delay_df = pd.DataFrame(delay_df.loc[delay_df['direction'] == direction])

            delay_df['planned_departure_time'] = delay_df['planned_departure_time'].apply(lambda x: datetime.datetime.combine(datetime.datetime.today(), x))
            delay_df.set_index('planned_departure_time', inplace=True)

            delay_df = delay_df['delay'].resample('30min').mean().round(2).reset_index().ffill()
            
            delay_df.rename(columns={'planned_departure_time':'timeslot_start'}, inplace=True)

            delay_dict = delay_df.to_dict('records')
            
            return JsonResponse({'times':[delay_dict]})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


    
@api_view(['GET'])
def line_delay_at_station(request, line, direction):

    """delay_at_station
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
            'line_number',
            'direction',
            'station_id',
            'delay'))

            delay_df = pd.DataFrame(delay_df.loc[delay_df['line_number'] == line])
            delay_df = pd.DataFrame(delay_df.loc[delay_df['direction'] == direction])

            delay_df = delay_df.groupby(['station_id'], as_index=False).agg({'delay': 'mean'}).round(2)
            delay_df = delay_df.sort_values('delay', ascending=False)

            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            delay_df = delay_df[['Name mit Ort', 'delay']]

            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def delay_at_station(request):

    """delay_at_station
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
            delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            delay_df = delay_df[['Name mit Ort', 'delay']]
            

            delay_dic = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dic})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def propability_at_station(request, station: str):

    """propability_at_station
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

            delay_df = pd.DataFrame(delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2))

            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            delay_df = delay_df.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            delay_df = delay_df.loc[delay_df['Name mit Ort'] == station, ['Name mit Ort', 'delay']]
            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def propability_at_stations(request):

    """propability_at_stations
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

            delay_series = delay_df.groupby(['station_id'], as_index=False)['delay'].apply(lambda delay: ((delay>2).sum()/len(delay))*100).round(2)
            delay_series = delay_series.sort_values('delay', ascending=False)

            stations_info_df = pd.read_csv('vvs_data.csv', sep=',', encoding='utf-8')
            delay_series = delay_series.join(stations_info_df.set_index('Nummer'), on='station_id', how="left")

            delay_series = delay_series[['Name mit Ort', 'delay']]

            delay_dic = delay_series.to_dict('records')

            return JsonResponse({'propability':delay_dic})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)