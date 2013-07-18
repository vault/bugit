from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib import admin
import base64, hashlib

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

    def fingerprint(self):
        key = base64.b64decode(self.pubkey.strip().partition('ssh-rsa ')[2])
        plain = hashlib.md5(key).hexdigest()
        return ':'.join(a+b for a,b in zip(plain[::2], plain[1::2]))


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

    def owners(self):
        return self.collaborators.filter(collaboration__permission='O')
    
    def readers(self):
        return self.collaborators.filter(collaboration__permission='R')

    def writers(self):
        return self.collaborators.filter(collaboration__permission='W')


class Collaboration(models.Model):
    PERMISSIONS = (
        ('O', 'Owner'),
        ('R', 'Read'),
        ('W', 'Read/Write'),
    )
    user = models.ForeignKey(User)
    repository = models.ForeignKey(Repository)
    permission = models.CharField(max_length=1, choices=PERMISSIONS, default='R')

    class Meta:
        unique_together = ("user", "repository")

    def __unicode__(self):
        return "{0} access for {1} on {2}".format(self.permission, self.user, self.repository)
    
# Methods for getting repos
#
# Just pass the user in as the first arg... 
# In Django 1.5 we could have subclassed AbstractUser for these
def owned_repos(self, include_private=False):
    if include_private:
        return self.collaborator_set.filter(collaboration__permission='O')
    else:
        return self.collaborator_set.filter(collaboration__permission='O', is_public=True)

def writable_repos(self, include_private=False):
    if include_private:
        return self.collaborator_set.filter(collaboration__permission='W')
    else:
        return self.collaborator_set.filter(collaboration__permission='W', is_public=True)

def readable_repos(self, include_private=False):
    if include_private:
        return self.collaborator_set.filter(collaboration__permission='R')
    else:
        return self.collaborator_set.filter(collaboration__permission='R', is_public=True)

class CollaborationInline(admin.TabularInline):
    model = Collaboration
    extra = 1

class RepoAdmin(admin.ModelAdmin):
    inlines = (CollaborationInline,)


admin.site.register(PublicKey)
admin.site.register(Repository, RepoAdmin)

post_save.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_save.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")
