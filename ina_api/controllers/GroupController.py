from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@require_http_methods(['GET'])
def getGroupById(request, id):
    try:
        groupObject = Group.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Groep bestaat", "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Group bestaat niet"}, safe=True)

@require_http_methods(['GET'])
def getGroupByName(request, group_name):
    try:
        groupObject = Group.objects.get(name=group_name).__repr__()
        return JsonResponse({"bool": True, "msg": "Groep bestaat", "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Group bestaat niet"}, safe=True)

@require_http_methods(['POST'])
def createGroup(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if( data['name'] == '' or
            data['desc'] == '' or
            data['public'] == ''):
            return JsonResponse({"bool": False, "msg": "Vul alle verplichte velden in aub"}, safe=True)
        try:
            #photo_path gotten later by setGroupImg
            groupObject = Group(name=data['name'], desc=data['desc'], photo_path=[''], member_count=0, public=data['public'])
            groupObject.save()
            return JsonResponse({"bool": True, "msg": "Groep aangemaakt", "id": groupObject.pk}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Kon groep niet aanmaken"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur alle verplichte velden in aub"}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupById(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        groupObject = Group.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Groep met id [" + str(data['id']) + "] bestaat niet"}, safe=True)
    try:
        groupObject.delete()
        return JsonResponse({"bool": True, "msg": "Groep verwijderd"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Kon groep niet verwijderen"}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupByName(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        groupObject = Group.objects.get(name=str(data['name']))
    except:
        return JsonResponse({"bool": False, "msg": "Groep met id [" + str(data['id']) + "] bestaat niet"}, safe=True)
    try:
        groupObject.delete()
        return JsonResponse({"bool": True, "msg": "Groep verwijderd"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Kon groep niet verwijderen"}, safe=True)

@require_http_methods(['POST'])
def uploadGroupPhoto(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        groupId = fieldName.split("_")[0]
        try:
            groupObject = Group.objects.get(pk=groupId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Groep bestaat niet"}, safe=True)
        fs = FileSystemStorage('./media/group/' + groupId)
        filename = fs.save(file.name, file)
        print(filename)
        uploadedFileUrl = ('/group/' + groupId + "/" + (filename).replace("%20", ""))
        print(uploadedFileUrl)
        try:
            groupObject.photo_path = uploadedFileUrl
            groupObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon groeps foto niet instellen", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Groeps foto geupload"}, safe=True)