from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


# Create your models here.
class User(AbstractUser):
    weight = models.IntegerField(null=True)
    goal = models.IntegerField(null=True)
    initial = models.IntegerField(null=True)
    end_date = models.DateField(null=True)
    start_date = models.DateField(default=datetime.date.today, null=True)
    metric = models.BooleanField(default=True)
