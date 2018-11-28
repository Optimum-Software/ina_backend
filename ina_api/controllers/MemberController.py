from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *

@require_http_methods(['GET'])
def getMember(request):
    return JsonResponse({}, safe=True)@require_http_methods(['GET'])

@require_http_methods(['POST'])
def createMember(request):
    return JsonResponse({}, safe=True)

@require_http_methods(['DELETE'])
def deleteMember(request):
    return JsonResponse({}, safe=True)