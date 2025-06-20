from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import UserProfile, Report, Comment
from .serializers import UserProfileSerializer, ReportSerializer, CommentSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend

# Liste et détail profil utilisateur connecté
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

# Classement utilisateurs par points
class LeaderboardView(generics.ListAPIView):
    queryset = UserProfile.objects.order_by('-points')[:10]
    serializer_class = UserProfileSerializer

# Signalements
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    filterset_fields = ['statut', 'gravite']
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        report = serializer.save(user=user)
        if user:
            profile = user.userprofile
            profile.points += 5  # Par exemple, 5 points par report
            profile.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        # Consultation et création accessibles à tous
        return []

# Endpoint pour afficher signalements léger pour carte
class MapReportsView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request):
        reports = Report.objects.all()
        data = [
            {
                'id': report.id,
                'latitude': report.latitude,
                'longitude': report.longitude,
                'statut': report.statut
            } for report in reports
        ]
        return Response(data)

# Commentaires
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []  # Autorise tout le monde à lire
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        report_id = self.kwargs['report_id']
        return Comment.objects.filter(report__id=report_id).order_by('-created_at')

    def perform_create(self, serializer):
        report_id = self.kwargs['report_id']
        report = Report.objects.get(id=report_id)
        comment = serializer.save(user=self.request.user, report=report)
        profile = self.request.user.userprofile
        profile.points += 2  # Par exemple, 2 points par commentaire
        profile.save()

class RegisterView(APIView):
    permission_classes = []  # Ou AllowAny

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

def api_doc_view(request):
    return render(request, 'clean_app/api_doc.html')

