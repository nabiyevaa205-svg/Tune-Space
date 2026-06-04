from datetime import date

from django.core.management.base import BaseCommand

from books.models import Author, Book, Genre


ARTISTS = [
    ("Whitney Houston", "Pop", ["I Will Always Love You", "How Will I Know", "I Wanna Dance With Somebody", "Greatest Love", "Run To You"]),
    ("Sam Smith", "Soul", ["Stay With Me", "All Woman", "Unholy", "Too Good At Goodbyes", "Writing's On The Wall"]),
    ("Clean Bandit", "Electronic", ["I Miss You", "Rather Be", "Rockabye", "Symphony", "Solo"]),
    ("Eagles", "Rock", ["Hotel California", "Take It Easy", "Desperado", "One Of These Nights", "Lyin' Eyes"]),
    ("Daniel Castro", "Blues", ["I'll Play The Blues", "Midnight Guitar", "Slow River", "Blue Lights", "Downtown Soul"]),
    ("BTS", "K-Pop", ["Dynamite", "Butter", "Boy With Luv", "Fake Love", "Spring Day"]),
    ("Britney Spears", "Pop", ["Toxic", "Baby One More Time", "Gimme More", "Oops I Did It Again", "Womanizer"]),
    ("Michael Jackson", "Pop", ["Billie Jean", "Beat It", "Smooth Criminal", "Thriller", "Man In The Mirror"]),
    ("Taylor Swift", "Pop", ["Cruel Summer", "Blank Space", "Anti-Hero", "Shake It Off", "Cardigan"]),
    ("The Weeknd", "R&B", ["Blinding Lights", "Starboy", "Die For You", "The Hills", "Save Your Tears"]),
    ("Billie Eilish", "Alternative", ["Bad Guy", "Lovely", "Happier Than Ever", "When The Party Is Over", "Ocean Eyes"]),
    ("Lady Gaga", "Dance", ["Shallow", "Poker Face", "Bad Romance", "Just Dance", "Rain On Me"]),
    ("Drake", "Hip-Hop", ["One Dance", "God's Plan", "Hotline Bling", "In My Feelings", "Passionfruit"]),
    ("Adele", "Soul", ["Hello", "Someone Like You", "Rolling In The Deep", "Easy On Me", "Set Fire To The Rain"]),
    ("Rihanna", "R&B", ["Diamonds", "Umbrella", "We Found Love", "Stay", "Work"]),
    ("Beyonce", "R&B", ["Halo", "Crazy In Love", "Formation", "Single Ladies", "Cuff It"]),
    ("Bruno Mars", "Funk", ["Uptown Funk", "Locked Out Of Heaven", "When I Was Your Man", "Treasure", "Grenade"]),
    ("Ed Sheeran", "Acoustic", ["Shape Of You", "Perfect", "Thinking Out Loud", "Photograph", "Bad Habits"]),
    ("Dua Lipa", "Dance", ["Levitating", "New Rules", "Don't Start Now", "Physical", "Houdini"]),
    ("Ariana Grande", "Pop", ["Thank U Next", "7 Rings", "Positions", "Into You", "No Tears Left To Cry"]),
    ("SZA", "R&B", ["Kill Bill", "Good Days", "Snooze", "Broken Clocks", "Saturn"]),
    ("Olivia Rodrigo", "Pop Rock", ["Drivers License", "Vampire", "Good 4 U", "Traitor", "Deja Vu"]),
    ("Post Malone", "Hip-Hop", ["Circles", "Sunflower", "Rockstar", "Chemical", "Congratulations"]),
    ("Kendrick Lamar", "Hip-Hop", ["Humble", "Alright", "DNA", "Swimming Pools", "Money Trees"]),
    ("Kanye West", "Hip-Hop", ["Stronger", "Heartless", "Runaway", "Gold Digger", "Flashing Lights"]),
    ("Travis Scott", "Hip-Hop", ["Sicko Mode", "Goosebumps", "Highest In The Room", "Fein", "My Eyes"]),
    ("Doja Cat", "Pop Rap", ["Say So", "Paint The Town Red", "Woman", "Agora Hills", "Kiss Me More"]),
    ("Miley Cyrus", "Pop", ["Flowers", "Wrecking Ball", "Party In The USA", "Malibu", "Midnight Sky"]),
    ("Harry Styles", "Pop", ["As It Was", "Watermelon Sugar", "Sign Of The Times", "Adore You", "Golden"]),
    ("Justin Bieber", "Pop", ["Peaches", "Sorry", "Love Yourself", "Baby", "Ghost"]),
    ("Selena Gomez", "Pop", ["Lose You To Love Me", "Rare", "Wolves", "Same Old Love", "Calm Down"]),
    ("Coldplay", "Rock", ["Yellow", "Viva La Vida", "Fix You", "Paradise", "A Sky Full Of Stars"]),
    ("Imagine Dragons", "Rock", ["Believer", "Radioactive", "Demons", "Thunder", "Bones"]),
    ("Maroon 5", "Pop Rock", ["She Will Be Loved", "Sugar", "Memories", "Animals", "This Love"]),
    ("Queen", "Rock", ["Bohemian Rhapsody", "Don't Stop Me Now", "Another One Bites The Dust", "Somebody To Love", "We Are The Champions"]),
    ("Nirvana", "Grunge", ["Smells Like Teen Spirit", "Come As You Are", "Lithium", "Heart Shaped Box", "About A Girl"]),
    ("Metallica", "Metal", ["Enter Sandman", "Nothing Else Matters", "One", "Master Of Puppets", "The Unforgiven"]),
    ("Daft Punk", "Electronic", ["Get Lucky", "One More Time", "Harder Better Faster Stronger", "Around The World", "Digital Love"]),
    ("Avicii", "Electronic", ["Wake Me Up", "Levels", "The Nights", "Waiting For Love", "Hey Brother"]),
    ("Shakira", "Latin Pop", ["Hips Don't Lie", "Whenever Wherever", "Waka Waka", "Chantaje", "She Wolf"]),
]


class Command(BaseCommand):
    help = "Seed the TuneSpace database with 40 artists and 200 songs."

    def handle(self, *args, **options):
        created_authors = 0
        created_books = 0

        for index, (artist_name, genre_name, titles) in enumerate(ARTISTS):
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            author, author_created = Author.objects.get_or_create(
                name=artist_name,
                defaults={"birthdate": date(1980 + (index % 20), 1, 1)},
            )
            if author_created:
                created_authors += 1

            for offset, title in enumerate(titles):
                book, book_created = Book.objects.update_or_create(
                    title=title,
                    author=author,
                    defaults={
                        "description": f"{title} by {artist_name} - TuneSpace curated track.",
                        "status": Book.STATUS_PUBLISHED,
                        "published_year": 2026 - (offset % 5),
                    },
                )
                book.genres.set([genre])
                if book_created:
                    created_books += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created_authors} new artists, {created_books} new songs."
        ))
