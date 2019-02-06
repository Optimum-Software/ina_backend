from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import mimetypes


@require_http_methods(['POST'])
@api_view(['POST'])
def likeProjectById(request):
    data = json.loads(request.body.decode('utf8'))
    projectId = data['id']
    userId = data['userId']
    try:
        projectObject = Project.objects.get(pk=projectId)
        if Project_Liked.objects.filter(project=projectObject).exists():
            return JsonResponse({"bool": False, "msg": "Je hebt het project al een like gegeven"})
        else:
            userObject = User.objects.get(pk=userId)
            projectLiked = Project_Liked(project=projectObject, user=userObject)
            projectLiked.save()
            projectObject.like_count += 1
            projectObject.save()
            likedCount = projectObject.like_count
            return JsonResponse({"bool": True, "msg": "Like is toegevoegd", "likedCount": likedCount})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om te liken"})


@require_http_methods(['POST'])
@api_view(['POST'])
def unlikeProjectById(request):
    data = json.loads(request.body.decode('utf8'))
    projectId = data['id']
    userId = data['userId']
    try:
        projectObject = Project.objects.get(pk=projectId)
        userObject = User.objects.get(pk=userId)
        if Project_Liked.objects.filter(project=projectObject).exists():
            Project_Liked.objects.get(project=projectObject, user=userObject).delete()
            projectObject.like_count -= 1
            projectObject.save()
            likedCount = projectObject.like_count
            return JsonResponse({"bool": True, "msg": "Project succesvol geunliked", "likedCount": likedCount})
        else:
            return JsonResponse({"bool": True, "msg": "Je hebt het project nog niet geliked"})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om te unliken"})



@require_http_methods(['GET'])
@api_view(['GET'])
def checkIfProjectLiked(request, projectId, userId):
    try:
        if Project_Liked.objects.filter(project=Project.objects.get(pk=projectId), user=User.objects.get(pk=userId)).exists():
            return JsonResponse({"bool": True, "msg": "Project is al geliked door deze gebruiker", "liked": True})
        else:
            return JsonResponse({"bool": True, "msg": "Project is nog niet geliked door deze gebruiker", "liked": False})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Er ging iets mis"})
