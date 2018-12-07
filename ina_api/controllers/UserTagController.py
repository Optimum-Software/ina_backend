from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getUserTagById(request,id):
    try:
        userTagObject = User_Tag.objects.get(pk=id)
        tagObject = userTagObject.tag.__repr__()
        userObject = userTagObject.user.__repr__()
        userTagjson = serializers.serialize('json', [ userTagObject, ])
        return JsonResponse({"bool": True, "msg": "Usertag bestaat", "userTag": userTagjson, "tag": tagObject, "user": userObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "UserTag bestaat niet"}, safe=True)