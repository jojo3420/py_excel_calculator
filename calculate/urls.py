from . import views
from django.urls import path

urlpatterns = [
    path('excel/', views.calculate, name='calculate_page')
]