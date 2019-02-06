from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getTagsByProjectId(request, id):
    tagList = []
    try:
        projectObject = Project.objects.get(pk=id)
        projectTagObject = Project_Tag.objects.filter(project=projectObject).all()
        for projectTag in projectTagObject:
            tagList.append(projectTag.tag.__repr__())

        return JsonResponse({"bool": True, "msg": "Tags gevonden voor project", "tags": tagList}, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Geen tags gevonden voor project"}, safe=True)