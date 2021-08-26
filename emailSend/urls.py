from . import views
from django.urls import path


urlpatterns = [
    path('send/', views.send, name='send_page'),
]