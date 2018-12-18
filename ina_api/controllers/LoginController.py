from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from ina_api.models import *
from ..serializers import CreateUserSerializer
import json
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import IntegrityError


class LoginUser(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"bool": True, "msg": "User successfully logged in",
                                 "token": token.key,
                                 "userId": user.id}, safe=True)
        else:
            return JsonResponse({"bool": False, "msg": "User credentials not valid", }, safe=True)


class LogoutUser(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
