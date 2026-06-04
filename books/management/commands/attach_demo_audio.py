import math
import struct
import wave
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = "Attach short generated WAV previews to tracks without audio files."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=220)

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        tracks_dir = media_root / "tracks"
        tracks_dir.mkdir(parents=True, exist_ok=True)

        updated = 0
        sample_rate = 22050
        duration_seconds = 8

        for index, book in enumerate(Book.objects.filter(audio_file="")[: options["limit"]]):
            filename = f"demo_track_{book.pk}.wav"
            path = tracks_dir / filename

            if not path.exists():
                frequency = 220 + ((index % 24) * 18)
                with wave.open(str(path), "w") as audio:
                    audio.setnchannels(1)
                    audio.setsampwidth(2)
                    audio.setframerate(sample_rate)
                    for frame in range(sample_rate * duration_seconds):
                        fade = min(1, frame / 2000, (sample_rate * duration_seconds - frame) / 2000)
                        value = int(22000 * fade * math.sin(2 * math.pi * frequency * frame / sample_rate))
                        audio.writeframes(struct.pack("<h", value))

            book.audio_file.name = f"tracks/{filename}"
            book.save(update_fields=["audio_file"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Attached demo audio to {updated} tracks."))
