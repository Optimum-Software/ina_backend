from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getGroupAdminById(request, id):
    try:
        groupAdminObject = Group_Admin.objects.get(pk=id)
        userObject = groupAdminObject.user.__repr__()
        groupObject = groupAdminObject.group.__repr__()
        groupAdminJson = serializers.serialize('json', [ groupAdminObject, ])
        return JsonResponse({"bool": True, "msg": "GroupAdmin bestaat", "groupAdmin": groupAdminJson, "user": userObject, "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "GroupAdmin bestaat niet"}, safe=True)