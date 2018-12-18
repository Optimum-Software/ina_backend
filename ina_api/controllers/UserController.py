from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json

from rest_framework.authtoken.models import Token

from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import CreateUserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage


@require_http_methods(['GET'])
def getUserById(request, id):
    try:
        userObject = User.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Gebruiker bestaat", "user": userObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Gebruiker bestaat niet"}, safe=True)

@require_http_methods(['POST']) #is post because you cant put email address in url for GET request
def getUserByEmail(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if( data['email'] == ''):
            return JsonResponse({"bool": False, "msg": "Vul alle verplichte velden in aub"}, safe=True)
        try:
            userObject = User.objects.get(email=data['email']).__repr__()
            return JsonResponse({"bool": True, "msg": "Gebruiker bestaat", "user": userObject}, safe=True)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Gebruiker bestaat niet"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur alle velden mee aub"}, safe=True)


@api_view(['GET'])
def test(request):
    try:
        if request.user.is_authenticated:
            return JsonResponse({"bool": True, "msg": "YAAAAAAAY!!"}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "unauthorized"}, safe=True)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                self.perform_create(serializer)
            except IntegrityError as e:
                return JsonResponse({"bool": False, "msg": "Account bestaat al"}, safe=True)
            headers = self.get_success_headers(serializer.data)
            # We create a token than will be used for future auth

            token = Token.objects.create(user=serializer.instance)
            token_data = {"token": token.key}

            if( data['email'] == '' or
                data['password'] == '' or
                data['firstName'] == '' or
                data['lastName'] == '' or
                data['mobile'] == ''):
                return JsonResponse({"bool": False, "msg": "Vul alle verplichte velden in aub"}, safe=True)
            try:
                userObject = User(email=data['email'], password=data['password'], first_name=data['firstName'], last_name=data['lastName'], mobile=data['mobile'])
                userObject.save()
                return JsonResponse({"bool": True, "msg": "Gebruiker aangemaakt", "id": userObject.pk}, safe=True)
            except:
                return JsonResponse({"bool": False, "msg": "Kon gebruiker niet aanmaken"}, safe=True)
        except IntegrityError as e:
            return JsonResponse({"bool": False, "msg": "Kon gebruiker niet aanmaken"}, safe=True)


@require_http_methods(['PUT'])
def updateUser(request):
    data = json.loads(request.body.decode('utf8'))

    try:
        userObject = User.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "User with id [" + str(data['id']) + "] does not exist"}, safe=True)
    try:
        userObject.bio = data['bio']
        userObject.organisation = data['organisation']
        userObject.function = data['function']
        userObject.save()

        return JsonResponse({"bool": True, "msg": "User entry updated"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "User entry could not be updated"}, safe=True)

@require_http_methods(['DELETE'])
def deleteUser(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        userObject = User.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['id']) + "] bestaat niet"}, safe=True)
    try:
        userObject.delete()
        return JsonResponse({"bool": True, "msg": "Gebruiker verwijderd"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Kon gebruiker niet verwijderen"}, safe=True)

@require_http_methods(['POST'])
def uploadFileForProfilePhoto(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        userId = fieldName.split("_")[0]
        try:
            userObject = User.objects.get(pk=userId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "User bestaat niet"}, safe=True)
        fs = FileSystemStorage('./user/' + userId)
        filename = fs.save(file.name, file)
        uploadedFileUrl = ('/user/' + userId + '/' + fs.url(filename)).replace("%20", "")

        try:
            userObject.profile_photo_path = uploadedFileUrl
            userObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon profiel foto niet instellen", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Profiel foto geupload"}, safe=True)

@require_http_methods(['POST'])
def editOptionalInfo(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        userObject = User.objects.get(pk=data['userId'])
    except:
        return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
    try:
        userObject.organisation = data['organisation']
        userObject.function = data['function']
        userObject.bio = data['bio']
        userObject.save()
    except:
        return JsonResponse({"bool": False, "msg": "Kon info niet instellen"}, safe=True)
    return JsonResponse({"bool": True, "msg": "Info voor gebruiker [" + str(data['userId']) + "] ingesteld"})
