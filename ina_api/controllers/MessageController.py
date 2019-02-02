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
        try:
            userObject = User.objects.get(pk=data['userId'])
        except:
            return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
        try:
            deviceObject = Device.objects.filter(user=userObject).first()
            if deviceObject.canNotificate:
                try:
                    chatObject = Chat.objects.get(pk=data['chatId'])
                    notObject = Notification(user=deviceObject.user, type=0, chat=chatObject, project=None)
                    notObject.save()
                except Exception as e:
                    print(e)
                apiKey = secretData['ONE_SIGNAL_APIKEY']
                appId = secretData['ONE_SIGNAL_APIID']
                header = {"Content-Type": "application/json; charset=utf-8",
                      "Authorization": "Basic " + apiKey}
      
                payload = {"app_id": appId,
                    "include_player_ids": [deviceObject.device_name],
                    "contents": {"en": "Je hebt nieuwe berichten"},
                    "headings": {"en": "ina"}}
                req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                return JsonResponse({"bool": True, "msg": "Bericht verstuurt"}, safe=True)
            else:
                return JsonResponse({"bool": False, "msg": "Gebruiker heeft notificaties uitstaan"})
        except:
            return JsonResponse({"bool": False, "msg": "Er is geen device"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur all verplichte velden mee aub: msg"}, safe=True)