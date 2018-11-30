from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getProjectFavoriteById(request, id):
    try:
        projectFavoriteObject = Project_Favorite.objects.get(pk=id)
        userObject = projectFavoriteObject.user.__repr__()
        projectObject = projectFavoriteObject.project.__repr__()
        projectFavoriteJson = serializers.serialize('json', [ projectFavoriteObject, ])
        return JsonResponse({"bool": True, "msg": "ProjectFavorite did exist", "projectLiked": projectFavoriteJson, "user": userObject, "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectFavorite did not exist"}, safe=True)