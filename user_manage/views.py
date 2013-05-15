from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import *
from django.forms.models import model_to_dict

from common.models import PublicKey 
from common.util import *

from user_manage.forms import UserForm, PublicKeyForm


def user_settings(request):
    user = request.user
    new_pk = PublicKeyForm()
    pubkeys = user.publickey_set.all()

    if not user.is_authenticated():
        return HttpResponse("Not authorized", status=401)

    if request.method == 'GET':
        user_form = UserForm(model_to_dict(user))
    elif request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            return redirect('repo_list', user.username)
    context = get_context(request, { 'user_form' : user_form, 'pk_form': new_pk, 'keys' : pubkeys })
    return render_to_response('user_manage/user_settings.html', context, context_instance=RequestContext(request))


def pubkey_add(request):
    user = request.user
    if request.method == 'GET':
        return HttpResponse("not implemented", status=405)

    if not user.is_authenticated():
        return HttpResponse("You should be authenticated....", status=401)

    form = PublicKeyForm(request.POST)
    if form.is_valid():
        key = form.save(commit=False)
        key.owner = user
        key.save()
        return redirect('user_settings')
    else:
        pubkeys = user.publickey_set.all()
        user_form = UserForm(model_to_dict(user))
        context = get_context(request, {'form' : form})
        return render_to_response('user_manage/key_edit.html', context, context_instance=RequestContext(request))


def pubkey_delete(request, key_id):
    pk = get_object_or_404(PublicKey, pk=key_id)
    if pk.owner == request.user and request.method == 'POST':
        pk.delete()
        return redirect('user_settings')


def pubkey_edit(request, key_id=None):
    if key_id is not None:
        pk = get_object_or_404(PublicKey, pk=key_id)
    else:
        pk = None
    user = request.user
    if not user.is_authenticated() or pk.owner != user:
        return HttpResponse("Not allowed", status=401)

    if request.method == 'POST':
        form = PublicKeyForm(request.POST, instance=pk)
        if form.is_valid():
            pk = form.save()
            return redirect('user_settings')
    elif request.method == 'GET':
        form = PublicKeyForm(model_to_dict(pk))
    else:
        return HttpResponse("Not implemented", status=405)

    context = get_context(request, {'form' : form, 'pk' : pk})
    return render_to_response('user_manage/key_edit.html', context, context_instance= RequestContext(request))

