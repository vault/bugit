from common.models import User
from django.db import models
from django.contrib import admin

# Create your models here.

class Message(models.Model):
    subject = models.CharField(max_length=140)
    message = models.TextField()
    sender = models.ForeignKey(User)
    sent = models.BooleanField(default=False)

    def __unicode__(self):
        return '"{0}" from {1}'.format(self.subject, self.sender.username)

admin.site.register(Message)

