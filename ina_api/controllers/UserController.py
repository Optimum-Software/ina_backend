from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

@require_http_methods(['GET'])
def getUserById(request,id):
    try:
        userObject = serializers.serialize('json', [ User.objects.get(pk=id), ])
        return JsonResponse({"bool": True, "msg": "User did exist", "user": userObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "User did not exist"}, safe=True)

@api_view(['GET'])
def test(request):
    try:
        if request.user.is_authenticated:
            return JsonResponse({"bool": True, "msg": "YAAAAAAAY!!"}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "unauthorized"}, safe=True)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        