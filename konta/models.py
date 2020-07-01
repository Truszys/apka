from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
# Create your models here.

class Nawyki(models.Model):
    nazwa = models.CharField(max_length=200)
    start = models.DateField(auto_now_add=True)
    koniec = models.DateField(null=True, blank=True)
    dzisiaj_zrobione = models.BooleanField(default=False)
    zrobione = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)