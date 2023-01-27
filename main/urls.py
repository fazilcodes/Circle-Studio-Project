from django.urls import path
from . import views



urlpatterns = [
    path('', views.Index, name='Index'),
    path('signin/', views.Signin, name='Signin'),
    path('signup/', views.Signup, name='Signup'),
]