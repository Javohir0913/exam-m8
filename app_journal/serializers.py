from rest_framework import serializers

from .models import Tags, Journal


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'tag_name')


class JournalListSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField(method_name='get_detail', read_only=True, source='detail')
    jornal_tags = TagsSerializer(many=True)

    class Meta:
        model = Journal
        fields = ('id', "jornal_name", 'jornal_logo', 'journal_description', 'jornal_tags', 'journal_file', 'detail')

    def get_detail(self, obj):
        return f"http://localhost:8000/api/journals/{obj.id}/"


class JournalDetailSerializer(serializers.ModelSerializer):
    jornal_tags = TagsSerializer(many=True)
    jornal_author = serializers.SerializerMethodField(method_name='get_jornal_author', read_only=True)

    class Meta:
        model = Journal
        fields = "__all__"
        extra_kwargs = {
            'jornal_author': {'read_only': True},
        }

    def get_jornal_author(self, obj):
        return obj.jornal_author.username
