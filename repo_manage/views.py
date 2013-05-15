# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import *
from django.forms.models import model_to_dict

from common.models import Repository
from repo_manage.forms import RepositoryForm, NewRepositoryForm

from common.util import *

def index(request):
    return HttpResponse("Index")


def repo_view(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    name = "%s/%s" %(user_name, repo_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    #if not repo.is_public or user != owner or not user in collaborators:
        #return HttpResponse('Not authorized', status=401)

    context = get_context(request,
            { 'repo' : repo, 'owner' : owner, 'collaborators': collaborators })
    return render_to_response('repo_manage/repo.html', context, context_instance=RequestContext(request))


def repo_browse(request, user_name, repo_name, path=None):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()
    #if user != owner or not repo.is_public or not user in collaborators:
        #return HttpResponse('Not autorized', status=401)

    if path is not None:
        text = get('http://localhost/cgit/%s/%s/%s' %(user_name, repo_name, path))
    else:
        text = get('http://localhost/cgit/%s/%s' %(user_name, repo_name))

    context = get_context(request, {'repo':repo, 'repo_html':text.text})
    return render_to_response('repo_manage/repo_view.html', context)


def repo_list(request, user_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)

    if user == owner:
        repos = Repository.objects.filter(owner=owner)
        colab = owner.collaborator_set.all()
    else:
        repos = Repository.objects.filter(owner=owner, is_public=True)
        mine = user.collaborator_set.filter(owner=owner)
        theirs = owner.collaborator_set.filter(owner=user)
        colab = mine | theirs
    context = get_context(request,
            { 'repos' : repos, 'owner' : owner, 'colab' : colab})
    return render_to_response('repo_manage/repo_list.html', context, context_instance=RequestContext(request))


def repo_add(request, user_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)

    if owner != user:
        return HttpResponse("You can't add this", status=401)

    if request.method == 'POST':
        form = NewRepositoryForm(request.POST)
        if form.is_valid():
            repo = Repository(name=form.cleaned_data['repo_name'], owner=owner)
            repo.save()
            return redirect('repo_edit', user_name, repo.name)
    else:
        return HttpResponse("You can't do that", status=405)

    context = get_context(request, {'new_form': form, 'form': RepositoryForm(), 'owner':owner})
    return render_to_response("repo_manage/repo_edit.html", context, context_instance=RequestContext(request))


def repo_new(request, user_name):
    owner = get_object_or_404(user, username=user_name)
    user = request.user

    if owner != user:
        return HttpResponse("You can't add this", status=401)

    if request.method == 'GET':
        new_form = NewRepositoryForm()
        form = RepositoryForm()
    elif request.method == 'POST':
        form = RepositoryForm(request.POST, owner=owner, name='f686bdfe')
        new_form = NewRepositoryForm(request.POST)
        if new_form.is_valid() and form.is_valid():
            repo = form.save(commit=False)
            repo.owner = owner
            repo.name = new_form.cleaned_data['repo_name']
            repo.save()
            return redirect('repo_view' , owner.user_name, repo.name)
    context = get_context(request, {'new_form':new_form, 'form':form})
    return render_to_response('repo_manage/repo.html', context, context_instance=RequestContext(request))


def repo_edit(request, user_name, repo_name):
    owner = get_object_or_404(User, username=user_name)
    user = request.user
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if owner != user:
        return HttpResponse("You can't edit this", status=401)

    if request.method == 'GET':
        form = RepositoryForm(model_to_dict(repo))
    elif request.method == 'POST':
        form = RepositoryForm(request.POST, instance=repo)
        if form.is_valid():
            repo = form.save()
            return redirect('repo_view', user.username, repo.name)

    context = get_context(request, {'owner': owner, 'repo' : repo, 'form' : form, })
    return render_to_response('repo_manage/repo_edit.html', context, context_instance=RequestContext(request))


def repo_delete(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    if user == owner and request.method == 'POST':
        repo = get_object_or_404(Repository, owner=owner, name=repo_name)
        repo.delete()
        return redirect('repo_list', user.username)


