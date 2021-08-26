from django.db import models


# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    pwd = models.CharField(max_length=100)
    is_verify = models.BooleanField(default=False)
