from rest_framework.routers import DefaultRouter
from .views_api import ReportViewSet, CommentViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')

urlpatterns = router.urls
