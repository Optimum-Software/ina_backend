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
            return JsonResponse({"bool": False, "msg": "Project met id [" + str(data['project']) + "] bestaat niet"})

        if data['title'] == '' or data['content'] == '':
            return JsonResponse({"bool": False, "msg": "Update moet een title en inhoud bevatten"})

        updateObject = Project_Update(project=projectObject, creator=userObject, title=data['title'], content=data['content'])
        updateObject.save()

        memberList = Member.objects.filter(project=projectObject).values_list('user', flat=True)
        followerList = Project_Followed.objects.filter(project=projectObject)
        deviceList = []
        if memberList.exists():
            for id in memberList:
                deviceObject = Device.objects.get(user=id)
                if deviceObject.canNotificate:
                    deviceList.append(deviceObject.device_name)
                    try:
                        notObject = Notification(user=deviceObject.user, type=1, chat=None, project=projectObject)
                        notObject.save()
                    except Exception as e:
                        print(e)
        if followerList.exists():
            for entry in followerList:
                deviceObject = Device.objects.get(user=entry.user)
                if deviceObject.canNotificate:
                    #check if the user wasn't already a member
                    unique = True
                    for deviceName in deviceList:
                        if deviceName == deviceObject.device_name:
                            unique = False
                            break
                    if unique:
                        if entry.canNotificate:
                            print("can send Notification")
                            deviceList.append(deviceObject.device_name)
                            try:
                                notObject = Notification(user=deviceObject.user, type=1, chat=None, project=projectObject)
                                notObject.save()
                            except Exception as e:
                                print(e)
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

@require_http_methods(['GET'])
def getProjectUpdatesByProjectId(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        updateList = Project_Update.objects.filter(project=project).order_by('-created_at').all()
        returnList = []
        for update in updateList:
            returnList.append(update.__repr__())
        return JsonResponse({"bool": True, "msg": "Updates voor project opgehaald", "updates": returnList})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon geen project updates ophalen"})