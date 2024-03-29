from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='history')
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=5, choices=[('movie', 'Movie'), ('tv', 'TV')], default='movie')

    def __str__(self):
        return str(self.media_id)