from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.core import serializers
import mimetypes

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
@api_view(['POST'])
def followProjectById(request):
    data = json.loads(request.body.decode('utf8'))
    projectId = data['id']
    userId = data['userId']
    try:
        projectObject = Project.objects.get(pk=projectId)
        userObject = User.objects.get(pk=userId)
        if Project_Followed.objects.filter(project=projectObject).exists():
            return JsonResponse({"bool": False, "msg": "Je volgt al dit project"}, safe=True)
        else:
            projectFollowed = Project_Followed(project=projectObject, user=userObject)
            projectFollowed.save()
            projectObject.follower_count += 1
            projectObject.save()
            followerCount = projectObject.follower_count
            return JsonResponse({"bool": True, "msg": "Je volgt nu het project", "followerCount": followerCount}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "volgen is mislukt"}, safe=True)


@require_http_methods(['GET'])
@api_view(['GET'])
def checkIfFollowed(request, userId, projectId):
    try:
        try:
            object = Project_Followed.objects.get(user=User.objects.get(pk=userId), project=Project.objects.get(pk=projectId))
            return JsonResponse({"bool": True, "msg": "Deze gebruiker volgt dit project wel", "followed": True, "canNotificate": object.canNotificate})
        except ObjectDoesNotExist:
            return JsonResponse({"bool": True, "msg": "Deze gebruiker volgt dit project niet", "followed": False})
    except:
        return JsonResponse({"bool": False, "msg": "Er is iets misgegaan"})

@require_http_methods(['POST'])
@api_view(['POST'])
def setCanNotificate(request):
    data = json.loads(request.body.decode('utf8'))
    try:
        projectFollowedObject = Project_Followed.objects.get(user=User.objects.get(pk=data['userId']), project=Project.objects.get(pk=data['projectId']))
        projectFollowedObject.canNotificate = data['canNotificate']
        projectFollowedObject.save()
        return JsonResponse({"bool": True, "msg": "Notificatie instellingen aangepast"})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon notificatie niet instellen"})


@require_http_methods(['GET'])
@api_view(['GET'])
def checkIfProjectFollowed(request, projectId, userId):
    try:
        if Project_Followed.objects.filter(project=Project.objects.get(pk=projectId), user=User.objects.get(pk=userId)).exists():
            return JsonResponse({"bool": True, "msg": "Project wordt al gevolgd door deze gebruiker", "followed": True})
        else:
            return JsonResponse({"bool": True, "msg": "Project wordt nog niet gevolgd door deze gebruiker", "followed": False})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Er ging iets mis"})


@require_http_methods(['POST'])
@api_view(['POST'])
def unfollowProjectById(request):
    data = json.loads(request.body.decode('utf8'))
    projectId = data['id']
    userId = data['userId']
    try:
        projectObject = Project.objects.get(pk=projectId)
        userObject = User.objects.get(pk=userId)
        if Project_Followed.objects.filter(project=projectObject).exists():
            Project_Followed.objects.get(project=projectObject, user=userObject).delete()
            projectObject.follower_count -= 1
            projectObject.save()
            follower_count = projectObject.follower_count
            return JsonResponse({"bool": True, "msg": "Project succesvol ontvolgd", "followerCount": follower_count})
        else:
            return JsonResponse({"bool": True, "msg": "Je volgt het project nog niet"})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om te ontvolgen"})

