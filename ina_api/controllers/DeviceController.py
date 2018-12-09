from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(["GET"])
def getDeviceById(request, id):
    response = {}
    try:
        deviceObject = Device.objects.get(pk=id)
        userObject = deviceObject.user.__repr__()
        deviceJson = serializers.serialize('json', [ deviceObject, ])
        response = {"bool": True, "msg": "Device bestaat", "device": deviceJson, "user": userObject}
    except ObjectDoesNotExist:
        response = {"bool": False, "msg": "Device bestaat niet"}
    return JsonResponse(response, safe=True)

@require_http_methods(["POST"])
def createDevice(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        try:
            userObject = User.objects.get(pk=data['userId'])
        except:
            return JsonResponse({"bool": False, "msg": "gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
        try:
            deviceObject = Device(user=userObject, device_name=data['deviceName'])
            deviceObject.save()
            return JsonResponse({"bool": True, "msg": "Device aangemaakt", "id": deviceObject.pk}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Kon Device niet aanmaken"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur all verplichte velden mee aub"}, safe=True)

@require_http_methods(["DELETE"])
def deleteDeviceById(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        deviceObject = Device.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Device met id [" + str(data['id']) + "] bestaat niet"}, safe=True)
    try:
        deviceObject.delete()
        return JsonResponse({"bool": True, "msg": "Device verwijderd"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Kon Device niet verwijderen"}, safe=True)
    
    
    