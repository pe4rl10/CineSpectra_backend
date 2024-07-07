from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializers import CreateOrderSerializer, TransactionSerializer
from rest_framework.response import Response
from .razorpay.main import RazorpayClient
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

rz_client = RazorpayClient()

class CreateOrderAPIView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = [JWTAuthentication]
    def post(self, request):
        create_order_serializer = CreateOrderSerializer(
            data=request.data
        )
        if create_order_serializer.is_valid():
            order_response = rz_client.create_order(
                amount=create_order_serializer.validated_data["amount"],
                currency=create_order_serializer.validated_data["currency"]
            )

            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Order created successfully",
                "data": order_response
            }

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": create_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TransactionAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request):
        print(request.data)

        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid():
            rz_client.verify_payment(
                razorpay_order_id=transaction_serializer.validated_data["order_id"],
                razorpay_payment_id=transaction_serializer.validated_data["payment_id"],
                razorpay_signature=transaction_serializer.validated_data["signature"]
            )
            transaction_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Transaction created successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Bad Request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class IsSubscribedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_subscribed = user.is_subscribed
        return Response({"is_subscribed": is_subscribed}, status=status.HTTP_200_OK)