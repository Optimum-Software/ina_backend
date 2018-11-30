from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getProjectTagById(request, id):
    try:
        projectTagObject = Project_Tag.objects.get(pk=id)
        tabObject = projectTagObject.tag.__repr__()
        projectObject = projectTagObject.project.__repr__()
        projectTagJson = serializers.serialize('json', [ projectTagObject, ])
        return JsonResponse({"bool": True, "msg": "ProjectTag did exist", "projectTag": projectTagJson, "tag": tabObject, "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectTag did not exist"}, safe=True)