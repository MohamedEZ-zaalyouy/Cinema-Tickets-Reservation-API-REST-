
from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservation', views.viewsets_reservation)


urlpatterns = [
    path('admin/', admin.site.urls),
   
    #1 without REST and No model Query => FBV
    path('django/norestnomodel/', views.no_rest_no_model),

    #2 Model data default django without REST.
    path('django/norestfrommodel/', views.no_rest_from_model),

    # 3 - Function based views (FBV)
    # 3 .1 GET & POST 
    path('rest/fbv', views.FBV_List ),


    # 3 .2 GET PUT DELETE 
    path('rest/fbv/<int:pk>', views.FBV_pk ),

    # 4- Class based views (CBV)

    # 4.1 list and Create GET & POST 
    path('rest/cbv/', views.CBV_List.as_view() ),

    # 4.2 GET PUT DELETE  
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view() ),

    # 5- Mixins
    # 5.1 list and Create GET & POST with Mixins
    path('rest/mixins/', views.mixins_list.as_view() ),


    # 5.2 GET PUT DELETE with Mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view() ),


    # 6- Generics
    # 6.1 list and Create GET & POST with Generics
    path('rest/generics/', views.generics_list.as_view() ),


    # 6.2 GET PUT DELETE with Generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view() ),


    # 7- ViewSets 
    path('rest/viewsets/', include(router.urls)),


    #  8- Find movie 
    path('fbv/findmovie/', views.find_movie),


    #   9- Create New Reservation
    path('fbv/newreservation/', views.new_reservation),

]
