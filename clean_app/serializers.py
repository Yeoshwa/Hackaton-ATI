from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Report, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'statut', 'points']

class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Report
        fields = ['id', 'user', 'latitude', 'longitude', 'photo', 'description', 'statut', 'gravite', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'report', 'content', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
