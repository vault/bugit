from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib import admin

from git.signals import dispatch_repo_work


class PublicKey(models.Model):
    owner = models.ForeignKey(User)
    description = models.SlugField(max_length=100)
    pubkey = models.TextField(blank=False)
    is_active = models.BooleanField()

    class Meta:
        unique_together = ("owner", "description")

    def filename(self):
        uname = self.owner.username
        return "%s/%s-%s.pub" % (uname, uname, self.description)

    def __unicode__(self):
        return "%s for \"%s\"" %(self.description, self.owner.username)


class Repository(models.Model):
    owner = models.ForeignKey(User, related_name='owner_set')
    name = models.SlugField(max_length=100, editable=False)
    description = models.CharField(max_length=100, blank=True)
    long_description = models.TextField(blank=True)
    is_public = models.BooleanField()
    is_created = models.BooleanField()
    collaborators = models.ManyToManyField(User, related_name='collaborator_set', blank=True)

    class Meta:
        unique_together = ("owner", "name")

    def __unicode__(self):
        return "%s/%s" %(self.owner.username, self.name)
    

admin.site.register(PublicKey)
admin.site.register(Repository)

post_save.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_save.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")
