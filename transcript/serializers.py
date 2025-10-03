from rest_framework import serializers
from .models import Transcript, Speaker, Tag, TranscriptTag


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['id', 'name', 'speaking_percentage']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class TranscriptTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    
    class Meta:
        model = TranscriptTag
        fields = ['tag']


class TranscriptSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)
    transcript_tags = TranscriptTagSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Transcript
        fields = [
            'id', 'title', 'content', 'summary', 'created_at', 
            'status', 'speakers', 'transcript_tags', 'tags'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_tags(self, obj):
        """Get tags associated with this transcript"""
        return [transcript_tag.tag for transcript_tag in obj.transcript_tags.all()]


class TranscriptListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    tags = serializers.SerializerMethodField()
    speaker_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Transcript
        fields = [
            'id', 'title', 'summary', 'created_at', 
            'status', 'tags', 'speaker_count'
        ]
    
    def get_tags(self, obj):
        """Get tags associated with this transcript"""
        return [transcript_tag.tag for transcript_tag in obj.transcript_tags.all()]
    
    def get_speaker_count(self, obj):
        """Get number of speakers for this transcript"""
        return obj.speakers.count()
