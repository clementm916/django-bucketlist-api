from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from .serializers import UserSerializer, BucketlistSerializer, ItemSerializer
from . models import Bucketlist, Item

from .utils.mixins import MultipleFieldLookupMixin, UpdateDestroyAPIView, CustomCreateAPIView


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


class BucketlistListView(generics.ListCreateAPIView):

    """
    List all bucketlists, search,or create a new bucketlist.

    """

    queryset = Bucketlist.objects.filter()
    serializer_class = BucketlistSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class BucketlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update or Delete a single bucketlist """
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    lookup_field = 'id'


class ItemsView(CustomCreateAPIView):
    """Create an item """
    serializer_class = ItemSerializer

    def get_object(self, id):
        try:
            id = int(id)
            return Bucketlist.objects.get(id=id)
        except (Bucketlist.DoesNotExist, KeyError):
            raise Http404


class ItemsDetailView(MultipleFieldLookupMixin, UpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_fields = ('bucketlist_id', 'id')
