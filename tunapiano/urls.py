"""tunapiano URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from tunaapi.views.artist import ArtistViewSet
from tunaapi.views.genre import GenreViewSet
from tunaapi.views.song import SongViewSet, SongGenreViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'song_genres', SongGenreViewSet, basename='song_genre')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
