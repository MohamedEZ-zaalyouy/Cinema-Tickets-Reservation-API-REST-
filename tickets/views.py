from django.shortcuts import render
from django.http.response import JsonResponse , Response
from .models import Movie, Guest, Reservation
from rest_framework.decorators import api_view



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


# List == GET 
# Create == POST
# pk query == PUT
# Delete destroy == DELETE

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3 - Function based views
# 3.1 GET & POST 
#~~~~~~~~~~~~~~~
@api_view(['GET','POST'])
def f_f_f(request):
    pass
    # GET


    # POST



# 3.2 GET PUT DELETE 
#~~~~~~~~~~~~~~~~~~~
@api_view(['GET','PUT','DELETE'])
def f_f_f(request):
    pass


 