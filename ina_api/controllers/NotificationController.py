from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers

@require_http_methods(['GET'])
def getNotificationByUser(request, id):
	try:
		userObject = User.objects.get(pk=id)
		notificationList = Notification.objects.filter(user=userObject).order_by('-created_at').all()
		returnList = []
		for noti in notificationList:
			if noti.type == 0:
				returnList.append(noti.__repr__())
				#print(returnList)
			elif noti.type == 1:
				object = noti.__repr__()
				imageList = []
				fileList = []
				try:
					fileObjects = File.objects.filter(project=noti.project)
					for file in fileObjects:
						if 'image' in mimetypes.guess_type(str(file))[0]:
							imageList.append(str(file))
						elif 'video' not in mimetypes.guess_type(str(file))[0]:
							fileList.append(str(file))
				except ObjectDoesNotExist:
					return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})
				imageList.append(noti.project.thumbnail)
				object['project']['images'] = imageList
				object['project']['files'] = fileList
				returnList.append(object)
		return JsonResponse({"bool": True, "msg": "Meldingen opgehaald", "notifications": returnList})
	except Exception as e:
		print(e)
		return JsonResponse({"bool": False, "msg": "Er ging iets mis met meldingen ophalen"})

@require_http_methods(['GET'])
def markAsRead(request, id):
	try:
		notiObject = Notification.objects.get(pk=id)
		notiObject.read = True
		notiObject.save()
		return JsonResponse({"bool": True, "msg": "Gemarkeerd als gelezen"})
	except Exception as e:
		print(e)
		return JsonResponse({"bool": False, "msg": "---Er is iets mis gegaan"})
