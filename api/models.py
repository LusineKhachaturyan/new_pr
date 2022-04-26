from email.policy import default
from django.db import models
from django.forms import BooleanField, CharField

class Checkbox(models.Model):

    name = models.CharField(max_length=150)
    is_checked = models.BooleanField(default=False)
