from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import ObjectDoesNotExist
import base64, hashlib

from django.conf import settings
from .signals import dispatch_repo_work
from validators import validate_key_format, validate_key_decode


class PublicKey(models.Model):
    owner = models.ForeignKey(User)
    description = models.SlugField(max_length=100)
    pubkey = models.TextField(blank=False, validators=[validate_key_format, validate_key_decode])
    is_active = models.BooleanField()

    class Meta:
        unique_together = ("owner", "description")

    def filename(self):
        uname = self.owner.username
        return "%s/%s-%s.pub" % (uname, uname, self.description)

    def __unicode__(self):
        return "%s for \"%s\"" % (self.description, self.owner.username)

    def fingerprint(self):
        key = base64.b64decode(self.pubkey.split(' ')[1])
        plain = hashlib.md5(key).hexdigest()
        return ':'.join(a+b for a,b in zip(plain[::2], plain[1::2]))


class Repository(models.Model):
    desc_formats = (
            ('M', 'Markdown'),
            ('T', 'Text'),
    )
    owner = models.ForeignKey(User, related_name='owner_set')
    name = models.SlugField(max_length=100, editable=False)
    description = models.CharField(max_length=100, blank=True)
    long_description = models.TextField(blank=True)
    description_format = models.CharField(max_length=1, choices=desc_formats, blank=True)
    is_public = models.BooleanField()
    is_created = models.BooleanField()
    collaborators = models.ManyToManyField(User, through='Collaboration', related_name='collaborator_set', blank=True)
    email_on_update = models.BooleanField()

    class Meta:
        unique_together = ("owner", "name")

    def __unicode__(self):
        return "%s/%s" %(self.owner.username, self.name)

    def get_clone_url(self):
        return "%s:%s/%s" % (self._ssh_url(), self.owner.username, self.name)


    def get_public_clone_url(self):
        return "%s/%s/%s" % (self._pub_url(), self.owner.username, self.name)


    def _pub_url(self):
        return 'git://%s' % settings.GIT_HOST


    def _ssh_url(self):
        return '%s@%s' % (settings.GIT_USER, settings.GIT_HOST)


    def owners(self):
        return self.collaborators.filter(collaboration__permission='O')
    
    def readers(self):
        return self.collaborators.filter(collaboration__permission='R')

    def writers(self):
        return self.collaborators.filter(collaboration__permission='W')

    def user_access(self, user):
        try:
            return self.collaboration_set.get(user=user).permission
        except ObjectDoesNotExist:
            if self.is_public:
                return 'R'
            else:
                None


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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    never_email = models.BooleanField()
    
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


try:
    admin.site.register(PublicKey)
    admin.site.register(Repository, RepoAdmin)
except AlreadyRegistered:
    pass


post_save.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_save.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=PublicKey, dispatch_uid="pubkey_save_dispatcher")

post_delete.connect(dispatch_repo_work,
        sender=Repository, dispatch_uid="repo_save_dispatcher")
