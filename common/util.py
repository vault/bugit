
from common.models import *
from repo_manage.forms import NewRepositoryForm

def get_context(request, ctx):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['new_repo_form'] = NewRepositoryForm()
    new_ctx = dict(context.items() + ctx.items())
    return new_ctx

