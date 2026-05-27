from pathlib import Path
from urllib.request import urlopen

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from books.models import Book


PHOTO_URLS = [
    "https://picsum.photos/seed/tunespace1/900/900",
    "https://picsum.photos/seed/tunespace2/900/900",
    "https://picsum.photos/seed/tunespace3/900/900",
    "https://picsum.photos/seed/tunespace4/900/900",
    "https://picsum.photos/seed/tunespace5/900/900",
    "https://picsum.photos/seed/tunespace6/900/900",
    "https://picsum.photos/seed/tunespace7/900/900",
    "https://picsum.photos/seed/tunespace8/900/900",
]


class Command(BaseCommand):
    help = "Download sample album photos and attach them to tracks"

    def handle(self, *args, **options):
        photo_dir = Path(settings.MEDIA_ROOT) / "books"
        photo_dir.mkdir(parents=True, exist_ok=True)

        books = list(Book.objects.all())
        if not books:
            self.stdout.write("No tracks found.")
            return

        updated = 0
        for idx, book in enumerate(books):
            url = PHOTO_URLS[idx % len(PHOTO_URLS)]
            safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in book.title).strip("_")
            local_path = photo_dir / f"photo_{safe_name}.jpg"

            if not local_path.exists():
                with urlopen(url, timeout=20) as response:
                    local_path.write_bytes(response.read())

            with local_path.open("rb") as f:
                book.cover.save(local_path.name, File(f), save=False)
            book.save(update_fields=["cover"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Attached downloaded photos: {updated}"))
