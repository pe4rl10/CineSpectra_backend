from django.urls import include, path
from .views import HistoryCreate, HistoryList, HistoryDetail, RetrieveHistoryByUser, DeleteUserHistory

urlpatterns = [
    path('add-movie/', HistoryCreate.as_view(), name='add-movie'),
    path('', HistoryList.as_view()),
    path('get-history/<str:user>/', RetrieveHistoryByUser.as_view(), name='retrieve-history-by-user'),
    path('clear-history/<int:user>/', DeleteUserHistory.as_view(), name='clear-history-by-user'),
    path('<int:pk>/', HistoryDetail.as_view(), name='get-single-history-object')
]