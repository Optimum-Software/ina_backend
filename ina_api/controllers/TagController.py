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
        return JsonResponse({"bool": True, "msg": "Tag bestaat", "Tag": tagObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Tag bestaat niet"}, safe=True)

@require_http_methods(['GET'])
def getAllProjectTagsById(request,id):
    tagList = []
    try:
        projectObject = Project.objects.get(pk=id)
        projectTags = Project_Tag.objects.filter(project=id).all()
        if (projectTags):
            for tag in projectTags:
                tagList.append({
                    'name': tag,
                })

            return JsonResponse({"bool": True, "msg": "Tags die bij project horen", "projects": tagList}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "Dit project heeft geen tags"}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om de tags op te halen"}, safe=True)