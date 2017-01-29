from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """ Logs in a user using username and password"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': 'Token ' + str(token.key)})


class UserRegistrationView(generics.CreateAPIView):
    """Registers a new user """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistListView(generics.CreateAPIView):
    pass


class BucketlistDetailView(generics.CreateAPIView):
    pass


class ItemsView(generics.CreateAPIView):
    pass


class ItemsDetailView(generics.CreateAPIView):
    pass
