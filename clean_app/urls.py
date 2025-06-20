from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileView, LeaderboardView, ReportViewSet, MapReportsView, CommentViewSet, RegisterView, CommentDeleteView, api_doc_view

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('reports/map/', MapReportsView.as_view(), name='map_reports'),
    path('reports/<int:report_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('register/', RegisterView.as_view(), name='register'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('', include(router.urls)),
    path('documentation/', api_doc_view, name='api-doc'),
]
