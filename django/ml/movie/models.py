from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField('description')
    rating = models.IntegerField(default=0)
    director = models.CharField(max_length=100)
    public_id = models.CharField(max_length=300)
    release_date = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(default=1)
    price = models.IntegerField(default=1)

    def __str__(self):
        return self.title


