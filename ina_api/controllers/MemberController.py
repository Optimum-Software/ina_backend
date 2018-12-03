from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getMember(request, group_id, user_id):
    try:
        try:
            userObject = User.objects.get(pk=user_id)
        except:
            return JsonResponse({"bool": False, "msg": "User with id [" + str(data['userId']) + "] did not exist"}, safe=True)
        try:
            groupObject = Group.objects.get(pk=group_id)
        except:
            return JsonResponse({"bool": False, "msg": "Group with id [" + str(data['groupId']) + "] did not exist"}, safe=True)
        memberObject = Member.objects.filter(user=userObject, group=groupObject).first()
        userObject = memberObject.user.__repr__()
        groupObject = memberObject.group.__repr__()
        memberJson = serializers.serialize('json', [ memberObject, ])
        return JsonResponse({"bool": True, "msg": "Member did exist", "member": memberJson, "user": userObject, "group": groupObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Member did not exist"}, safe=True)
    
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
    data = json.loads(request.body.decode('utf-8'))
    try:
        try:
            userObject = User.objects.get(pk=data['userId'])
        except:
            return JsonResponse({"bool": False, "msg": "User with id [" + str(data['userId']) + "] did not exist"}, safe=True)
        try:
            groupObject = Group.objects.get(pk=data['groupId'])
        except:
            return JsonResponse({"bool": False, "msg": "Group with id [" + str(data['groupId']) + "] did not exist"}, safe=True)
        try:
            if not Member.objects.filter(user=userObject, group=groupObject).exists():
                memberObject = Member(user=userObject, group=groupObject)
                memberObject.save()
                return JsonResponse({"bool": True, "msg": "Member entry created", "id": memberObject.pk}, safe=True)
            else:
                return JsonResponse({"bool": False, "msg": "Entry allready exists"}, safe=True)
        except:
            return JsonResponse({"bool": False, "msg": "Could not create entry"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Please send all required fields"}, safe=True)

@require_http_methods(['DELETE'])
def deleteMemberById(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        memberObject = Member.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Member with id [" + str(data['id']) + "] did not exist"}, safe=True)
    try:
        memberObject.delete()
        return JsonResponse({"bool": True, "msg": "Member entry deleted"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Member entry could not be deleted"}, safe=True)