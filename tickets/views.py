from django.shortcuts import render
from django.http.response import JsonResponse 
from django.http import Http404
from .models import Movie, Guest, Reservation
from rest_framework.decorators import api_view 
from rest_framework import status, filters, mixins, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
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

# 4.1 list and Create GET & POST 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

class CBV_List(APIView):
    #GET
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)
    
    #POST
    def post(self, request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status= status.HTTP_201_CREATED)
        return Response( serializer.data, status= status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE 
# ~~~~~~~~~~~~~~~~~~

class CBV_pk(APIView):
    
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk = pk)
        except Guest.DoesNotExist:
            raise Http404
        
    #GET
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    #PUT
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE 
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_200_OK)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 5- Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      

# 5.1 mixins list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset =Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self,  request):
        return self.create(request)


# 5.2 mixins GET PUT DELETE 
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset =Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)
    
    def put(self,  request, pk):
        return self.update(request)
    
    def delete(self,  request, pk):
        return self.destroy(request)
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 6- Generics 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 6.1 list and Create GET & POST 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 6.2 get __ put __ delete
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 7- ViewSets 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # filter_backends = [filter.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 8- Find movie 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 9 - Create New Reservation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie']
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status= status.HTTP_201_CREATED)