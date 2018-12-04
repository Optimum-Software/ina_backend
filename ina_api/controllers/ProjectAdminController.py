from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getProjectAdminById(request, id):
    try:
        projectAdminObject = Project_Admin.objects.get(pk=id)
        userObject = projectAdminObject.user.__repr__()
        projectObject = projectAdminObject.project.__repr__()
        projectAdminJson = serializers.serialize('json', [ projectAdminObject, ])
        return JsonResponse({"bool": True, "msg": "ProjectAdmin did exist", "ProjectAdmin": projectAdminJson, "user": userObject, "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectAdmin did not exist"}, safe=True)