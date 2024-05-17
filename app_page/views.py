from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet

from config.settings import EMAIL_HOST_USER
from users.permissions import IsSuperUser, IsPostOrGet
from .models import FAQ, Requirements, Contacts, Appeal
from .serializers import FAQSerializer, RequirementsSerializer, ContactsSerializer, AppealSerializer


# Create your views here.
class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save()


class RequirementsViewSet(ModelViewSet):
    queryset = Requirements.objects.all()
    serializer_class = RequirementsSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save()


class ContactsViewSet(ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [IsSuperUser]


class SendEmailMessageViewSet(ModelViewSet):
    queryset = Appeal.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = [IsPostOrGet]
    serializer_class = AppealSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_name = request.data['first_name']
        email = request.data['email']
        message = request.data['message']
        send_mail(
            subject=f'Appeal: {first_name}',
            message=f"Name: {first_name}\n"
                    f"from: {email}\n\n"
                    f"Message:\n{message}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[EMAIL_HOST_USER],
        )
        return super().create(request, *args, **kwargs)
