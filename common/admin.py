
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin

from .models import Collaboration, PublicKey, Repository

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

