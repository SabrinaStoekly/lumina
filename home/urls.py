from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import handler404  

urlpatterns = [
    path('', views.index, name='home'),    
]

handler404 = 'home.views.custom_404_page'