from django.urls import path
from .views import MovieList, MovieDetail, RecommendMovieList
from rest_framework.routers import DefaultRouter

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view()),
    path('movie/<str:movie_id>/', MovieDetail.as_view()),
    path('recommend-movie/<str:movie_id>/', RecommendMovieList.as_view()),
]