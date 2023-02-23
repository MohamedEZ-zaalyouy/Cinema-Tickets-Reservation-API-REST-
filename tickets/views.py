from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Movie, Guest, Reservation

# Create your views here.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #1 without REST and No model Query => FBV
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def no_rest_no_model(request):
    guests = [
        {
            'id':1,
            'name':"Mohamed",
            'mobile': 21261234567
        },
        {
            'id':2,
            'name':"Ali",
            'mobile': 21267654321
        }
    ]

    return JsonResponse(guests , safe=False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #2 Model data default django without REST.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def no_rest_from_model(request):
    
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name','mobile'))
    }

    return JsonResponse(response)