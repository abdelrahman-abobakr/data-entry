from rest_framework.routers import DefaultRouter
from .views import EntryViewSet

router = DefaultRouter()
router.register(r'entry', EntryViewSet, basename='entry')

urlpatterns = router.urls