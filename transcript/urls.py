from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TranscriptViewSet, SpeakerViewSet, TagViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'transcripts', TranscriptViewSet, basename='transcript')
router.register(r'speakers', SpeakerViewSet, basename='speaker')
router.register(r'tags', TagViewSet, basename='tag')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
