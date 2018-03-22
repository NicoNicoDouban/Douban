from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class userActive(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=30)

    def __str__(self):
        return self.username
