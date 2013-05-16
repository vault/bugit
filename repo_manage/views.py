# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.template import RequestContext
from django.db import IntegrityError

from common.models import Repository
from repo_manage.forms import RepositoryForm, NewRepositoryForm

from common.util import get_context

def index(request):
    user = request.user
    return redirect("repo_list", user.username)


def repo_view(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    collaborators = repo.collaborators.all()

    can_see = repo.is_public or user == owner
    can_edit = user in collaborators or user == owner
    can_view = can_see or can_edit
    if not can_view:
        return HttpResponse('Not authorized', status=401)

    context = get_context(request,
            {'repo' : repo, 'owner' : owner,'can_see':can_see, 'can_edit': can_edit, 'collaborators': collaborators })
    return render_to_response('repo_manage/repo.html', context, context_instance=RequestContext(request))


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


def repo_simple_new(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("You can't add this", status=401)
    
    if request.method == 'GET':
        return redirect('repo_new')
    elif request.method == 'POST':
        new_form = NewRepositoryForm(request.POST)
        if new_form.is_valid():
            repo = Repository(owner=user)
            repo.name = new_form.cleaned_data['repo_name']
            try:
                repo.save()
                return redirect('repo_edit', user.username, repo.name)
            except IntegrityError:
                new_form._errors["repo_name"] = ErrorList(["You already have a repository named that"])
    context = get_context(request, {'new_form':new_form, 'form':RepositoryForm()})
    return render_to_response('repo_manage/repo_edit.html', context, context_instance=RequestContext(request))


def repo_new(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("You can't add this", status=401)

    if request.method == 'GET':
        new_form = NewRepositoryForm()
        form = RepositoryForm()
    elif request.method == 'POST':
        new_form = NewRepositoryForm(request.POST)
        form = RepositoryForm(request.POST)
        if new_form.is_valid() and form.is_valid():
            repo = form.save(commit=False)
            repo.owner = user
            repo.name = new_form.cleaned_data['repo_name']
            try:
                repo.save()
                return redirect('repo_view' , user.username, repo.name)
            except IntegrityError:
                new_form._errors["repo_name"] = ErrorList(["You already have a repository named that"])
    context = get_context(request, { 'new_form':new_form, 'form':form})
    return render_to_response('repo_manage/repo_edit.html', context, context_instance=RequestContext(request))


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

    if user != owner:
        return HttpResponse("You can't delete this", status=401)

    if request.method == 'POST':
        repo = get_object_or_404(Repository, owner=owner, name=repo_name)
        repo.delete()
        return redirect('repo_list', user.username)
    else:
        return HttpResponse("You can't do that", status=405)



