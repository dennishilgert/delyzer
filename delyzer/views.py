from .models import Departure
from .serializers import DepartureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status


@api_view('GET')
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

        

@api_view('GET')
def departure_detail(request, id: int):

    """departure_list
    description:
        * GET: returns a departures by its id

    Args:
            id (number): Departure _ID

    Returns:
        _type_: HttpResponse
    
    tests:
        * Test that the API returns the correct departure for a given ID.
        * Test that the API returns a 404 error if the ID doesn't exist.
        * Test that the API returns the expected data for the departure.
    """
    try:
        departure = Departure.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DepartureSerializer(departure)
        return JsonResponse(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
