from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
import json
from django.core.exceptions import ObjectDoesNotExist
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['POST'])
def createChat(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user1Object = User.objects.get(pk=data['user1Id'])
    except:
        return JsonResponse({"bool": False, "msg": "gebruiker met id [" + str(data['user1Id']) + "] bestaat niet"}, safe=True)
    try:
        user2Object = User.objects.get(pk=data['user2Id'])
    except:
        return JsonResponse({"bool": False, "msg": "gebruiker met id [" + str(data['user2Id']) + "] bestaat niet"}, safe=True)
    try:
        chatObject = Chat(user1=user1Object, user2=user2Object, chat_uid=data['chatUid'])
        chatObject.save()
    except:
        JsonResponse({"bool": False, "msg": "Kon chat niet aanmaken"})

    return JsonResponse({"bool": True, "msg": "Chat aangemaakt", "chat": chatObject.__repr__()})

@require_http_methods(['GET'])
def getChatsForUser(request, id):
    try:
        userObject = User.objects.get(pk=id)
    except:
        return JsonResponse({"bool": False, "msg": "gebruiker met id [" + str(id) + "] bestaat niet"}, safe=True)

    querySet = Chat.objects.filter(user1=userObject).all() | Chat.objects.filter(user2=userObject).all()
    querySetGroupChats = Member.objects.filter(user=userObject).all()
    chatList = []
    for chat in querySet:
        chatItem = chat.__repr__()
        chatItem['group'] = False
        chatList.append(chatItem)

    for chat in querySetGroupChats:
        chatItem = chat.group.__repr__()
        chatItem['group'] = True
        chatList.append(chatItem)

    return JsonResponse({"bool": True, "msg": "chats gevonden", "chatList": chatList})