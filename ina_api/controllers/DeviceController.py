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
        response = {"bool": True, "msg": "Device did exist", "device": deviceJson, "user": userObject}
    except ObjectDoesNotExist:
        response = {"bool": False, "msg": "Device did not exist"}
    return JsonResponse(response, safe=True)

@require_http_methods(["POST"])
def createDevice(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        try:
            userObject = User.objects.get(pk=data['userId'])
        except:
            return JsonResponse({"bool": False, "msg": "User with id [" + str(data['userId']) + "] did not exist"}, safe=True)
        try:
            deviceObject = Device(user=userObject, device_name=data['deviceName'])
            deviceObject.save()
            return JsonResponse({"bool": True, "msg": "Device entry created", "id": deviceObject.pk}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Could not create entry"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Please send all required fields"}, safe=True)

@require_http_methods(["DELETE"])
def deleteDeviceById(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        deviceObject = Device.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Device with id [" + str(data['id']) + "] did not exist"}, safe=True)
    try:
        deviceObject.delete()
        return JsonResponse({"bool": True, "msg": "Device entry deleted"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Device entry could not be deleted"}, safe=True)
    
    
    