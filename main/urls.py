from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.Index, name='Index'),
    path('settings/', views.Settings, name='Settings'),
    path('signin/', views.Signin, name='Signin'),
    path('signup/', views.Signup, name='Signup'),
    path('logout/', views.Logout, name='Logout'),
    path('upload/', views.Upload, name='Upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.Profile, name='profile'),
    path('follower', views.Follow, name='Follow'),
    path('search', views.Search, name='Search')
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
