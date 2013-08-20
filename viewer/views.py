from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404

from requests import get
from urllib import urlretrieve

from common.models import Repository
from common.util import get_context


def cgit_url(user_name, repo_name, path, query=None):
    if path is not None:
        base = 'http://localhost:8080/view/%s/%s/%s' %(user_name, repo_name, path)
    else:
        base = 'http://localhost:8080/view/%s/%s' %(user_name, repo_name)
    if query is not None and len(query)>1:
        base = "%s?%s" % (base, query)
    return base


def view_index(request):
    return redirect('index')


def user_index(request, user_name):
    return redirect('repo_list', user_name)


def repo_plain(request, user_name, repo_name, path, prefix='plain'):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    can_see = user == owner or repo.is_public
    can_edit = user in collaborators
    if not (can_see or can_edit):
        return HttpResponse('Not authorized', status=401)

    query = request.GET.urlencode()
    new_path = '%s/%s' % (prefix, path)
    url = cgit_url(user_name, repo_name, new_path, query)
    (fname, info) = urlretrieve(url)
    response = HttpResponse(FileWrapper(open(fname)), content_type='text/plain')
    return response
    


def repo_snapshot(request, user_name, repo_name, path):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()
 
    can_see = user == owner or repo.is_public
    can_edit = user in collaborators
    if not (can_see or can_edit):
        return HttpResponse('Not authorized', status=401)
  
    query = request.GET.urlencode()
    new_path = 'snapshot/%s' % path
    filename = path.split('/')[-1]
    url = cgit_url(user_name, repo_name, new_path, query)
    (fname, info) = urlretrieve(url)
    response = HttpResponse(FileWrapper(open(fname)), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


def repo_browse(request, user_name, repo_name, path=None):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    can_see = user == owner or repo.is_public
    can_edit = user in collaborators

    commit_id = None

    method = None
    parts = request.path.split('/')
    if len(parts) >= 4:
        if len(parts[4]) > 1:
            method = parts[4]
        else:
            method = 'summary'

    try:
        commit_id = request.GET['id']
    except KeyError:
        pass

    if not (can_see or can_edit):
        return HttpResponse('Not authorized', status=401)

    query = request.GET.urlencode()
    url = cgit_url(user_name, repo_name, path, query)
    text = get(url)

    context = get_context(request, {'owner': owner, 'repo_html':text.text, 'repo':repo,
        'can_see': can_see, 'can_edit':can_edit, 'id':commit_id, 'method':method})
    return render_to_response('viewer/repo_view.html', context)


