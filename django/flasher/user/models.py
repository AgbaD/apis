from django.db import models

# Create your models here.


class Note(models.Model):
    user_id = models.IntegerField
    question = models.TextField()
    answer = models.TextField()
