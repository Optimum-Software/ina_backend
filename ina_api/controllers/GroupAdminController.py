from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *

@require_http_methods(['GET'])
def getGroupAdminById(request):
    return JsonResponse({}, safe=True)