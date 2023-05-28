import datetime
from .models import Departure
from .serializers import DepartureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import pandas as pd
import logging

from .utils.filter import Filter

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
            lines_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'line_name'))

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
            
            stations_df_unique = Filter.join_station_name(stations_df_unique)

            stations_df_sub = pd.DataFrame(stations_df_sub['Name mit Ort'])

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

            delay_df = Filter.by_delay(delay_df)
            
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
            
            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.by_delay(delay_df)

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
            
            delay_df = Filter.by_time(delay_df)

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

            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.by_time(delay_df)

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

            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.delay_at_station(delay_df)

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

            delay_df = Filter.delay_at_station(delay_df)
            

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

            delay_df = Filter.propability_at_station(delay_df)

            delay_df = delay_df.loc[delay_df['Name mit Ort'] == station]
            
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

            delay_df = Filter.propability_at_station(delay_df)

            delay_dic = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dic})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def propability_of_line(request, line, direction):

    """propability_of_line
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
            'delay'))

            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.propability_of_line(delay_df)

            if delay_df.empty:
                return Response(status=status.HTTP_404_NOT_FOUND)

            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def propability_of_lines(request):

    """propability_of_lines
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
            'delay'))

            delay_df = Filter.propability_of_line(delay_df)

            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def propability_at_stations_of_line(request, line, direction):

    """propability_of_lines
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

            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.propability_at_station(delay_df)

            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.info(e)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)