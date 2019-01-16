from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))
json_data = open(os.path.join(BASE,'config.json'))
secretData = json.load(json_data)

@require_http_methods(['GET'])
def getUpdateById(request, id):
    try:
        updateObject = ProjectUpdate.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Update bestaat", "user": updateObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Update bestaat niet"}, safe=True)

@require_http_methods(['POST'])
def addUpdate(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            userObject = User.objects.get(pk=data['user'])
        except:
            return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['user']) + "] bestaat niet"})

        try:
            projectObject = Project.objects.get(pk=data['project'])
        except:
            return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['user']) + "] bestaat niet"})

        if data['title'] == '' or data['content'] == '':
            return JsonResponse({"bool": False, "msg": "Update moet een title en inhoud bevatten"})

        updateObject = Project_Update(project=projectObject, creator=userObject, title=data['title'], content=data['content'])
        updateObject.save()

        memberList = Member.objects.filter(project=projectObject).values_list('user', flat=True)
        deviceList = []
        for id in memberList:
            deviceList.append(Device.objects.get(user=id).device_name)     
        apiKey = secretData['ONE_SIGNAL_APIKEY']
        appId = secretData['ONE_SIGNAL_APIID']
        header = {"Content-Type": "application/json; charset=utf-8",
                  "Authorization": "Basic " + apiKey}
  
        payload = {"app_id": appId,
           "include_player_ids": deviceList,
           "contents": {"en": "Er is een update voor project: " + projectObject.name},
           "headings": {"en": "ina"}}
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

        return JsonResponse({"bool": True, "msg": "update aangemaakt", "projectUpdate": updateObject.pk})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon update niet aanmaken"})