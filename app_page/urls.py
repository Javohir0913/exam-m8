from rest_framework import routers

from .views import FAQViewSet, RequirementsViewSet, ContactsViewSet, SendEmailMessageViewSet

router = routers.DefaultRouter()

router.register('faq', viewset=FAQViewSet)
router.register('requirements', viewset=RequirementsViewSet)
router.register('contacts', viewset=ContactsViewSet)
router.register('send-email', viewset=SendEmailMessageViewSet)
urlpatterns = router.urls
