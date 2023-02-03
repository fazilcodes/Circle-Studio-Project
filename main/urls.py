from django.urls import path
from . import views



urlpatterns = [
    path('', views.Index, name='Index'),
    path('settings/', views.Settings, name='Settings'),
    path('signin/', views.Signin, name='Signin'),
    path('signup/', views.Signup, name='Signup'),
    path('logout/', views.Logout, name='Logout'),
    path('upload/', views.Upload, name='Upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.Profile, name='profile')
]