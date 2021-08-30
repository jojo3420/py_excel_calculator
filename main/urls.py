from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index_page'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('failed/', views.failed_login, name='failed_login'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
]