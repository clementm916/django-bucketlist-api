from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bucketlist, Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)


class BucketlistidField(serializers.RelatedField):
    def to_representation(self, value):
        """Returns an integer (id) field for the bucketlist_id attribute in item"""
        bucketlist_id = value.id
        return bucketlist_id


class ItemSerializer(serializers.ModelSerializer):
    """ Model serializer for the Item model"""
    bucketlist_id = BucketlistidField(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'done',
                  'date_created', 'bucketlist_id', 'date_modified')

    def create(self, validated_data):
        print("VALIDATED: ", validated_data)
        view = self.context['view']
        bucketlist_id = view.kwargs.get('id')
        add_to = {'bucketlist_id': view.get_object(bucketlist_id)}
        data = validated_data.copy()
        data.update(add_to)
        print("NEW VALIDATED: ", data)
        return Item.objects.create(**data)


class CreatedbyField(serializers.RelatedField):
    def to_representation(self, value):
        """Returns an integer (id) field for the bucketlist_id attribute in item"""
        created_by = value.id
        return created_by


class BucketlistSerializer(serializers.ModelSerializer):
    """ Model serializer for the bucketlist model"""
    items = ItemSerializer(many=True, read_only=True)
    created_by = CreatedbyField(read_only=True)

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'items', 'date_created',
                  'date_modified', 'created_by')

    def create(self, validated_data):
        request = self.context['request']
        created_by = request.user
        print(request.user)
        add_to_validated = {'created_by': created_by}
        data = validated_data.copy()
        data.update(add_to_validated)
        return Bucketlist.objects.create(**data)
