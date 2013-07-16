from common.models import User
from django.db import models

# Create your models here.

class Message(models.Model):
    subject = models.CharField(max_length=140)
    message = models.TextField()
    sender = models.ForeignKey(User)
    sent = models.BooleanField(default=False)

