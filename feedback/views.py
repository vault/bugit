from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from forms import FeedbackForm

from common.util import get_context


def feedback_main(request, success=False):
    if request.method == 'GET':
        form = FeedbackForm()
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback', True)

    context = get_context(request, {'form':form})
    return render_to_response('feedback/feedback.html', context, context_instance=RequestContext(request))
        

