import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Transcript(models.Model):
    STATUS_CHOICES = [
        ('Started', 'Started'),
        ('Postponed', 'Postponed'),
        ('Finished', 'Finished'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Started')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Speaker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='speakers')
    speaking_percentage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    
    class Meta:
        ordering = ['-speaking_percentage']
    
    def __str__(self):
        return f"{self.name} ({self.speaking_percentage}%)"


class Tag(models.Model):
    COLOR_CHOICES = [
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TranscriptTag(models.Model):
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='transcript_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='transcript_tags')
    
    class Meta:
        unique_together = ['transcript', 'tag']
    
    def __str__(self):
        return f"{self.transcript.title} - {self.tag.name}"
