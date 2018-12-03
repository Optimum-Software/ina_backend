from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getFileById(request, id):
    try:
        fileObject = File.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "File did exist", "file": fileObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "File did not exist"}, safe=True)