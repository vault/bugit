from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import *
from requests import get

from common.models import Repository
from common.util import *


def repo_browse(request, user_name, repo_name, path=None):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    #repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    #collaborators = repo.collaborators.all()
    #if user != owner or not repo.is_public or not user in collaborators:
        #return HttpResponse('Not autorized', status=401)

    if path is not None:
        text = get('http://localhost:8080/view/%s/%s/%s' %(user_name, repo_name, path))
    else:
        text = get('http://localhost:8080/view/%s/%s' %(user_name, repo_name))

    context = get_context(request, {'repo_html':text.text})
    return render_to_response('viewer/repo_view.html', context)


