from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getTagById(request, id):
    try:
        tagObject = Tag.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Tag did exist", "Tag": tagObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Tag did not exist"}, safe=True)