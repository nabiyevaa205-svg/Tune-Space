import math
import struct
import wave
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from PIL import Image, ImageDraw, ImageFont

from books.models import Book


TRACK_PRESETS = {
    "Golden Dragon Internal Flight": (196, (85, 29, 130), (41, 127, 255)),
    "She Will Be Loved": (220, (215, 74, 126), (255, 146, 95)),
    "All Woman": (246, (61, 97, 227), (96, 211, 255)),
    "I Want To Know What Love Is": (262, (130, 37, 92), (255, 96, 143)),
    "I Will Always Love You": (294, (65, 70, 170), (164, 116, 255)),
    "Hotel California": (329, (184, 97, 34), (255, 204, 97)),
    "Stay With Me": (349, (36, 140, 132), (107, 236, 194)),
    "I Miss You": (392, (124, 41, 170), (235, 114, 255)),
}


class Command(BaseCommand):
    help = "Generate demo audio tracks and album covers, then attach them to Book records"

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        track_dir = media_root / "tracks"
        cover_dir = media_root / "books"
        track_dir.mkdir(parents=True, exist_ok=True)
        cover_dir.mkdir(parents=True, exist_ok=True)

        updated = 0
        for book in Book.objects.all():
            freq, c1, c2 = TRACK_PRESETS.get(book.title, (240, (76, 102, 180), (94, 206, 235)))

            safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in book.title).strip("_")
            wav_path = track_dir / f"{safe_name}.wav"
            cover_path = cover_dir / f"{safe_name}.png"

            if not wav_path.exists():
                self._generate_wav(wav_path, freq)
            if not cover_path.exists():
                self._generate_cover(cover_path, book.title, book.author, c1, c2)

            changed = False
            if not book.audio_file:
                with wav_path.open("rb") as f:
                    book.audio_file.save(wav_path.name, File(f), save=False)
                changed = True

            if not book.cover:
                with cover_path.open("rb") as f:
                    book.cover.save(cover_path.name, File(f), save=False)
                changed = True

            if changed:
                book.save(update_fields=["audio_file", "cover"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Demo media ready. Updated tracks: {updated}"))

    def _generate_wav(self, target_path: Path, freq: int, duration_sec: float = 24.0):
        sample_rate = 44100
        amplitude = 16000
        n_samples = int(sample_rate * duration_sec)

        with wave.open(str(target_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            for i in range(n_samples):
                t = i / sample_rate
                beat = 0.5 * math.sin(2 * math.pi * 2 * t)
                tone = math.sin(2 * math.pi * freq * t)
                overtone = 0.3 * math.sin(2 * math.pi * (freq * 1.5) * t)
                value = int(amplitude * (0.7 * tone + overtone + 0.2 * beat))
                wav_file.writeframesraw(struct.pack("<h", max(-32767, min(32767, value))))

    def _generate_cover(self, target_path: Path, title: str, artist: str, c1, c2):
        img = Image.new("RGB", (800, 800), c1)
        draw = ImageDraw.Draw(img)

        for y in range(800):
            p = y / 799
            r = int(c1[0] * (1 - p) + c2[0] * p)
            g = int(c1[1] * (1 - p) + c2[1] * p)
            b = int(c1[2] * (1 - p) + c2[2] * p)
            draw.line((0, y, 800, y), fill=(r, g, b))

        draw.ellipse((90, 120, 710, 740), outline=(255, 255, 255), width=3)
        draw.ellipse((240, 270, 560, 590), outline=(255, 255, 255), width=2)
        draw.rectangle((130, 645, 670, 715), fill=(12, 14, 31, 170))

        title_font = ImageFont.load_default()
        artist_font = ImageFont.load_default()
        draw.text((155, 655), title[:40], fill=(243, 246, 255), font=title_font)
        draw.text((155, 685), artist[:40], fill=(205, 214, 255), font=artist_font)

        img.save(target_path, "PNG")
