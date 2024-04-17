from rest_framework import serializers
from .models import User, Message
import secrets
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    salt = serializers.CharField(read_only=True)  # Mark the salt field as read-only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'salt']

    def create(self, validated_data):

        salt = secrets.token_hex(16)
        hashed_password = make_password(validated_data['password'], salt=salt)
        validated_data['salt'] = salt
        validated_data['password'] = hashed_password
        return super().create(validated_data)
  
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        data.pop('salt', None)
        return data

class UserRetreiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'salt']



class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'content', 'created_time']