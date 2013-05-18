from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib import admin

from common.signals import dispatch_repo_work


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
        return "%s for \"%s\"" % (self.description, self.owner.username)



class Repository(models.Model):
    owner = models.ForeignKey(User, related_name='owner_set')
    name = models.SlugField(max_length=100, editable=False)
    description = models.CharField(max_length=100, blank=True)
    long_description = models.TextField(blank=True)
    is_public = models.BooleanField()
    is_created = models.BooleanField()
    collaborators = models.ManyToManyField(User, through='Collaboration', related_name='collaborator_set', blank=True)

    class Meta:
        unique_together = ("owner", "name")

    def __unicode__(self):
        return "%s/%s" %(self.owner.username, self.name)

    def get_clone_url(self):
        return "git@eng-git.bu.edu:%s/%s" % (self.owner.username, self.name)

    def get_public_clone_url(self):
        return "git://eng-git.bu.edu/%s/%s" % (self.owner.username, self.name)


class Collaboration(models.Model):
    PERMISSIONS = (
        ('O', 'Owner'),
        ('R', 'Read'),
        ('W', 'Read/Write'),
    )
    user = models.ForeignKey(User)
    repository = models.ForeignKey(Repository)
    permission = models.CharField(max_length=1, choices=PERMISSIONS)

    class Meta:
        unique_together = ("user", "repository")

    def __unicode__(self):
        return "{0} access for {1} on {2}".format(self.permission, self.user, self.repository)
    


admin.site.register(PublicKey)
admin.site.register(Repository)
admin.site.register(Collaboration)

post_save.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_save.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")
