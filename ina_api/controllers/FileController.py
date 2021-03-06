from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.core import serializers
from django.core.files.storage import FileSystemStorage

@require_http_methods(['GET'])
def getFileById(request, id):
    try:
        fileObject = File.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "File bestaat", "file": fileObject}, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "File bestaat niet"}, safe=True)

@require_http_methods(['POST'])
@api_view(['POST'])
def uploadFileForProject(request):
	for fieldName in request.FILES:
		file = request.FILES[fieldName]
		projectId = fieldName.split("_")[0]
		try:
			projectObject = Project.objects.get(pk=projectId)
		except ObjectDoesNotExist:
			return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)
		fs = FileSystemStorage('./media/project/' + projectId)
		filename = fs.save(file.name, file)
		uploadedFileUrl = ('/project/' + projectId + fs.url(filename)).replace("%20", "")

		try:
			fileObject = File(project = projectObject, path = uploadedFileUrl)
			fileObject.save()
		except:
			return JsonResponse({"bool": False, "msg": "Kon File object niet aanmaken", "file": filename}, safe=True)
	return JsonResponse({"bool": True, "msg": "Files geupload"}, safe=True)
