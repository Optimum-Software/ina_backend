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
        projectLikedJson = serializers.serialize('json', [projectLikedObject, ])
        return JsonResponse(
            {"bool": True, "msg": "ProjectLiked bestaat", "projectLiked": projectLikedJson, "user": userObject,
             "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "ProjectLiked bestaat niet"}, safe=True)


@require_http_methods(['POST'])
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

@require_http_methods(['GET'])
def checkIfProjectLiked(request, projectId, userId):
    try:
        if Project_Liked.objects.filter(project=Project.objects.get(pk=projectId), user=User.objects.get(pk=userId)).exists():
            return JsonResponse({"bool": True, "msg": "Project is al geliked door deze gebruiker", "liked": True})
        else:
            return JsonResponse({"bool": True, "msg": "Project is nog niet geliked door deze gebruiker", "liked": False})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Er ging iets mis"})

@require_http_methods(['GET'])
def getAllLikedProjectsById(request,id):
    projectList = []
    try:
        user = User.objects.get(pk=id)
        projectLikes = Project_Liked.objects.filter(user=user)
        if (projectLikes):
            for project in projectLikes:
                fileObject = File.objects.get(project=project)
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

            return JsonResponse({"bool": True, "msg": "Projects found that you liked", "projects": projectList}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "you have not like any projects"}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "failed to get your likes"}, safe=True)

@require_http_methods(['GET'])
def getLikedProjectsByUserId(request, user_id):
    try:
        userObject = User.objects.get(pk=user_id)
        likedList = Project_Liked.objects.filter(user=userObject).all()
        projectsLiked= []
        if (likedList):
            for entry in likedList:
                projectObject = entry.project.__repr__()
                projectsLiked.append(projectObject)
            return JsonResponse({"bool": True, "found": True, "msg": "Gelikedte projecten gevonden", "projects": projectsLiked})
        else:
            return JsonResponse({"bool": True, "found": True, "msg": "Je hebt geen projecten geliked"})
    except:
        return JsonResponse({"bool": False, "msg": "Kon gelikedte projecten niet ophalen"})
