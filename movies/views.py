from .models import Movies
from .serializers import MoviesSerializer, MovieIdSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer



from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class MovieList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

class MovieDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Movies
    serializer_class = MoviesSerializer

    def get_object(self, queryset=None):
        movie_id = self.kwargs.get('movie_id')
        return get_object_or_404(Movies, movie_id=movie_id)

class RecommendMovieList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Movies
    serializer_class = MovieIdSerializer

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        movie_obj = Movies.objects.get(movie_id=movie_id)
        movie_index = movie_obj.id
        print(movie_index)

        movies = pickle.load(open('movies.pkl', 'rb'))

        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(movies['tags']).toarray()

        similarity = cosine_similarity(vectors)




        distances = similarity[movie_index - 1]
        print(distances)
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

        recommendations = []
        for i in movies_list:
            obj = Movies.objects.get(id=(i[0] + 1))
            recommendations.append(obj)
        return recommendations




