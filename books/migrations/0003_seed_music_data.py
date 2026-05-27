from django.db import migrations


def seed_tracks(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    tracks = [
        ("Golden Dragon Internal Flight", "Estas Tonne", "Atmospheric live guitar session with cinematic emotion."),
        ("She Will Be Loved", "Franko Lotus", "Soft pop ballad for calm evening listening."),
        ("All Woman", "Sam Smith", "Soul-inspired vocal track with minimal groove."),
        ("I Want To Know What Love Is", "Daniel Castro", "Classic mood with modern blues texture."),
        ("I Will Always Love You", "Whitney Houston", "Powerful vocal anthem remastered mood version."),
        ("Hotel California", "Eagles", "Timeless rock arrangement and smooth guitar lines."),
        ("Stay With Me", "Sam Smith", "Emotional pop track for late-night playlist."),
        ("I Miss You", "Clean Bandit", "Melodic electronic-pop song with rhythmic pulse."),
    ]

    for title, author, description in tracks:
        Book.objects.get_or_create(
            title=title,
            author=author,
            defaults={"description": description},
        )


def unseed_tracks(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    titles = [
        "Golden Dragon Internal Flight",
        "She Will Be Loved",
        "All Woman",
        "I Want To Know What Love Is",
        "I Will Always Love You",
        "Hotel California",
        "Stay With Me",
        "I Miss You",
    ]
    Book.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_alter_book_cover"),
    ]

    operations = [
        migrations.RunPython(seed_tracks, unseed_tracks),
    ]
