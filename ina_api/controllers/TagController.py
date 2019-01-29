from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage

@require_http_methods(['GET'])
def getTagById(request, id):
    try:
        tagObject = Tag.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Tag bestaat", "Tag": tagObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Tag bestaat niet"}, safe=True)

@require_http_methods(['GET'])
def getAllTags(request):
    tagList = []
    try:
        tags = Tag.objects.all()
        for tag in tags:
            tagList.append(tag.__repr__())
        return JsonResponse({"bool": True, "msg": "Tags opgehaald", "tags": tagList})
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om tags op te halen"})

@require_http_methods(['GET'])
def getAllProjectTagsById(request,id):
    tagList = []
    try:
        projectObject = Project.objects.get(pk=id)
        projectTags = Project_Tag.objects.filter(project=projectObject).all()

        if (projectTags):
            for tag in projectTags:
                specificTag = Tag.objects.get(id=tag.tag_id)
                tagList.append({
                    'name': specificTag.name,
                })

            return JsonResponse({"bool": True, "msg": "Tags die bij het project horen", "tags": tagList}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "Dit project heeft geen tags"}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Het is niet gelukt om de tags op te halen"}, safe=True)

@require_http_methods(['POST'])
def uploadPictureForTag(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        tagId = fieldName
        try:
            tagObject = Tag.objects.get(pk=tagId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)
        fs = FileSystemStorage('./media/tag/' + tagId)
        filename = fs.save(file.name, file)
        uploadedFileUrl = ('/tag/' + tagId + "/" + filename).replace("%20", "")
        try:
            tagObject.thumbnail = uploadedFileUrl
            tagObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon foto niet opslaan", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Foto geupload"}, safe=True)

@require_http_methods(['POST'])
def searchForTags(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        resultList = Tag.objects.filter(name__icontains=data['searchTerm']).all()
        tags = []
        for result in resultList:
            tags.append(result.__repr__())
        return JsonResponse({"bool": True, "msg": "Zoeken is gelukt", "tags": tags})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Er is iets mis gegaan tijdens het zoeken"})