from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests

@require_http_methods(["POST"])
def sendMsgToUser(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        try:
            userObject = User.objects.get(pk=data['userId'])
        except:
            return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
        try:
            print(userObject.id)
            deviceObject = Device.objects.filter(user=userObject).first()
            apiKey = "NjBmM2NhY2MtOTcyNi00OGNkLWI2NWUtMWM0ZTEwY2U0YmZj"
            appId = "33abe35a-5325-45cc-bbee-074d6cc1d558"
            header = {"Content-Type": "application/json; charset=utf-8",
                      "Authorization": "Basic " + apiKey}
      
            payload = {"app_id": appId,
               "include_player_ids": [deviceObject.device_name],
               "contents": {"en": "Je hebt nieuwe berichten"},
               "headings": {"en": "ina"}}
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            return JsonResponse({"bool": True, "msg": "Bericht verstuurt"}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Er is geen device"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur all verplichte velden mee aub: msg"}, safe=True)