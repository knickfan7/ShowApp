from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from watchlists.models import Watchlists

User._meta.get_field('email')._unique = True

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_info):
        user = User.objects.create_user(
            validated_info['username'],
            validated_info['email'],
            validated_info['password']
        )
        '''
        Watchlists.objects.create(owner=user, name='Completed')
        Watchlists.objects.create(owner=user, name="Currently Watching")
        Watchlists.objects.create(owner=user, name="Dropped")
        Watchlists.objects.create(owner=user, name="Plan to Watch")
        Watchlists.objects.create(owner=user, name="On Hold")
        '''
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials. Try Again.")