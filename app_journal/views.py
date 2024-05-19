from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwnerOrSuperUser, IsSuperUser
from .models import Tags, Journal
from .serializers import TagsSerializer, JournalDetailSerializer, JournalListSerializer


# Create your views here.
class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save()


class JournalViewSet(ModelViewSet):
    queryset = Journal.objects.all()
    permission_classes = [IsSuperUser]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3

    def get_serializer_class(self):
        if self.action == 'list':
            return JournalListSerializer
        return JournalDetailSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(jornal_author=self.request.user)
        return serializer.save()

