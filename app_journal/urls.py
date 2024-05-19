from rest_framework import routers

from .views import TagsViewSet, JournalViewSet

router = routers.DefaultRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register('journals', JournalViewSet, basename='journals')

urlpatterns = router.urls