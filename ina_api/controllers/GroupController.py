from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def getGroupById(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['GET'])
def getGroupByName(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['POST'])
def createGroup(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupById(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['DELETE'])
def deleteGroupByName(request):
	return JsonResponse({}, safe=True)