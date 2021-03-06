from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from moviepy.editor import *
import mimetypes
from rest_framework.decorators import api_view


@require_http_methods(['GET'])
@api_view(['GET'])
def getProjectById(request, userId, projectId):
    try:
        projectObject = Project.objects.get(pk=projectId)
        imageList = []
        fileList = []
        likedBool = False
        memberBool = False
        followedBool = False

        try:
            fileObjects = File.objects.filter(project=projectObject)
            for file in fileObjects:
                if 'image' in mimetypes.guess_type(str(file))[0]:
                    imageList.append(str(file))
                elif 'video' not in mimetypes.guess_type(str(file))[0]:
                    fileList.append(file.__repr__())

            if Project_Liked.objects.filter(project=projectObject, user=userId).exists():
                likedBool = True
            if Project_Followed.objects.filter(project=projectObject, user=userId).exists():
                followedBool = True
            if Member.objects.filter(project=projectObject, user=userId).exists():
                memberBool = True

        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})

        imageList.append(projectObject.thumbnail)

        project = projectObject.__repr__()
        project['images'] = imageList
        project['files'] = fileList
        project['liked'] = likedBool
        project['followed'] = followedBool
        project['member'] = memberBool

        return JsonResponse({"bool": True, "msg": "Project bestaat", "project": project}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)


@require_http_methods(['GET'])
def getProjectByIdNotLoggedIn(request, projectId):
    try:
        projectObject = Project.objects.get(pk=projectId)
        imageList = []
        fileList = []

        try:
            fileObjects = File.objects.filter(project=projectObject)
            for file in fileObjects:
                if 'image' in mimetypes.guess_type(str(file))[0]:
                    imageList.append(str(file))
                elif 'video' not in mimetypes.guess_type(str(file))[0]:
                    fileList.append(file.__repr__())

        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})

        project = projectObject.__repr__()
        project['images'] = imageList
        project['files'] = fileList
        project['liked'] = False
        project['followed'] = False
        project['member'] = False

        return JsonResponse({"bool": True, "msg": "Project bestaat", "project": project}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)


@require_http_methods(['POST'])
@api_view(['POST'])
def getProjects(request):
    data = json.loads(request.body.decode('utf-8'))
    filterType = data['filter']
    userId = data['userId']
    projectList = []
    try:
        projectObjects = []

        # Case: get all projects
        if filterType == 'all':
            projectObjects = Project.objects.all()

        # Case: newest projects first
        elif filterType == 'newest_first':
            projectObjects = Project.objects.order_by('created_at').all()

        # Case: oldest projects first
        elif filterType == 'oldest_first':
            projectObjects = Project.objects.order_by('-created_at').all()

        # Case: most liked projects first
        elif filterType == 'most_liked':
            projectObjects = Project.objects.order_by('-like_count').all()

        # Case: most followed projects first
        elif filterType == 'most_followed':
            projectObjects = Project.objects.order_by('-follower_count').all()

        # Case: most search for projects
        elif filterType == 'search':
            projectObjects = Project.objects.filter(name__icontains=data['searchTerm']).all()

        # Case: filter by tag
        elif filterType == 'tag':
            tagObject = Tag.objects.get(name=data['tagName'])
            allProjects = Project_Tag.objects.filter(tag=tagObject)
            for project_tag in allProjects:
                projectObjects.append(project_tag.project)

        # Case: get all projects user likes
        elif filterType == 'user_liked':
            userObject = User.objects.get(pk=userId)
            likedList = Project_Liked.objects.filter(user=userObject).all()
            for entry in likedList:
                projectObjects.append(entry.project)

        # Case: get all projects user follows
        elif filterType == 'user_followed':
            userObject = User.objects.get(pk=userId)
            projectsFollowed = Project_Followed.objects.filter(user=userObject).all()
            for entry in projectsFollowed:
                projectObjects.append(entry.project)

        # Case: get all projects user participates in
        elif filterType == 'user_member':
            userObject = User.objects.get(pk=userId)
            memberList = Member.objects.filter(user=userObject).all()
            for entry in memberList:
                projectObjects.append(entry.project)

        for project in projectObjects:
            imageList = []
            fileList = []
            likedBool = False
            memberBool = False
            followedBool = False

            try:
                fileObjects = File.objects.filter(project=project)
                for file in fileObjects:
                    if 'image' in mimetypes.guess_type(str(file))[0]:
                        imageList.append(str(file))
                    elif 'video' not in mimetypes.guess_type(str(file))[0]:
                        fileList.append(file.__repr__())

                if Project_Liked.objects.filter(project=project, user=userId).exists():
                    likedBool = True
                if Project_Followed.objects.filter(project=project, user=userId).exists():
                    followedBool = True
                if Member.objects.filter(project=project, user=userId).exists():
                    memberBool = True
                    print("member true")

            except ObjectDoesNotExist:
                return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})

            object = project.__repr__()
            object['images'] = imageList
            object['files'] = fileList
            object['liked'] = likedBool
            object['followed'] = followedBool
            object['member'] = memberBool
            projectList.append(object)

        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['POST'])
def getProjectsNotLoggedIn(request):
    data = json.loads(request.body.decode('utf-8'))
    filterType = data['filter']
    projectList = []

    try:
        projectObjects = []
        # Case: get all projects
        if filterType == 'all':
            projectObjects = Project.objects.all()

            # Case: newest projects first
        elif filterType == 'newest_first':
            projectObjects = Project.objects.order_by('created_at').all()

            # Case: oldest projects first
        elif filterType == 'oldest_first':
            projectObjects = Project.objects.order_by('-created_at').all()

            # Case: most liked projects first
        elif filterType == 'most_liked':
            projectObjects = Project.objects.order_by('-like_count').all()

            # Case: most followed projects first
        elif filterType == 'most_followed':
            projectObjects = Project.objects.order_by('-follower_count').all()

            # Case: most search for projects
        elif filterType == 'search':
            projectObjects = Project.objects.filter(name__icontains=data['searchTerm']).all()

            # Case: filter by tag
        elif filterType == 'tag':
            tagObject = Tag.objects.get(name=data['tagName'])
            allProjects = Project_Tag.objects.filter(tag=tagObject).values_list('project', flat=True)
            for id in allProjects:
                project = Project.objects.get(pk=id)
                projectObjects.append(project)

        for project in projectObjects:
            imageList = []
            fileList = []

            try:
                fileObjects = File.objects.filter(project=project)
                for file in fileObjects:
                    if 'image' in mimetypes.guess_type(str(file))[0]:
                        imageList.append(str(file))
                    elif 'video' not in mimetypes.guess_type(str(file))[0]:
                        fileList.append(file.__repr__())

            except ObjectDoesNotExist:
                return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})

            object = project.__repr__()
            object['images'] = imageList
            object['files'] = fileList
            object['liked'] = False
            object['followed'] = False
            object['member'] = False
            projectList.append(object)

        return JsonResponse({"bool": True, "msg": "Projects found", "projects": projectList}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "There a no projects"}, safe=True)


@require_http_methods(['POST'])
@api_view(['POST'])
def createProject(request):
    try:
        start_date = request.POST.get('beginDate')
        if start_date == "":
            start_date = None

        end_date = request.POST.get('endDate')
        if end_date == "":
            end_date = None

        creatorId = request.POST.get('creatorId')
        creator = User.objects.get(pk=creatorId)
        project = Project(
            name=request.POST.get('name'),
            thumbnail="",
            desc=request.POST.get('desc'),
            location=request.POST.get('location'),
            start_date=start_date,
            end_date=end_date,
            creator=creator
        )
        project.save()

        projectId = project.pk

        # save thumnail and save path in project
        thumbnail = request.FILES.get("thumbnail")
        fs = FileSystemStorage('./media/project/' + str(projectId) + "/thumbnail")
        thumbnailPath = fs.save(thumbnail.name, thumbnail)
        uploadedFileUrl = ('/project/' + str(projectId) + '/thumbnail/' + thumbnailPath)
        project.thumbnail = uploadedFileUrl
        project.save()

        try:
            memberObject = Member(user=creator, project=project)
            memberObject.save()
        except Exception as e:
            print(e)
            return JsonResponse({"bool": False, "msg": "Er ging iets fout"})

        # save all documents of project
        if len(request.FILES) > 0:
            for fieldName in request.FILES:
                try:
                    if fieldName == "thumbnail":
                        continue

                    file = request.FILES[fieldName]
                    fs = FileSystemStorage('./media/project/' + str(projectId))
                    filename = fs.save(file.name, file)

                    uploadedFileUrl = ('/project/' + str(projectId) + '/' + filename.replace("%20", ""))

                    newFile = File(project=project, path=uploadedFileUrl)

                    newFile.save()

                    if 'video' in mimetypes.guess_type(str(file))[0]:
                        clip = VideoFileClip('./media/project/' + str(projectId) + '/' + file.name)
                        clip.save_frame('./media/project/' + str(projectId) + '/videoThumbnail_' + file.name + '.jpg',
                                        t=0.00)
                        uploadedThumbnailUrl = (
                                '/project/' + str(projectId) + '/videoThumbnail_' + file.name.replace("%20",
                                                                                                      "") + '.jpg')
                        newThumbnail = File(project=project, path=uploadedThumbnailUrl)

                        newThumbnail.save()

                        uploadedFileUrl = ('/project/' + str(projectId) + '/' + filename.replace("%20", ""))

                        newFile = File(project=project, path=uploadedFileUrl)

                        newFile.save()

                except Exception as e:
                    print(e)

        # add Tags
        try:
            tags = []
            for fieldName in request.POST:
                if "#" in fieldName:
                    tags.append(request.POST.get(fieldName))
            if len(tags) > 0:
                for tag in tags:
                    if Tag.objects.filter(name=tag).exists():
                        tagObject = Tag.objects.filter(name=tag).first()
                        projectTag = Project_Tag(tag=tagObject, project=project)
                        projectTag.save()
                    else:
                        newTag = Tag(name=tag, thumbnail="")
                        newTag.save()
                        projectTag = Project_Tag(tag=newTag, project=project)
                        projectTag.save()
        except:
            print("oeps")
        return JsonResponse({"bool": True, "msg": "Project aangemaakt", "id": project.pk}, safe=True)
    except Exception as e:
        return JsonResponse({"bool": False, "msg": "Kon project niet aanmaken"}, safe=True)

@require_http_methods(['POST'])
@api_view(['POST'])
def deleteProject(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        userObject = User.objects.get(pk=data['userId'])
        projectObject = Project.objects.get(pk=data['projectId'])

        if projectObject.creator == userObject:
            projectObject.delete()
            return JsonResponse({"bool": True, "msg": "Project verwijdert", "deleted": True})
        else:
            return JsonResponse({"bool": True, "msg": "Deze gebruiker mag heeft geen rechten om dit project te verwijderen", "deleted": False})
    except Exception as e:
        print(e) 
        return JsonResponse({"bool": False, "msg": "Er is iets misgegaan met het project verwijderen"})


@require_http_methods(['POST'])
@api_view(['POST'])
def editProject(request):
    try:
        projectId = request.POST.get('projectId')

        projectObject = Project.objects.get(pk=projectId)

        name = request.POST.get('name')
        if projectObject.name != name:
            projectObject.name = name
        desc = request.POST.get('desc')
        if projectObject.desc != desc:
            projectObject.desc = desc
        location = request.POST.get('location')
        if projectObject.location != location:
            projectObject.location = location

        start_date = request.POST.get('beginDate')
        if start_date == "" or start_date == "undefined" or start_date == "null":
            start_date = None
        if projectObject.start_date != start_date:
            projectObject.start_date = start_date

        end_date = request.POST.get('endDate')
        if end_date == "" or end_date == "undefined" or end_date == "null":
            end_date = None
        if projectObject.end_date != end_date:
            projectObject.end_date = end_date
        projectObject.save()

        # update thumbnail if needed
        try:
            thumbnail = request.FILES["thumbnail"]
            fs = FileSystemStorage('./media/project/' + str(projectId) + "/thumbnail")
            filesInThumbnailDir = fs.listdir('./')[1]
            if thumbnail.name not in filesInThumbnailDir:
                fs.delete(filesInThumbnailDir[0])
                thumbnailPath = fs.save(thumbnail.name, thumbnail)
                uploadedFileUrl = ('/project/' + str(projectId) + '/thumbnail/' + thumbnailPath)
                projectObject.thumbnail = uploadedFileUrl
                projectObject.save()
                newFile = File(project=projectObject, path=uploadedFileUrl)
                newFile.save()

        except Exception as e:
            print("thumbnail error")
            print(e)

        # update other files if needed
        if len(request.FILES) > 0:
            fs = FileSystemStorage('./media/project/' + str(projectId))

            allFilesInDir = fs.listdir('./')[1]
            print(request.FILES)

            for fieldName in request.FILES:
                file = request.FILES[fieldName]
                if fieldName == "thumbnail":
                    continue
                if file.name in allFilesInDir:
                    allFilesInDir.remove(file.name)
                    continue
                savedFile = fs.save(file.name, file)
                uploadedFileUrl = ('/project/' + str(projectId) + '/' + savedFile.replace("%20", ""))
                newFile = File(project=projectObject, path=uploadedFileUrl)
                newFile.save()
                if 'video' in mimetypes.guess_type(str(file))[0]:
                    clip = VideoFileClip('./media/project/' + str(projectId) + '/' + file.name)
                    clip.save_frame('./media/project/' + str(projectId) + '/videoThumbnail_' + file.name + '.jpg',
                                    t=0.00)
                    uploadedThumbnailUrl = ('/project/' + str(projectId) + '/videoThumbnail_' + file.name.replace("%20",
                                                                                                                  "") + '.jpg')
                    newThumbnail = File(project=projectObject, path=uploadedThumbnailUrl)

                    newThumbnail.save()

                    uploadedFileUrl = ('/project/' + str(projectId) + '/' + savedFile.replace("%20", ""))

                    newFile = File(project=projectObject, path=uploadedFileUrl)

                    newFile.save()
            if len(allFilesInDir) > 0:
                for file in allFilesInDir:
                    File.objects.get(project=projectObject, path='/project/' + str(projectId) + '/' + file).delete()
                    fs.delete(file)
                    allFilesInDir.remove(file)

        # update tags if needed
        try:
            newTags = []
            oldTagList = Project_Tag.objects.values_list('tag').filter(project=projectObject)
            oldTags = []

            for oldTag in oldTagList:
                tagObject = Tag.objects.get(pk=oldTag[0])
                oldTags.append(tagObject.name)

            for fieldName in request.POST:
                if "#" in fieldName:
                    newTags.append(request.POST.get(fieldName))
            if len(newTags) > 0:
                for tag in newTags:
                    if tag in oldTags:
                        oldTags.remove(tag)
                        print("Tag is al toegevoegd aan het project")
                        continue
                    # kijk of tag al bestaat in Tag tabel
                    elif Tag.objects.filter(name=tag).exists():

                        tagObject = Tag.objects.get(name=tag)
                        if not Project_Tag.objects.filter(tag=tagObject, project=projectObject).exists():
                            projectTag = Project_Tag(tag=tagObject, project=projectObject)
                            projectTag.save()
                            oldTags.remove(tag)

                    # Als tag nog niet bestaat in tag tabel, maak de tag aan en voeg toe aan project
                    else:
                        newTag = Tag(name=tag, thumbnail="")
                        newTag.save()
                        projectTag = Project_Tag(tag=newTag, project=projectObject)
                        projectTag.save()

            if len(oldTags) > 0:
                for projectTag in oldTags:
                    tagObject = Tag.objects.filter(name=projectTag).first()
                    Project_Tag.objects.filter(tag=tagObject, project=projectObject).delete()
        except Exception as e:
            print(e)

        return JsonResponse({"bool": True, "msg": "Project succesvol aangepast", "id": projectObject.pk}, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon project niet aanpassen"}, safe=True)


@require_http_methods(['POST'])
@api_view(['POST'])
def uploadThumbnailForProject(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        projectId = fieldName.split("_")[0]
        try:
            projectObject = Project.objects.get(pk=projectId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Project bestaat niet"}, safe=True)
        fs = FileSystemStorage('./media/project/' + projectId)
        filename = fs.save(file.name, file)
        uploadedFileUrl = ('/project/' + projectId + "/" + filename).replace("%20", "")

        try:
            projectObject.thumbnail = uploadedFileUrl
            projectObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon foto niet opslaan", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Thumnail geupload"}, safe=True)


@require_http_methods(['GET'])
@api_view(['GET'])
def getSwipeProjects(request, userId):
    try:
        userObject = User.objects.get(pk=userId)
    except:
        return JsonResponse({"bool": False, "msg": "Er is geen gebruiker met id [" + str(userId) + "]"})

    try:
        # First get all projects that the user did NOT create
        allProjectList = Project.objects.exclude(creator=userObject)

        # Next filter the list on all projects for the which the user is an admin
        projectAdminList = Project_Admin.objects.filter(user=userObject)

        filteredProjectList = allProjectList
        for project in projectAdminList:
            filteredProjectList = filteredProjectList.exclude(project_admin=project)

        # Next filter the list on all projects that the user has already liked
        likeList = Project_Liked.objects.filter(user=userObject)

        secondFilterProjectList = filteredProjectList
        for project in likeList:
            secondFilterProjectList = secondFilterProjectList.exclude(project_liked=project)

        # TODO filter based on tags the user likes
        #
        #
        #
        #

        returnList = []
        for entry in secondFilterProjectList:
            imageList = []
            fileList = []
            try:
                fileObjects = File.objects.filter(project=entry)
                for file in fileObjects:
                    if 'image' in mimetypes.guess_type(str(file))[0]:
                        imageList.append(str(file))
                    elif 'video' not in mimetypes.guess_type(str(file))[0]:
                        fileList.append(file.__repr__())

                if Project_Liked.objects.filter(project=project, user=userId).exists():
                    likedBool = True
                if Project_Followed.objects.filter(project=project, user=userId).exists():
                    followedBool = True
                if Member.objects.filter(project=project, user=userId).exists():
                    memberBool = True


            except ObjectDoesNotExist:
                return JsonResponse({"bool": False, "msg": "er is iets misgegaan"})

            imageList.append(entry.thumbnail)

            object = entry.__repr__()
            object['images'] = imageList
            object['files'] = fileList
            object['liked'] = likedBool
            object['followed'] = followedBool
            object['member'] = memberBool
            returnList.append(object)
        return JsonResponse({"bool": True, "msg": "Swipe projects opgehaald", "projects": returnList})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Er is wat fout gegaan met het ophalen van projecten", "projects": []})
