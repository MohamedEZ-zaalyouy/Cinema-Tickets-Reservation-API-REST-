from django.shortcuts import render
from django.http.response import JsonResponse 
from django.http import response
from .models import Movie, Guest, Reservation
from rest_framework.decorators import api_view 
from rest_framework import status, filters
from rest_framework.response import Response
from .serializers import MovieSerializer, GuestSerializer, ReservationSerializer



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
# 3 - Function based views (FBV)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 3.1 GET & POST 
# ~~~~~~~~~~~~~~
@api_view(['GET','POST'])
def FBV_List(request):

    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serialize = GuestSerializer(guests, many = True)
        return Response(serialize.data)

    # POST
    elif request.method == 'POST':
        serialize = GuestSerializer(data= request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status= status.HTTP_201_CREATED)
        return Response(serialize.data, status= status.HTTP_400_BAD_REQUEST)



# 3.2 GET PUT DELETE 
# ~~~~~~~~~~~~~~~~~~
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):

    try:
        guest = Guest.objects.filter(pk=pk)
    except Guest.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
   

    # GET
    if request.method == 'GET':
        serialize = GuestSerializer(guest, many = True)
        return Response(serialize.data)

    # PUT
    elif request.method == 'PUT':
        serialize = GuestSerializer(guest, data= request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.data.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status= status.HTTP_200_OK)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4- Class based views (CBV)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~