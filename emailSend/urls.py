from . import views
from django.urls import path


urlpatterns = [
    path('send/', views.send, name='send'),
    path('send_page/', views.send_page, name='send_page'),
]