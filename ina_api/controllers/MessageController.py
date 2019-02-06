from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.core import serializers
import requests
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))
json_data = open(os.path.join(BASE,'config.json'))
secretData = json.load(json_data)

@require_http_methods(["POST"])
@api_view(['POST'])
def sendMsgToUser(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if not data['group']:
            #Gets the user that recieves the noti
            try:
                userObject = User.objects.get(pk=data['userId'])
            except Exception as e:
                print(e)
                return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
        try:
            users = []
            if not data['group']:
                deviceObject = Device.objects.get(user=userObject)
                if deviceObject.canNotificate:
                    try:
                        chatObject = Chat.objects.get(pk=data['chatId'])
                        notObject = Notification(user=deviceObject.user, type=0, chat=chatObject, project=None, groupChat=None)
                        notObject.save()
                        users.append(deviceObject.device_name)
                    except Exception as e:
                        print(e)
                else:
                    return JsonResponse({"bool": False, "msg": "Gebruiker heeft notificaties uitstaan"})

            else:
                memberList = Member.objects.filter(project=Project.objects.get(pk=data['chatId'])) 
                for member in memberList:
                    deviceObject = Device.objects.get(user=member.user)
                    if deviceObject.canNotificate:
                        try:
                            projectObject = Project.objects.get(pk=data['chatId'])
                            notObject = Notification(user=deviceObject.user, type=2, chat=None, project=None, groupChat=projectObject)
                            notObject.save()
                            users.append(deviceObject.device_name)
                        except Exception as e:
                            print(e)
                            return JsonResponse({"bool": False, "msg": "Er is iets fout gegaan"})
            apiKey = secretData['ONE_SIGNAL_APIKEY']
            appId = secretData['ONE_SIGNAL_APIID']
            header = {"Content-Type": "application/json; charset=utf-8",
                  "Authorization": "Basic " + apiKey}

            payload = {"app_id": appId,
                "include_player_ids": users,
                "contents": {"en": "Je hebt nieuwe berichten"},
                "headings": {"en": "ina"},
                "data": {"type": 0}}
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))    
            return JsonResponse({"bool": True, "msg": "Bericht verstuurt"}, safe=True)
        except Exception as e:
            print(e)
            return JsonResponse({"bool": False, "msg": "Er is geen device"}, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Stuur all verplichte velden mee aub: msg"}, safe=True)