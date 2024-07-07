from rest_framework import serializers

from ..models import Transaction



class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()

class TransactionSerializer(serializers.ModelSerializer):
    # # Add a field to include the username of the associated user
    # user = serializers.StringRelatedField(source='user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['payment_id', 'order_id', 'signature', 'amount', 'user']
