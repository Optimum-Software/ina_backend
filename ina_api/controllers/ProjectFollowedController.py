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
        userObject = User.objects.get(pk=userId)
        if Project_Followed.objects.filter(project=projectObject).exists():
            return JsonResponse({"bool": False, "msg": "Je volgt al dit project"}, safe=True)
        else:
            projectFollowed = Project_Followed(project=projectObject, user=userObject)
            projectFollowed.save()
            return JsonResponse({"bool": True, "msg": "Je volgt nu het project"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "volgen is mislukt"}, safe=True)

@require_http_methods(['GET'])
def getAllFollowedProjectsById(request,id):
    projectList = []
    try:
        user = User.objects.get(pk=id)
        projectsFollowed = Project_Followed.objects.filter(user=user)
        if (projectsFollowed):
            for project in projectsFollowed:
                fileObject = File.objects.get(project=project)
                print(project)
                projectList.append({
                    'id': project.id,
                    'name': project.name,
                    'url': fileObject.path,
                    'desc': project.desc,
                    'start_date': project.start_date,
                    'end_date': project.end_date,
                    'created_at': project.created_at,
                    'like_count': project.like_count,
                    'follower_count': project.follower_count,
                    'location': project.location
                })

            return JsonResponse({"bool": True, "msg": "Projecten die je volgt.", "projects": projectList}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "Je volgt nog geen projecten"}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Het is is niet gelukt om te volgen"}, safe=True)