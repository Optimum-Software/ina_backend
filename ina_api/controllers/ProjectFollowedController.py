from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getProjectFollowedById(request, id):
    try:
        projectFollowedObject = Project_Followed.objects.get(pk=id)
        userObject = projectFollowedObject.user.__repr__()
        projectObject = projectFollowedObject.project.__repr__()
        projectFollowedJson = serializers.serialize('json', [ projectFollowedObject, ])
        return JsonResponse({"bool": True, "msg": "ProjectFollowed bestaat", "projectFollowed": projectFollowedJson, "user": userObject, "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectFollowed bestaat niet"}, safe=True)

@require_http_methods(['POST'])
def followProjectById(request):
    data = json.loads(request.body.decode('utf8'))
    projectId = data['id']
    userId = data['userId']

    try:
        projectObject = Project.objects.get(pk=projectId)
        userObject = Project.objects.get(pk=userId)
        projectFollowed = Project_Followed(project=projectObject.name, user=userObject)
        projectFollowed.save()
        return JsonResponse({"bool": True, "msg": "Je volgt nu het project"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "volgen is mislukt"}, safe=True)
