from django.urls import path
from . import views

urlpatterns = [
    path('', views.load),
    path('main', views.index),
    path('registerUser', views.registerUser),
    path('loginUser', views.loginUser),
    path('travels', views.travels),
    path('logout', views.logout),
    path('createTrip', views.createTrip),
    path('joinTrip/<tripID>', views.joinTrip),
    path('travels/add', views.newTrip),
    path('travels/destination/<tripID>', views.viewTrip),
    
]
