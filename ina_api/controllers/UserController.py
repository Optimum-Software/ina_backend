from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getUserById(request,id):
    try:
        userObject = serializers.serialize('json', [ User.objects.get(pk=id), ])
        return JsonResponse({"bool": True, "msg": "User did exist", "user": userObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "User did not exist"}, safe=True)