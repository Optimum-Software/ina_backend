from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getProjectById(request, id):
    try:
        projectObject = Project.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Project bestaat", "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)

@require_http_methods(['GET'])
def getAllProjects(request):
    projectList = []
    try:
        projectObjects = Project.objects.all()
        for project in projectObjects:
            fileObjectList = File.objects.filter(project=project).all()
            url = ""
            for file in fileObjectList:
                try:
                    type = file.path.split("/")[3]
                except:
                    break
                if type[0:5] == "image":
                    url = file.path
                    break

            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': url,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:

        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)

@require_http_methods(['GET'])
def getAllProjectsNewestFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('created_at').all()
        for project in projectObjects:
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
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)

@require_http_methods(['GET'])
def getAllProjectsOldestFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-created_at').all()
        for project in projectObjects:
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
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)

@require_http_methods(['GET'])
def getAllProjectsMostLikedFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-like_count').all()
        for project in projectObjects:
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
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)

@require_http_methods(['GET'])
def getAllProjectsMostFollowsFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-follower_count').all()
        for project in projectObjects:
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
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)
