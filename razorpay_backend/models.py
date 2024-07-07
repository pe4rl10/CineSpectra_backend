from django.db import models
from django.conf import settings

class Transaction(models.Model):
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        return f"Transaction {self.id} for {self.user}"

    def save(self, *args, **kwargs):
        # Call the parent class' save() method
        super().save(*args, **kwargs)

        # Check if the user associated with the transaction is subscribed
        if not self.user.is_subscribed:
            # Update the is_subscribed attribute to True
            self.user.is_subscribed = True
            self.user.save()  # Save the user instance
