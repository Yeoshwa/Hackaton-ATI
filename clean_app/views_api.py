from rest_framework import viewsets
from clean_app.models import Report, Comment, UserProfile
from clean_app.serializers import ReportSerializer, CommentSerializer, UserProfileSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-points')
    serializer_class = UserProfileSerializer
