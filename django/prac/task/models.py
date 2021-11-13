from django.db import models

# Create your models here.


class Player(models.Model):
    firstname = models.CharField(max_length=33)
    lastname = models.CharField(max_length=33)
    email = models.EmailField("email")
    password = models.CharField(max_length=103)
    public_id = models.CharField(max_length=103)
    number = models.IntegerField(default=0)

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)
