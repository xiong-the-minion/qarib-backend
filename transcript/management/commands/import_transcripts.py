import os
import re
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from transcript.models import Transcript, Speaker, Tag, TranscriptTag


class Command(BaseCommand):
    help = 'Import transcript files from public/assets directory and convert them to database records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='public/assets',
            help='Path to the directory containing transcript files (default: public/assets)'
        )
        parser.add_argument(
            '--status',
            type=str,
            default='Finished',
            choices=['Started', 'Postponed', 'Finished'],
            help='Status to assign to imported transcripts (default: Finished)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually creating records'
        )

    def handle(self, *args, **options):
        assets_path = options['path']
        status = options['status']
        dry_run = options['dry_run']

        # Check if the directory exists
        if not os.path.exists(assets_path):
            raise CommandError(f'Directory "{assets_path}" does not exist')

        # Find all text files
        text_files = []
        for file in os.listdir(assets_path):
            if file.endswith(('.txt', '.text')):
                text_files.append(file)

        if not text_files:
            self.stdout.write(
                self.style.WARNING(f'No text files found in "{assets_path}"')
            )
            return

        self.stdout.write(f'Found {len(text_files)} text files to process')

        for filename in text_files:
            file_path = os.path.join(assets_path, filename)
            transcript_title = os.path.splitext(filename)[0]
            
            self.stdout.write(f'Processing: {filename}')
            
            try:
                if dry_run:
                    self._dry_run_import(file_path, transcript_title, status)
                else:
                    self._import_transcript(file_path, transcript_title, status)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {filename}: {str(e)}')
                )

    def _dry_run_import(self, file_path, transcript_title, status):
        """Show what would be imported without creating records"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        parsed_data = self._parse_transcript_content(content)
        
        self.stdout.write(f'  Would create transcript: "{transcript_title}"')
        self.stdout.write(f'  Status: {status}')
        self.stdout.write(f'  Content length: {len(content)} characters')
        self.stdout.write(f'  Speakers found: {len(parsed_data["speakers"])}')
        
        for speaker_name, speaker_data in parsed_data['speakers'].items():
            self.stdout.write(f'    - {speaker_name}: {speaker_data["percentage"]:.1f}% ({speaker_data["word_count"]} words)')

    def _import_transcript(self, file_path, transcript_title, status):
        """Import a single transcript file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        parsed_data = self._parse_transcript_content(content)
        
        # Create or get existing transcript
        transcript, created = Transcript.objects.get_or_create(
            title=transcript_title,
            defaults={
                'content': content,
                'summary': self._generate_summary(content),
                'status': status
            }
        )
        
        if created:
            self.stdout.write(f'  Created transcript: "{transcript_title}"')
        else:
            self.stdout.write(f'  Updated existing transcript: "{transcript_title}"')
            transcript.content = content
            transcript.summary = self._generate_summary(content)
            transcript.status = status
            transcript.save()
        
        # Clear existing speakers for this transcript
        transcript.speakers.all().delete()
        
        # Create speakers
        for speaker_name, speaker_data in parsed_data['speakers'].items():
            Speaker.objects.create(
                name=speaker_name,
                transcript=transcript,
                speaking_percentage=speaker_data['percentage']
            )
        
        self.stdout.write(f'  Created {len(parsed_data["speakers"])} speakers')

    def _parse_transcript_content(self, content):
        """Parse transcript content to extract speakers and their contributions"""
        lines = content.strip().split('\n')
        speakers = defaultdict(lambda: {'word_count': 0, 'lines': []})
        
        current_speaker = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a speaker name and timestamp
            speaker_match = re.match(r'^([A-Za-z\s]+)\s+\d+:\d+\s*$', line)
            
            if speaker_match:
                # Save previous speaker's content
                if current_speaker and current_content:
                    speakers[current_speaker]['lines'].extend(current_content)
                    speakers[current_speaker]['word_count'] += sum(len(line.split()) for line in current_content)
                
                # Start new speaker
                current_speaker = speaker_match.group(1).strip()
                current_content = []
            else:
                # This is content for the current speaker
                if current_speaker:
                    current_content.append(line)
        
        # Don't forget the last speaker
        if current_speaker and current_content:
            speakers[current_speaker]['lines'].extend(current_content)
            speakers[current_speaker]['word_count'] += sum(len(line.split()) for line in current_content)
        
        # Calculate percentages
        total_words = sum(data['word_count'] for data in speakers.values())
        
        for speaker_data in speakers.values():
            if total_words > 0:
                speaker_data['percentage'] = (speaker_data['word_count'] / total_words) * 100
            else:
                speaker_data['percentage'] = 0
        
        return {'speakers': dict(speakers)}

    def _generate_summary(self, content):
        """Generate a simple summary from the content"""
        # Take first few sentences as summary
        sentences = re.split(r'[.!?]+', content)
        summary_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        return '. '.join(summary_sentences) + '.' if summary_sentences else ''
