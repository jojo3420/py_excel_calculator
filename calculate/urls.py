from . import views
from django.urls import path

urlpatterns = [
    path('', views.calculate, name='calculate_page')
]