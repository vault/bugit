from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404

from requests import get
from urllib import urlretrieve

from common.models import Repository
from common.util import get_context


def cgit_url(user_name, repo_name, method, path, query=None):
    url = 'http://localhost:8080/view'
    if method == 'summary':
        base = '%s/%s/%s' %(url, user_name, repo_name)
    else:
        base = '%s/%s/%s/%s' %(url, user_name, repo_name, method)

    if path is not None:
        base = '%s/%s' %(base, path)

    if query is not None and len(query)>1:
        base = "%s?%s" % (base, query)

    return base

def cumulative_path(path):
    if path is None or len(path) == 0:
        return path

    c = [path[0]]
    for part in path[1:]:
        c.append('%s/%s'%(c[-1], part))

    return c


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


def repo_browse(request, user_name, repo_name, method='summary', path=None):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    can_see = user == owner or repo.is_public
    can_edit = user in collaborators

    if not (can_see or can_edit):
        return HttpResponse('Not authorized', status=401)

    commit_id = request.GET.get('id')
    q = request.GET.get('q', '')
    qtype = request.GET.get('qt', 'grep')

    messages = {
        'grep'  : 'Log Message',
        'author': 'Author',
        'committer' : 'Committer',
        'range' : 'Range' }
    search_text = messages.get(qtype, messages['grep'])

    if method == 'tree':
        file_path = path.split('/')
        path_parts = cumulative_path(file_path)
        file_path = zip(file_path, path_parts)
    else:
        file_path = None

    query = request.GET.urlencode()
    url = cgit_url(user_name, repo_name, method, path, query)
    text = get(url)

    context = get_context(request, {'owner': owner, 'repo_html':text.text, 'repo':repo,
        'can_see': can_see, 'can_edit':can_edit, 'id':commit_id, 'method':method,
        'q':q, 'qtype':qtype, 'search_text':search_text, 'file_path':file_path})
    return render_to_response('viewer/repo_view.html', context)


