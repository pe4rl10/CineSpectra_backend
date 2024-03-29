from rest_framework import serializers
from .models import Movies

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

class MovieIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['movie_id', 'title']