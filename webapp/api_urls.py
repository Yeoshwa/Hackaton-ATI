from rest_framework.routers import DefaultRouter
from .views_event import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = router.urls
