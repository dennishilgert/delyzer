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
        * GET: returns a list of all departures in the database

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call

    Example:
        ```
        {
        "departures": [
            {
                "id": 53969,
                "station_id": 5001800,
                "destination_id": 5004512,
                "direction": "Herrenberg",
                "direction_from": "Kirchheim (T)",
                "line_number": "S1",
                "line_name": "S-Bahn",
                "planned_departure_time": "11:40:00",
                "delay": 1,
                "current_date": "2023-05-15T11:01:35.190999+02:00"
            },
            {
                "id": 53970,
                "station_id": 5001800,
                "destination_id": 5004211,
                "direction": "Kirchheim (T)",
                "direction_from": "Herrenberg",
                "line_number": "S1",
                "line_name": "S-Bahn",
                "planned_departure_time": "11:49:00",
                "delay": 1,
                "current_date": "2023-05-15T11:01:35.196941+02:00"
            },
            ...
        ]}
        ```
    
    tests:
        * Test that the API returns a list of departures.
        * Test that the API returns the correct departure data.
        * Test that the API returns 500 when there are any DB Problems
    """

    if request.method == 'GET':
        try:
            logger.info("request for departure_list")

            departures_data = Departure.objects.all()
            serializer = DepartureSerializer(departures_data, many=True)
            return JsonResponse({'departures':serializer.data})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def departure_detail(request, id: int):

    """departure_detail
    description:
        * GET: returns departure details by its id

    Args:
        request (Request): Information about the call
        id (number): Departure_ID

    Returns:
        _type_: HttpResponse
    
    Example:
        ```
        {
        "departure": 
            {
                "id": 53969,
                "station_id": 5001800,
                "destination_id": 5004512,
                "direction": "Herrenberg",
                "direction_from": "Kirchheim (T)",
                "line_number": "S1",
                "line_name": "S-Bahn",
                "planned_departure_time": "11:40:00",
                "delay": 1,
                "current_date": "2023-05-15T11:01:35.190999+02:00"
            }
        
        ```
        
    tests:
        * Test that the API returns the correct departure for a given ID.
        * Test that the API returns a 404 error if the ID doesn't exist.
        * Test that the API returns 500 when there are any DB Problems
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for departure_detail")

            departure_data = Departure.objects.get(pk=id)

            serializer = DepartureSerializer(departure_data)
            return JsonResponse({'departure':serializer.data})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def lines(request):

    """lines
    description:
        * GET: returns a list of all lines that are currently in the Database

    Returns:
        _type_: HttpResponse
    
    Args:
        request (Request): Information about the call

    Example:
        ```
            {
            "lines": [
                {
                    "line_number": "S1",
                    "direction": "Herrenberg"
                },
                {
                    "line_number": "S1",
                    "direction": "Kirchheim (T)"
                },
                ...
            ]}
        ```

    tests:
        * Test that the API returns the right lines
        * Test that the API returns 404 at any request other than GET
        * Test that the API returns 500 when there are any DB Problems
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for lines")

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
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def stations(request):
    """stations
    description:
        * GET: returns a list of all stations

    Returns:
        _type_: HttpResponse
    
    Args:
        request (Request): Information about the call

    Example:
        ```
            {
                "stations": {
                    "Name mit Ort": {
                        "5001800": "Altbach",
                        "5001801": "Mettingen",
                        ...
                    }
                }
            }
        ```
        
    tests:
        * Test that the API returns a list of stations.
        * Test that the API returns 404 at any request other than GET
        * Test that the API returns 500 when there are any DB Problems
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for stations")
            stations_df = pd.DataFrame(Departure.objects.values('station_id'))

            stations_df_unique = stations_df.drop_duplicates(subset='station_id')
            stations_df_unique = stations_df_unique.reset_index(drop = True)
            
            stations_df_unique = Filter.join_station_name(stations_df_unique)

            stations_df_sub = pd.DataFrame(stations_df_unique['Name mit Ort'])

            stations_dict = stations_df_sub.to_dict()


            return JsonResponse({'stations':stations_dict})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lines_by_delay(request):
    """lines_by_delay
    description:
        * GET: returns a list of all trains with their average delays

    Returns:
        _type_: HttpResponse
    
    Args:
        request (Request): Information about the call

    Example:
        ```
            {
                "delays": [
                    {
                        "line_number": "S1",
                        "direction": "Herrenberg",
                        "delay": 0.11
                    },
                    {
                        "line_number": "S1",
                        "direction": "Kirchheim (T)",
                        "delay": 0.11
                    },
                    ...
                ]
            }
        ```

    tests:
        * Test that the API returns a list of stations.
        * Test that the API returns 404 at any request other than GET
        * Test that the API returns 500 when there are any DB Problems
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for lines_by_delay")

            delay_df = pd.DataFrame(Departure.objects.values('line_number',
            'id',
            'direction',
            'delay',
            'line_name'))

            delay_df = Filter.by_delay(delay_df)
            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dict})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

api_view(['GET'])
def line_by_delay(request, line, direction):

    """line_by_delay
    description:
        * GET: returns a train by its id with its average delay

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call
        line (string): Line name
        direction (string): Direction name    

    Example:
        ```
            {
                "delays": [
                    {
                        "line_number": "S1",
                        "direction": "Herrenberg",
                        "delay": 0.11
                    }
                ]
            }
        ```    

    tests:
        * Test that the API returns the line with the given id and direction.
        * Test that the API returns an empty list if the line or direction doesn't exist.
        * Test that the API returns 404 at any request other than GET
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for line_by_delay")

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
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def delay_at_time(request):

    """delay_at_time
    description:
        * GET: returns a list of the average delay of all trains orderd by time

    Returns:
        _type_: HttpResponse
    
    Args:
        request (Request): Information about the call

    Example:
        ```    
            {
                "times": [
                    [
                        {
                            "timeslot_start": "2023-05-28T00:00:00",
                            "delay": 0.0
                        },
                        {
                            "timeslot_start": "2023-05-28T00:30:00",
                            "delay": 0.0
                        },
                        ...
                    ]
                ]
            }
        ```    

    tests:
        * Test that the API returns a list of times.
        * Test that the API returns 24 times in half hour steps.
        * Test that the API returns 404 at any request other than GET
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for delay_at_time")

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
            logger.error(e)        
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def line_delay_at_time(request, line, direction):

    """line_delay_at_time
    description:
        * GET: returns a list of the average delay of one train by its line and direction orderd by time

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call
        line (string): Line name
        direction (string): Direction name    

    Example:
        ```    
            {
                "times": [
                    [
                        {
                            "timeslot_start": "2023-05-28T00:00:00",
                            "delay": 0.0
                        }
                    ]
                ]
            }
        ```    

    tests:
        * Test that the API returns a list of times.
        * Test that the API returns 24 times in half hour steps.
        * Test that the API returns 404 at any request other than GET
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for line_delay_at_time")

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
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


    
@api_view(['GET'])
def line_delay_at_station(request, line, direction):

    """line_delay_at_station
    description:
        * GET: returns a list of the delay from a train by its line and direction ordered by stations 

    Returns:
        _type_: HttpResponse
        
    Args:
        request (Request): Information about the call
        line (string): Line name
        direction (string): Direction name    

    Example:
        ```    
            {
                "delays": [
                    {
                        "Name mit Ort": "Stadtmitte",
                        "delay": 0.93
                    },
                    {
                        "Name mit Ort": "Böblingen",
                        "delay": 0.64
                    },
                    ...
                ]
            }
        ```    

    tests:
        * Test that the API returns a list of stations with delays.
        * Test that the API returns all stations of the given line.
        * Test that the API returns all stations ordered by delays.
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for line_delay_at_station")

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
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def delay_at_station(request):

    """delay_at_station
    description:
        * GET: returns a list of the delay from all trains ordered by stations 

    Returns:
        _type_: HttpResponse
        
    Args:
        request (Request): Information about the call

    Example:
        ```    
            {
                "delays": [
                    {
                        "Name mit Ort": "Stadtmitte",
                        "delay": 1.93
                    },
                    {
                        "Name mit Ort": "Böblingen",
                        "delay": 2.64
                    },
                    ...
                ]
            }
        ```    

    tests:
        * Test that the API returns a list of stations with delays.
        * Test that the API returns all stations (like the stations request)
        * Test that the API returns all stations ordered by delays.
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for delay_at_station")

            delay_df = pd.DataFrame(Departure.objects.values('id',
            'station_id',
            'delay'))

            delay_df = Filter.delay_at_station(delay_df)
            

            delay_dic = delay_df.to_dict('records')

            return JsonResponse({'delays':delay_dic})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def propability_at_station(request, station: str):

    """propability_at_station
    description:
        * GET: returns the propability of a delay at a specific station 

    Returns:
        _type_: HttpResponse
        
    Args:
        request (Request): Information about the call
        station (string): Station name

    Example:
        ```    
            {
                "propability": [
                    {
                        "Name mit Ort": "Stadtmitte",
                        "delay": 0.0
                    }
                ]
            }
        ```    

    tests:
        * Test that the API returns a the right station with its delay propability.
        * Test that the API returns the correct propability in % for the station.
        * Test that the API returns an empty list if the station is not found.
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for propability_at_station")

            delay_df = pd.DataFrame(Departure.objects.values('id',
            'station_id',
            'delay'))

            delay_df = Filter.propability_at_station(delay_df)

            delay_df = delay_df.loc[delay_df['Name mit Ort'] == station]
            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def propability_at_stations(request):

    """propability_at_stations
    description:
        * GET: returns the propability of a delay at all stations

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call

    Example:
        ```    
            {
                "propability": [
                    {
                        "Name mit Ort": "Stadtmitte",
                        "delay": 1.0
                    },
                    {
                        "Name mit Ort": "Böblingen",
                        "delay": 0.0
                    },
                    ...
                ]
            }
        ```    

    tests:
        * Test that the API returns stations with its delay propability.
        * Test that the API returns the correct propability in % for the stations.
        * Test that the API returns all stations from the database by its delay propability.
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for propability_at_stations")

            delay_df = pd.DataFrame(Departure.objects.values('id',
            'station_id',
            'delay'))

            delay_df = Filter.propability_at_station(delay_df)

            delay_dic = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dic})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def propability_of_line(request, line, direction):

    """propability_of_line
    description:
        * GET: returns the delay propability of a specific line by its direction

    Returns:
        _type_: HttpResponse
        
    Args:
        request (Request): Information about the call
        line (string): Line name
        direction (string): Direction name  

    Example:
        ```    
            {
                "propability": [
                    {
                        "line_number": "S1",
                        "direction": "Herrenberg",
                        "delay": 1.0
                    },
                ]
            }
        ```    

    tests:
        * Test that the API returns the specified line with its average delay propability.
        * Test that the API returns the correct propability in % for the line.
        * Test that the API returns an empty list if there is no line with the given number and direction
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for propability_of_line")

            delay_df = pd.DataFrame(Departure.objects.values('id',
            'line_number',
            'direction',
            'delay'))

            delay_df = Filter.by_line(delay_df, line, direction)

            delay_df = Filter.propability_of_line(delay_df)

            delay_dict = delay_df.to_dict('records')
            
            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def propability_of_lines(request):

    """propability_of_lines
    description:
        * GET: returns the delay propability of all lines by its direction

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call

    Example:
        ```    
            {
                "propability": [
                    {
                        "line_number": "S1",
                        "direction": "Herrenberg",
                        "delay": 1.0
                    },
                    {
                        "line_number": "S1",
                        "direction": "Kirchheim (T)",
                        "delay": 1.2
                    },
                    ...
                ]
            }
        ```    

    tests:
        * Test that the API returns the lines with its average delay propability.
        * Test that the API returns the correct propability in % for the lines.
        * Test that the API returns an empty list if there is no line in the database.
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for propability_of_lines")

            delay_df = pd.DataFrame(Departure.objects.values('id',
            'line_number',
            'direction',
            'delay'))

            delay_df = Filter.propability_of_line(delay_df)

            
            delay_dict = delay_df.to_dict('records')

            return JsonResponse({'propability':delay_dict})
        
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def propability_at_stations_of_line(request, line, direction):

    """propability_of_lines
    description:
        * GET: returns the delay propability of all lines by its direction

    Returns:
        _type_: HttpResponse

    Args:
        request (Request): Information about the call
        line (string): Line name
        direction (string): Direction name  

    Example:
        ```    
            {
                "propability": [
                    {
                        "Name mit Ort": "Gärtringen",
                        "delay": 1.36
                    },
                    {
                        "Name mit Ort": "Wernau (N)",
                        "delay": 0.56
                    },
                    ...
                ]
            }
        ```    

    tests:
        * Test that the API returns the specified line with its average delay propability ordered by stations.
        * Test that the API returns the correct propability in % for the line.
        * Test that the API returns an empty list if there is no line with the given number and direction
        (* Test that the API returns 404 at any request other than GET)
    """
    
    if request.method == 'GET':
        try:
            logger.info("request for propability_at_stations_of_line")

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
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)