from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from .models import Transcript, Speaker, Tag, TranscriptTag
from .serializers import TranscriptSerializer, TranscriptListSerializer, SpeakerSerializer, TagSerializer


class TranscriptFilter(django_filters.FilterSet):
    """Custom filter for Transcript model"""
    status = django_filters.ChoiceFilter(choices=Transcript.STATUS_CHOICES)
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='transcript_tags__tag',
        queryset=Tag.objects.all(),
        to_field_name='id'
    )
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Transcript
        fields = ['status', 'tags', 'created_after', 'created_before']


class TranscriptViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Transcript model with filtering, sorting, and pagination.
    
    GET /api/transcripts/ - List all transcripts with filtering and sorting
    GET /api/transcripts/{id}/ - Get single transcript detail
    """
    queryset = Transcript.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TranscriptFilter
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['created_at', 'title', 'status']
    ordering = ['-created_at']  # Default ordering
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return TranscriptListSerializer
        return TranscriptSerializer


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Speaker model.
    """
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['transcript']
    ordering_fields = ['speaking_percentage', 'name']
    ordering = ['-speaking_percentage']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Tag model.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['color']
    search_fields = ['name']
    ordering_fields = ['name', 'color']
    ordering = ['name']
