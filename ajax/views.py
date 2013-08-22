
from django.http import HttpResponse
from common.models import User

import json

def user_complete(request):
    letters = request.GET.get('query')
    if letters is None:
        return HttpResponse(json.dumps([]), content_type='application/json')

    users = User.objects.filter(username__contains=letters)
    users = [user.username for user in users]
    return HttpResponse(json.dumps(users), content_type='application/json')

