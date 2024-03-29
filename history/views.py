from django.shortcuts import render
from .models import History
from rest_framework import generics
from .serializers import HistorySerializer, HistoryMediaIdSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response

# Create your views here.
class HistoryCreate(generics.CreateAPIView):
    permission_classes = [IsOwner]
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class HistoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class HistoryDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class RetrieveHistoryByUser(generics.ListAPIView):
    permission_classes = [IsOwner]
    queryset = History.objects.all()
    serializer_class = HistoryMediaIdSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user')
        if user_id is not None:
            return History.objects.filter(user=user_id)
        return History.objects.none()

class DeleteUserHistory(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = History.objects.none()  # Return an empty queryset
    lookup_url_kwarg = 'user'  # Specify the lookup URL keyword argument

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user')
        History.objects.filter(user=user_id).delete()
        return Response({"detail": "History records deleted successfully."}, status=204)