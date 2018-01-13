from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.response import Response

from django.http import Http404

from django.contrib.auth.models import User

from .serializers import UserSerializer, BucketlistSerializer, ItemSerializer
from . models import Bucketlist, Item

from .utils.mixins import MultipleFieldLookupMixin, UpdateDestroyAPIView, CustomCreateAPIView
from .utils.pagination import BucketlistPagination


class LoginView(ObtainAuthToken, generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        """ 

        Logs in a user using username and password
        Method: POST
          Parameters:
              username (required)
              password (required)
          Response: JSON
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': 'Token ' + str(token.key)})


class UserRegistrationView(generics.CreateAPIView):
    """
    Freaking registers a new user 
    Method: POST
          Parameters:
              username (required)
              password (required)
          Response: JSON

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistListView(generics.ListCreateAPIView):

    """
    List all bucketlists, search,or create a new bucketlist.

    Method: POST
          Parameters:
              name  (required)
          Header:
              Authorization  (required)
          Response: JSON

    """

    serializer_class = BucketlistSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = BucketlistPagination

    def get(self, request, *args, **kwargs):
        """List all bucketlists or search by name.

        Method: GET
          Parameters:
              page  (optional)    default=1
              limit  (optional) 
              q      (optional) 
             

          Header:
              Authorization  (required)
          Response: JSON

        """
        search_name = request.GET.get('q', None)
        if search_name:

            search_result = Bucketlist.objects.filter(
                name__icontains=search_name)

            serializer = BucketlistSerializer(search_result, many=True)
            return Response(serializer.data)

        return self.list(request, *args, **kwargs)

    # overwite get queryset to returns bucketlists created by the user
    def get_queryset(self):

        queryset = Bucketlist.objects.filter(created_by=self.request.user)

        return queryset


class BucketlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve(GET), Update(PUT) or Delete(DELETE) a single bucketlist 

    Method: GET
          Parameters:
              id  (required)
          Header:
              Authorization  (required)
          Response: JSON

    Method: PUT
          Parameters:
              id  (required)
              name(required)
          Header:
              Authorization  (required)
          Response: JSON
    Method: DELETE
          Parameters:
              id  (required)
          Header:
              Authorization  (required)
          Response: JSON


    """

    serializer_class = BucketlistSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):

        queryset = Bucketlist.objects.filter(created_by=self.request.user)

        return queryset


class ItemsView(CustomCreateAPIView):
    """
    Create an item
    Method: POST
          Parameters:
              id  (required)
              name  (required)
              description     (optional)
              done      (optional)  
          Header:
              Authorization  (required)
          Response: JSON 

    """
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        try:
            id = int(id)
            print("USER:", user)
            return Bucketlist.objects.filter(id=id, created_by=user)[0]
        except (Bucketlist.DoesNotExist, KeyError, IndexError):
            raise Http404


class ItemsDetailView(MultipleFieldLookupMixin, UpdateDestroyAPIView):
    """
    Update (PUT) or delete (DELETE) an item
    Method: PUT
          Parameters:
              id  (required)
              bucketlist_id  (required)
              name  (optional)
              description     (optional)
              done      (optional)  
          Header:
              Authorization  (required)
          Response: JSON 


    Method: DELETE
          Parameters:
              id  (required)
              bucketlist_id  (required)
          Header:
              Authorization  (required)
          Response: JSON 

    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_fields = ('bucketlist_id', 'id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
