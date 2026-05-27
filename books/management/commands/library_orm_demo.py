from django.core.management.base import BaseCommand

from books.models import Author, Book, Genre


class Command(BaseCommand):
    help = "Runs the ORM tasks for authors, books, and genres."

    def handle(self, *args, **options):
        authors_data = [
            {"name": "George Orwell", "birthdate": "1903-06-25"},
            {"name": "J. K. Rowling", "birthdate": "1965-07-31"},
            {"name": "Haruki Murakami", "birthdate": "1949-01-12"},
        ]

        authors = []
        for data in authors_data:
            author, _ = Author.objects.get_or_create(
                name=data["name"],
                defaults={"birthdate": data["birthdate"]},
            )
            authors.append(author)

        dystopian, _ = Genre.objects.get_or_create(name="Dystopian")
        fantasy, _ = Genre.objects.get_or_create(name="Fantasy")
        fiction, _ = Genre.objects.get_or_create(name="Fiction")

        book_one, _ = Book.objects.get_or_create(
            id=1,
            defaults={
                "title": "1984",
                "author": authors[0],
                "description": "Classic dystopian novel.",
                "published_year": 1949,
            },
        )
        book_two, _ = Book.objects.get_or_create(
            title="Harry Potter and the Goblet of Fire",
            author=authors[1],
            defaults={
                "description": "Fantasy adventure.",
                "published_year": 2000,
            },
        )
        book_three, _ = Book.objects.get_or_create(
            title="Kafka on the Shore",
            author=authors[2],
            defaults={
                "description": "Magical realism.",
                "published_year": 2002,
            },
        )

        book_one.genres.set([dystopian, fiction])
        book_two.genres.set([fantasy, fiction])
        book_three.genres.set([fiction])

        target_author = Author.objects.get(name="J. K. Rowling")
        author_books = list(Book.objects.filter(author=target_author).values_list("title", flat=True))
        self.stdout.write(f"Books by {target_author.name}: {author_books}")

        updated = Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")
        self.stdout.write(f"Updated book with id=1: {updated}")

        cascade_author = Author.objects.create(name="Cascade Author", birthdate="1970-01-01")
        cascade_book = Book.objects.create(
            title="Cascade Test",
            author=cascade_author,
            description="Cascade test record.",
            published_year=2005,
        )
        cascade_author_id = cascade_author.id
        cascade_book_id = cascade_book.id
        cascade_author.delete()
        cascade_exists = Book.objects.filter(id=cascade_book_id).exists()
        self.stdout.write(
            f"Cascade after deleting author {cascade_author_id}: book exists={cascade_exists}"
        )

        recent_titles = list(Book.recent_books.values_list("title", flat=True))
        self.stdout.write(f"Recent books after 2000: {recent_titles}")
