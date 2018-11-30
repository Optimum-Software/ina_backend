from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getMember(request, group_id, user_id):
	return JsonResponse({}, safe=True)
	
def getMemberById(request, id):
    try:
        memberObject = Member.objects.get(pk=id)
        userObject = memberObject.user.__repr__()
        groupObject = memberObject.group.__repr__()
        memberJson = serializers.serialize('json', [ memberObject, ])
        return JsonResponse({"bool": True, "msg": "Member did exist", "member": memberJson, "user": userObject, "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Member did not exist"}, safe=True)

@require_http_methods(['POST'])
def createMember(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['DELETE'])
def deleteMember(request):
    return JsonResponse({}, safe=True)