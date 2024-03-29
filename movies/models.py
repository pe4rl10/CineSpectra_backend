from django.db import models

# Create your models here.
class Movies(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
