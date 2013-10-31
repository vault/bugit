from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.template import RequestContext
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from common.models import PublicKey, UserProfile
from common.util import get_context

from user_manage.forms import UserForm, PublicKeyForm, ProfileForm


def user_settings(request):
    user = request.user
    new_pk = PublicKeyForm()
    p_form = ProfileForm()
    pubkeys = user.publickey_set.all()
    profile = UserProfile.objects.get_or_create(user=user)[0]

    if not user.is_authenticated():
        return HttpResponse("Not authorized", status=401)

    if request.method == 'GET':
        user_form = UserForm(model_to_dict(user))
        p_form = ProfileForm(model_to_dict(profile))
    elif request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            return redirect('user_settings')
    context = get_context(request, { 'user_form' : user_form, 'pk_form': new_pk,
        'keys' : pubkeys, 'profile_form': p_form })
    return render_to_response('user_manage/user_settings.html', context, context_instance=RequestContext(request))


def user_profile(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("Not authorized", status=401)

    if request.method != "POST":
        return HttpResponse("Method not allowed", 405)
    else:
        profile = user.get_profile()
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
        return redirect('user_settings')




def pubkey_add(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("You should be authenticated....", status=401)

    if request.method == 'GET':
        form = PublicKeyForm()
    elif request.method == 'POST':
        form = PublicKeyForm(request.POST)
        if form.is_valid():
            key = form.save(commit=False)
            key.owner = user
            try:
                key.save()
                return redirect('user_settings')
            except IntegrityError:
                form._errors["description"] = ErrorList(["You have a public key with that name already"])
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
        if key_id is not None:
            form = PublicKeyForm(request.POST, instance=pk)
        else:
            form = PublicKeyForm(request.POST)
        if form.is_valid():
            try:
                pk = form.save()
                return redirect('user_settings')
            except IntegrityError:
                form._errors["description"] = ErrorList(["You have a public key with that name already"])
                context = get_context(request, {'form' : form, 'pk': pk})
                return render_to_response('user_manage/key_edit.html', context, context_instance=RequestContext(request))
    elif request.method == 'GET':
        form = PublicKeyForm(model_to_dict(pk))
    else:
        return HttpResponse("Not implemented", status=405)

    context = get_context(request, {'form' : form, 'pk' : pk})
    return render_to_response('user_manage/key_edit.html', context, context_instance= RequestContext(request))

