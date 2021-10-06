from django.db import models
from datetime import datetime

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=53)
    content = models.TextField(blank=True)
    date_created = models.DateTimeField(default=datetime.utcnow)
    creator = models.CharField(default='Anon', max_length=33)
    receiver_id = models.IntegerField(default=0)
    public_id = models.CharField(max_length=103)

    def __str__(self):
        return self.title
