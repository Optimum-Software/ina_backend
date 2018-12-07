from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getProjectLikedById(request, id):
    try:
        projectLikedObject = Project_Liked.objects.get(pk=id)
        userObject = projectLikedObject.user.__repr__()
        projectObject = projectLikedObject.project.__repr__()
        projectLikedJson = serializers.serialize('json', [ projectLikedObject, ])
        return JsonResponse({"bool": True, "msg": "ProjectLiked bestaat", "projectLiked": projectLikedJson, "user": userObject, "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectLiked bestaat niet"}, safe=True)