from django.urls import path
from .api_razorpay import CreateOrderAPIView, TransactionAPIView, IsSubscribedAPIView


urlpatterns = [
    path('order/create/', CreateOrderAPIView.as_view(), name='create-order-api'),
    path('order/complete/', TransactionAPIView.as_view(), name='complete-order-api'),
    path('user/is_subscribed/', IsSubscribedAPIView.as_view(), name='is-subscribed-api'),
]