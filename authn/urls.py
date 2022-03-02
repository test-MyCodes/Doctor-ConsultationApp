from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name='login'),
    path('how/',views.how,name='how'),
    path('forget/',views.forget,name='forget'),
    path('changepassword/<token>/',views.changepassword,name='changepassword'),
    path('logout',views.logout,name='logout')
]