from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getGroupById(request, id):
    try:
        groupObject = Group.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Group did exist", "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Group did not exist"}, safe=True)

@require_http_methods(['GET'])
def getGroupByName(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['POST'])
def createGroup(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if( data['name'] == '' or
            data['desc'] == '' or
            data['public'] == ''):
            return JsonResponse({"bool": False, "msg": "Please fill in all required fields"}, safe=True)
        try:
            #photo_path gotten later by setGroupImg
            groupObject = Group(name=data['name'], desc=data['desc'], photo_path=[''], member_count=0, public=data['public'])
            groupObject.save()
            return JsonResponse({"bool": True, "msg": "Group entry created", "id": groupObject.pk}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Could not create entry"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Please send all required fields"}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupById(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        groupObject = Group.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Group with id [" + str(data['id']) + "] did not exist"}, safe=True)
    try:
        groupObject.delete()
        return JsonResponse({"bool": True, "msg": "Group entry deleted"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Group entry could not be deleted"}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupByName(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        groupObject = Group.objects.get(name=str(data['name']))
    except:
        return JsonResponse({"bool": False, "msg": "Group with name [" + str(data['name']) + "] did not exist"}, safe=True)
    try:
        groupObject.delete()
        return JsonResponse({"bool": True, "msg": "Group entry deleted"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Group entry could not be deleted"}, safe=True)