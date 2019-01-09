from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.files.storage import FileSystemStorage

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
            projectList.append({
                'id': project.id,
                'name': project.name,
                'thumbnail': project.thumbnail,
                'creator': project.creator.__repr__(),
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


@require_http_methods(['POST'])
def uploadThumbnailForProject(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        projectId = fieldName.split("_")[0]
        try:
            projectObject = Project.objects.get(pk=projectId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)
        fs = FileSystemStorage('./media/project/' + projectId)
        filename = fs.save(file.name, file)
        uploadedFileUrl = ('/project/' + projectId + "/" + filename).replace("%20", "")

        try:
            projectObject.thumbnail = uploadedFileUrl
            projectObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon foto niet opslaan", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Thumnail geupload"}, safe=True)