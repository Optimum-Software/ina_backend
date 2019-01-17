from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.core import serializers


@require_http_methods(['GET'])
def getProjectById(request, id):
    try:
        projectObject = Project.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Project bestaat", "project": projectObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)


@require_http_methods(['GET'])
def getAllProjects(request):
    projectList = []
    try:
        projectObjects = Project.objects.all()
        for project in projectObjects:
            fileObjectList = File.objects.filter(project=project).all()
            url = ""
            for file in fileObjectList:
                try:
                    type = file.path.split("/")[3]
                except:
                    break
                if type[0:5] == "image":
                    url = file.path
                    break

            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': url,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:

        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['GET'])
def getAllProjectsNewestFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('created_at').all()
        for project in projectObjects:
            fileObject = File.objects.get(project=project)
            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': fileObject.path,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['GET'])
def getAllProjectsOldestFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-created_at').all()
        for project in projectObjects:
            fileObject = File.objects.get(project=project)
            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': fileObject.path,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['GET'])
def getAllProjectsMostLikedFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-like_count').all()
        for project in projectObjects:
            fileObject = File.objects.get(project=project)
            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': fileObject.path,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['GET'])
def getAllProjectsMostFollowsFirst(request):
    projectList = []
    try:
        projectObjects = Project.objects.order_by('-follower_count').all()
        for project in projectObjects:
            fileObject = File.objects.get(project=project)
            projectList.append({
                'id': project.id,
                'name': project.name,
                'url': fileObject.path,
                'desc': project.desc,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'created_at': project.created_at,
                'like_count': project.like_count,
                'follower_count': project.follower_count,
                'location': project.location
            })
        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['POST'])
def createProject(request):
    try:
        start_date = request.POST.get('beginDate')
        if start_date == "":
            start_date = None

        end_date = request.POST.get('endDate')
        if end_date == "":
            end_date = None

        project = Project(
            name=request.POST.get('name'),
            thumbnail="",
            desc=request.POST.get('desc'),
            location=request.POST.get('location'),
            start_date=start_date,
            end_date=end_date
        )
        project.save()

        projectId = project.pk
        print(projectId)
        # save thumnail and save path in project
        # thumbnail = request.FILES.get("thumbnail")
        #
        # print("THUMBNAIL print")
        # print(thumbnail)
        # fs = FileSystemStorage('./media/project/' + projectId)
        # thumbnailPath = fs.save(thumbnail.name, thumbnail)
        # project.thumbnail = thumbnailPath

        # save all documents of project
        if len(request.FILES) > 0:
            for fieldName in request.FILES:
                try:
                    print(fieldName)
                    file = request.FILES[fieldName]
                    fs = FileSystemStorage('./media/project/' + projectId)
                    filename = fs.save(file.name, file)
                    uploadedFileUrl = ('/project/' + projectId + '/' + filename.replace("%20", ""))
                    newFile = File(project=projectId, path=uploadedFileUrl)
                    newFile.save()
                except Exception as e:
                    print(e)
        else:
            print("er zijn geen bestanden in request.files")
        return JsonResponse({"bool": True, "msg": "Project aangemaakt", "id": project.pk}, safe=True)
    except Exception as e:
        print("Exceptie print:")
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon project niet aanmaken"}, safe=True)
