from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import *
from requests import get

from common.models import Repository
from common.util import *


def view_index(request):
    return redirect('index')


def user_index(request, user_name):
    return redirect('repo_list', user_name)


def repo_browse(request, user_name, repo_name, path=None):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    can_see = user == owner or repo.is_public
    can_edit = user in collaborators
    if not (can_see or can_edit):
        return HttpResponse('Not authorized', status=401)

    query = request.GET.urlencode()
    if path is not None:
        text = get('http://localhost:8080/view/%s/%s/%s?%s' %(user_name, repo_name, path, query))
    else:
        text = get('http://localhost:8080/view/%s/%s?%s' %(user_name, repo_name, query))

    context = get_context(request, {'repo_html':text.text})
    return render_to_response('viewer/repo_view.html', context)


