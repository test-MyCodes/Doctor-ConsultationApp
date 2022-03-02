from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('attendant/<int:pk>/',views.attendant,name='attendant'),
    path('doctor/<int:pk>/',views.doctor,name='doctor'),
    path('getdata/',views.getdata,name='getdata'),
    path('test/<int:pk>/',views.test,name='test'),
    path('medicalshop/<int:pk>/',views.medicalshop,name='medicalshop'),
    path('getmedicalshop/',views.getmedicalshop,name='getmedicalshop'),
    path('givetablets/<int:pk>/',views.givetablets,name='givetablets'),
    path('medicalshop/<int:test>/notAvailTablets/',views.notAvailTablets,name='notAvailTablets')
    #path('back/',views.back,name='back')
]