
from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
   
    #1 without REST and No model Query => FBV
    path('django/norestnomodel/', views.no_rest_no_model),

    #2 Model data default django without REST.
    path('django/norestfrommodel/', views.no_rest_from_model),

]
