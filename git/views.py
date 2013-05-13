# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import *
from django.forms.models import model_to_dict

from git.models import Repository, PublicKey 
from git.forms import PublicKeyForm, RepositoryForm, UserForm


def index(request):
    return HttpResponse("Index")


def repo_view(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    name = "%s/%s" %(user_name, repo_name)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    if repo.is_public or user == owner:
        collaborators = repo.collaborators.all()
        context = {
            'repo' : repo,
            'owner' : owner,
            'user'  : user,
            'collaborators': collaborators,
        }
        return render_to_response('git/repo.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponse('Not authorized', status=401)


def user_settings(request):
    user = request.user
    if request.method == 'GET' and user.is_authenticated():
        pubkeys = user.publickey_set.all()
        user_form = UserForm(model_to_dict(user))
        new_pk = PublicKeyForm()
        context = {
            'user' : user,
            'user_form' : user_form,
            'pk_form' : new_pk,
            'keys' : pubkeys,
        }
        return render_to_response('git/user_settings.html', context, context_instance=RequestContext(request))
    elif request.method == 'POST' and user.is_authenticated():
        user_form = UserForm(request.POST, instance=user)
        user = user_form.save()
        return redirect('repo_list', user.username)
    else:
        return HttpResponse('How did you get here?', status=401)


def pubkey_add(request):
    user = request.user
    if request.method == 'GET':
        return HttpResponse("not implemented")
    elif user.is_authenticated():
        form = PublicKeyForm(request.POST)
        key = form.save(commit=False)
        key.owner = user
        key.save()
        return redirect('user_settings')
    else:
        return HttpResponse("You should be authenticated....")


def pubkey_delete(request, key_id):
    pk = get_object_or_404(PublicKey, pk=key_id)
    if pk.owner == request.user and request.method == 'POST':
        pk.delete()
        return redirect('user_settings')


def pubkey_edit(request, key_id):
    pk = get_object_or_404(PublicKey, pk=key_id)
    user = request.user
    if not user.is_authenticated():
        return HttpResponse("you should be authenticated")
    if pk.owner == user and request.method == 'POST':
        form = PublicKeyForm(request.POST, instance=pk)
        pk = form.save()
        return redirect('user_settings')
    elif pk.owner == user and request.method == 'GET':
        form = PublicKeyForm(model_to_dict(pk))
        context = { 'form' : form, 'pk' : pk , 'user': user}
        return render_to_response('git/key_edit.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponse("What is this case even?")


def repo_list(request, user_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    if user_name == user.username:
        repos = Repository.objects.filter(owner=owner)
        colab = owner.collaborator_set.all()
    else:
        repos = Repository.objects.filter(owner=owner, is_public=True)
        mine = user.collaborator_set.filter(owner=owner)
        theirs = owner.collaborator_set.filter(owner=user)
        colab = mine | theirs
    context = {
        'repos' : repos,
        'owner' : owner,
        'user'  : user,
        'colab' : colab
    }
    return render_to_response('git/repo_list.html', context, context_instance=RequestContext(request))


def repo_add(request, user_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    if user == owner and request.method == 'POST':
        name = request.POST['repo_name']
        repo = Repository(name=name, owner=owner)
        repo.save()
        return redirect('repo_edit', user_name, repo.name)
    else:
        return HttpResponse("No way")


def repo_delete(request, user_name, repo_name):
    user = request.user
    owner = get_object_or_404(User, username=user_name)
    if user == owner and request.method == 'POST':
        repo = get_object_or_404(Repository, owner=owner, name=repo_name)
        repo.delete()
        return redirect('repo_list', user.username)


def repo_edit(request, user_name, repo_name):
    owner = get_object_or_404(User, username=user_name)
    user = request.user
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    if request.method == 'GET' and owner == user:
        form = RepositoryForm(model_to_dict(repo))
        context = {
            'owner': owner,
            'user' : user,
            'repo' : repo,
            'form' : form,
        }
        return render_to_response('git/repo_edit.html', context, context_instance=RequestContext(request))
    elif request.method == 'POST' and owner == user:
        form = RepositoryForm(request.POST, instance=repo)
        repo = form.save()
        return redirect('repo_view', user.username, repo.name)
    else:
        return HttpResponse('How did you get here?', status=401)


