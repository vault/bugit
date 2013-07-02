# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.template import RequestContext
from django.db import IntegrityError

from common.models import Repository, Collaboration
from common.models import owned_repos, readable_repos, writable_repos
from repo_manage.forms import RepositoryForm, NewRepositoryForm, CollaborationFormSet

from common.util import get_context

def index(request):
    user = request.user
    return redirect("repo_list", user.username)


def repo_view(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    owners = repo.owners()
    writers = repo.writers()
    readers = repo.readers()

    can_see = user in repo.collaborators.all()
    can_edit = user in owners

    if not can_see:
        return HttpResponse('Not authorized', status=401)

    context = get_context(request,
            {'repo' : repo, 'owner' : owner,'can_see':can_see, 'can_edit': can_edit,
                'owners': owners, 'writers':writers, 'readers':readers })
    return render_to_response('repo_manage/repo.html', context, context_instance=RequestContext(request))


def repo_list(request, user_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)

    if user == owner:
        owned = owned_repos(owner, include_private=True)
        write = writable_repos(owner, include_private=True) 
        read  = readable_repos(owner, include_private=True)
    else:
        owned = owned_repos(owner)
        write = writable_repos(owner)
        read = None
    context = get_context(request,
            { 'owned' : owned,'write':write, 'read':read, 'owner' : owner,})
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
                repo.collaboration_set.add(Collaboration(user=user, permission='O'))
                return redirect('repo_edit', user.username, repo.name)
            except IntegrityError:
                new_form._errors["repo_name"] = ErrorList(["You DKDKDK already have a repository named that"])
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
                repo.collaboration_set.add(Collaboration(user=user, permission='O'))
                return redirect('repo_view' , user.username, repo.name)
            except IntegrityError:
                new_form._errors["repo_name"] = ErrorList(["You ABABAB already have a repository named that"])
    context = get_context(request, { 'new_form':new_form, 'form':form})
    return render_to_response('repo_manage/repo_edit.html', context, context_instance=RequestContext(request))


def repo_edit(request, user_name, repo_name):
    owner = get_object_or_404(User, username=user_name)
    user = request.user
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    owners = repo.owners()

    if user not in owners:
        return HttpResponse("You can't edit this", status=401)

    if request.method == 'GET':
        form = RepositoryForm(model_to_dict(repo))
        colab_form = CollaborationFormSet(instance=repo, 
                queryset=repo.collaboration_set.exclude(user=user))
    elif request.method == 'POST':
        form = RepositoryForm(request.POST, instance=repo)
        colab_form = CollaborationFormSet(request.POST, instance=repo)
        if form.is_valid() and colab_form.is_valid():
            repo = form.save()
            colab_form.save()
            return redirect('repo_view', user.username, repo.name)

    context = get_context(request, {'owner': owner, 'repo' : repo, 'form' : form, 'colab': colab_form})
    return render_to_response('repo_manage/repo_edit.html', context, context_instance=RequestContext(request))


def repo_delete(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if user not in repo.owners():
        return HttpResponse("You can't delete this", status=401)

    if request.method == 'POST':
        repo.delete()
        return redirect('repo_list', user.username)
    else:
        return HttpResponse("You can't do that", status=405)



