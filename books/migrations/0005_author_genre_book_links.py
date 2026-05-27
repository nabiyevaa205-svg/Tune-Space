import datetime

from django.db import migrations, models


def forwards_create_authors(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    Author = apps.get_model("books", "Author")

    author_map = {}
    for book in Book.objects.all().only("id", "author"):
        author_name = book.author.strip() if book.author else "Unknown"
        author = author_map.get(author_name)
        if author is None:
            author = Author.objects.create(name=author_name, birthdate=datetime.date(1970, 1, 1))
            author_map[author_name] = author
        book.author_fk = author
        book.save(update_fields=["author_fk"])


def backwards_restore_author_field(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    for book in Book.objects.select_related("author").all().only("id", "author"):
        book.author = book.author.name if book.author_id else ""
        book.save(update_fields=["author"])


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0004_book_audio_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                ("birthdate", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="book",
            name="published_year",
            field=models.PositiveIntegerField(default=2001),
        ),
        migrations.AddField(
            model_name="book",
            name="author_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="books",
                to="books.author",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="genres",
            field=models.ManyToManyField(blank=True, related_name="books", to="books.genre"),
        ),
        migrations.RunPython(forwards_create_authors, backwards_restore_author_field),
        migrations.RemoveField(
            model_name="book",
            name="author",
        ),
        migrations.RenameField(
            model_name="book",
            old_name="author_fk",
            new_name="author",
        ),
    ]
