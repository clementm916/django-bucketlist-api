from rest_framework import mixins
from rest_framework import generics

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status


class MultipleFieldLookupMixin(object):
    """Allows multiple field lookups in a view"""

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)


class UpdateDestroyAPIView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    """
    Concrete view for  updating or deleting a model instance.
    """

    def put(self, request, *args, **kwargs):
        """Updates an Item"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Deletes an Item"""
        return self.destroy(request, *args, **kwargs)


class CustomCreateAPIView(generics.CreateAPIView):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        self.perform_create(serializer)
        # except:
        # return Response({'detail': 'Provided name taken by an item in the
        # same bucketlist!'}, status=status.HTTP_409_CONFLICT)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
