from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index_page'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='login'),
    path('logout/', views.LoginOutView.as_view(), name='logout'),
]