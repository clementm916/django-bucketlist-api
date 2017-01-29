from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)
