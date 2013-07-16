from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from forms import FeedbackForm

from common.util import get_context


def feedback_main(request):
    success = False
    if 'success' in request.GET:
        success = True

    if request.method == 'GET':
        form = FeedbackForm()
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sender = request.user
            feedback.save()
            furl = reverse('feedback') + '?success=1'
            return HttpResponseRedirect(furl)

    context = get_context(request, {'form':form, 'success':success})
    return render_to_response('feedback/feedback.html', context, context_instance=RequestContext(request))
        

