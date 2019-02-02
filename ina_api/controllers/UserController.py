from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.authtoken.models import Token
from ina_api.models import *
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import CreateUserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage


@require_http_methods(['GET'])
def getUserById(request, id):
    try:
        userObject = User.objects.get(pk=id).__repr__()
        return JsonResponse({"bool": True, "msg": "Gebruiker bestaat", "user": userObject}, safe=True)
    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Gebruiker bestaat niet"}, safe=True)


@require_http_methods(['POST'])  # is post because you cant put email address in url for GET request
def getUserByEmail(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if (data['email'] == ''):
            return JsonResponse({"bool": False, "msg": "Vul alle verplichte velden in aub"}, safe=True)
        try:
            userObject = User.objects.get(email=data['email']).__repr__()
            return JsonResponse({"bool": True, "msg": "Gebruiker bestaat", "user": userObject}, safe=True)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "Gebruiker bestaat niet"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Stuur alle velden mee aub"}, safe=True)

@require_http_methods(['GET'])
@api_view(['GET'])
def getUserSettings(request, id):
    try:
        userObject = User.objects.get(pk=id)

        #canNotificate
        canNotificate = Device.objects.get(user=userObject).canNotificate
        settingsData = {
            'canNotificate': canNotificate
        }
        return JsonResponse({"bool": True, "msg": "Instellingen opgehaald", "settings": settingsData})
    except:
        return JsonResponse({"bool": False, "msg": "Er ging wat mis met het ophalen van deze instellingen"})

@require_http_methods(['POST'])
@api_view(['POST'])
def saveUserSettings(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        userObject = User.objects.get(pk=data['userId'])

        #canNotificate
        deviceObject = Device.objects.get(user=userObject)
        deviceObject.canNotificate = data['canNotificate']
        deviceObject.save()

        return JsonResponse({"bool": True, "msg": "Instellingen opgeslagen"})
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon de instellingen niet opslaan"})


@require_http_methods(['POST'])
def sendPasswordVerification(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        if User.objects.filter(email=data['email']).exists():

            user = User.objects.get(email=data['email'])
            code = generateVerificationCode()
            user.passwordVerification = code
            user.save()

            sendEmail(data['email'], code)

            return JsonResponse({"bool": True, "msg": "E-mail met verificatie is verzonden"}, safe=True)

    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "msg": "Gebruiker bestaat niet"}, safe=True)


def sendEmail(email, code):
    subject = 'Wachtwoord veranderen INA'
    message = 'De verificatie code om uw wachtwoord te veranderen is: ' + code
    email_from = settings.EMAIL_HOST_USER
    target = [email]
    send_mail(subject, message, email_from, target, fail_silently=False)


def generateVerificationCode():
    code = get_random_string(length=6)
    return code


@require_http_methods(['POST'])
def changePassword(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(email=data['email'])
        if user.passwordVerification == data['code']:
            user.passwordVerification = None
            user.password = data['newPassword']
            user.save()
            return JsonResponse({"bool": True, "msg": "Wachtwoord succesvol veranderd!"}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "Verificatie code is onjuist"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Er is iets misgegaan"}, safe=True)

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

            if (data['email'] == '' or
                    data['password'] == '' or
                    data['firstName'] == '' or
                    data['lastName'] == '' or
                    data['mobile'] == ''):
                return JsonResponse({"bool": False, "msg": "Vul alle verplichte velden in aub"}, safe=True)
            try:
                userObject = User(email=data['email'], password=data['password'], first_name=data['firstName'],
                                  last_name=data['lastName'], mobile=data['mobile'])
                userObject.save()
                return JsonResponse({"bool": True, "msg": "Gebruiker aangemaakt", "id": userObject.pk}, safe=True)
            except:
                return JsonResponse({"bool": False, "msg": "Kon gebruiker niet aanmaken"}, safe=True)
        except IntegrityError as e:
            return JsonResponse({"bool": False, "msg": "Kon gebruiker niet aanmaken"}, safe=True)


@require_http_methods(['POST'])
@api_view(['POST'])
def updateUser(request):
    try:
        userObject = User.objects.get(pk=request.POST.get('id'))
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(request.POST.get('id')) + "] bestaat niet"}, safe=True)
    try:
        if request.POST.get('firstName') != '':
            userObject.first_name = request.POST.get('firstName')
            userObject.save()
        if request.POST.get('lastName') != '':
            userObject.last_name = request.POST.get('lastName')
            userObject.save()
        if request.POST.get('bio') != '':
            userObject.bio = request.POST.get('bio')
            userObject.save()
        if request.POST.get('organisation') != '':
            userObject.organisation = request.POST.get('organisation')
            userObject.save()
        if request.POST.get('function') != '':
            userObject.function = request.POST.get('function')
            userObject.save()
        if len(request.FILES) > 0:
            for fieldName in request.FILES:
                file = request.FILES[fieldName]
                fs = FileSystemStorage('./media/user/' + request.POST.get('id'))
                filename = fs.save(file.name, file)

                uploadedFileUrl = ('/user/' + request.POST.get('id') + '/' + (filename).replace("%20", ""))

                try:
                    userObject.profile_photo_path = uploadedFileUrl
                    userObject.save()
                except:
                    return JsonResponse({"bool": False, "msg": "Kon profiel foto niet aanpassen", "file": filename}, safe=True)
        return JsonResponse({"bool": True, "msg": "Gebruiker aangepast"}, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon gebruiker niet aanpassen"}, safe=True)


@require_http_methods(['DELETE'])
@api_view(['DELETE'])
def deleteUser(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        userObject = User.objects.get(pk=data['id'])
    except:
        return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['id']) + "] bestaat niet"},
                            safe=True)
    try:
        userObject.delete()
        return JsonResponse({"bool": True, "msg": "Gebruiker verwijderd"}, safe=True)
    except:
        return JsonResponse({"bool": False, "msg": "Kon gebruiker niet verwijderen"}, safe=True)

@require_http_methods(['POST'])
@api_view(['POST'])
def uploadFileForProfilePhoto(request):
    for fieldName in request.FILES:
        file = request.FILES[fieldName]
        userId = fieldName.split("_")[0]
        try:
            userObject = User.objects.get(pk=userId)
        except ObjectDoesNotExist:
            return JsonResponse({"bool": False, "msg": "User bestaat niet"}, safe=True)
        fs = FileSystemStorage('./media/user/' + userId)
        filename = fs.save(file.name, file)
        uploadedFileUrl = ('/user/' + userId + '/' + (filename).replace("%20", ""))

        try:
            userObject.profile_photo_path = uploadedFileUrl
            userObject.save()
        except:
            return JsonResponse({"bool": False, "msg": "Kon profiel foto niet instellen", "file": filename}, safe=True)
    return JsonResponse({"bool": True, "msg": "Profiel foto geupload"}, safe=True)

@require_http_methods(['POST'])
@api_view(['POST'])
def editOptionalInfo(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        userObject = User.objects.get(pk=data['userId'])
    except:
        return JsonResponse({"bool": False, "msg": "Gebruiker met id [" + str(data['userId']) + "] bestaat niet"}, safe=True)
    try:
        print(data)
        userObject.organisation = data['organisation']
        userObject.function = data['function']
        userObject.bio = data['bio']
        userObject.save()
    except Exception as e:
        print(e)
        return JsonResponse({"bool": False, "msg": "Kon info niet instellen"}, safe=True)
    return JsonResponse({"bool": True, "msg": "Info voor gebruiker [" + str(data['userId']) + "] ingesteld"})
