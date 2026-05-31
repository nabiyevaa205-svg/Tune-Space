from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import get_language

from online_library.translations import get_ui_text

from .models import Book


ARTIST_IMAGES = [
    "books/photo_golden_dragon_internal_flight.jpg",
    "books/photo_i_miss_you.jpg",
    "books/photo_she_will_be_loved.jpg",
    "books/photo_i_want_to_know_what_love_is.jpg",
    "books/photo_all_woman.jpg",
    "books/photo_stay_with_me.jpg",
]

POPULAR_ARTISTS = [
    {
        "name": "BTS",
        "slug": "bts",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/BTS_on_the_Billboard_Music_Awards_red_carpet%2C_1_May_2019.jpg",
        "bio_key": "artist_bts_bio",
    },
    {
        "name": "Britney Spears",
        "slug": "britney-spears",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Britney_spears_2009.jpg",
        "bio_key": "artist_britney_bio",
    },
    {
        "name": "Michael Jackson",
        "slug": "michael-jackson",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Michael_Jackson%2C_1988_%2846845017052%29.jpg",
        "bio_key": "artist_michael_bio",
    },
    {
        "name": "Taylor Swift",
        "slug": "taylor-swift",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/191125_Taylor_Swift_at_the_2019_American_Music_Awards.png",
        "bio_key": "artist_taylor_bio",
    },
    {
        "name": "The Weeknd",
        "slug": "the-weeknd",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/FEQ_July_2018_The_Weeknd_%2844778856382%29_%28cropped%29.jpg",
        "bio_key": "artist_weeknd_bio",
    },
    {
        "name": "Billie Eilish",
        "slug": "billie-eilish",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Billie_Eilish_2019_by_Glenn_Francis.jpg",
        "bio_key": "artist_billie_bio",
    },
    {
        "name": "Lady Gaga",
        "slug": "lady-gaga",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Lady_Gaga_You_and_I_Manchester.jpg",
        "bio_key": "artist_gaga_bio",
    },
    {
        "name": "Drake",
        "slug": "drake",
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Drake_July_2016.jpg",
        "bio_key": "artist_drake_bio",
    },
]

ARTIST_TRACKS = {
    "bts": [
        ("Dynamite", "1,920,450,114", "3:19"),
        ("Butter", "1,342,908,552", "2:44"),
        ("Boy With Luv", "1,184,320,901", "3:49"),
        ("Fake Love", "934,220,778", "4:02"),
        ("Spring Day", "612,091,440", "4:34"),
    ],
    "britney-spears": [
        ("Toxic", "1,128,453,772", "3:19"),
        ("...Baby One More Time", "982,230,411", "3:30"),
        ("Gimme More", "748,112,904", "4:11"),
        ("Oops!... I Did It Again", "701,320,118", "3:31"),
        ("Womanizer", "640,991,882", "3:44"),
    ],
    "michael-jackson": [
        ("Billie Jean", "1,746,321,009", "4:54"),
        ("Beat It", "1,102,552,782", "4:18"),
        ("Smooth Criminal", "978,440,211", "4:17"),
        ("Thriller", "936,120,774", "5:57"),
        ("Man in the Mirror", "695,341,220", "5:19"),
    ],
    "taylor-swift": [
        ("Cruel Summer", "2,010,384,520", "2:58"),
        ("Blank Space", "1,732,440,110", "3:51"),
        ("Anti-Hero", "1,521,940,665", "3:20"),
        ("Shake It Off", "1,418,033,208", "3:39"),
        ("cardigan", "892,430,118", "3:59"),
    ],
    "the-weeknd": [
        ("Blinding Lights", "5,435,135,151", "3:20"),
        ("Starboy", "4,562,134,023", "3:50"),
        ("Die For You", "3,282,528,561", "4:20"),
        ("The Hills", "2,987,140,771", "4:02"),
        ("Save Your Tears", "2,846,004,192", "3:35"),
    ],
    "billie-eilish": [
        ("bad guy", "2,921,492,010", "3:14"),
        ("lovely", "2,314,660,983", "3:20"),
        ("Happier Than Ever", "1,434,229,852", "4:58"),
        ("when the party's over", "1,220,537,991", "3:16"),
        ("ocean eyes", "1,026,910,441", "3:20"),
    ],
    "lady-gaga": [
        ("Shallow", "2,578,903,221", "3:35"),
        ("Poker Face", "1,490,112,804", "3:57"),
        ("Bad Romance", "1,382,441,006", "4:54"),
        ("Just Dance", "1,090,785,554", "4:02"),
        ("Rain On Me", "934,672,118", "3:02"),
    ],
    "drake": [
        ("One Dance", "3,214,903,772", "2:54"),
        ("God's Plan", "2,641,822,004", "3:19"),
        ("Hotline Bling", "1,882,331,091", "4:27"),
        ("In My Feelings", "1,532,882,401", "3:37"),
        ("Passionfruit", "1,217,904,630", "4:58"),
    ],
}

ARTICLES = [
    {
        "slug": "summer-music-trends",
        "title_key": "article_1_title",
        "summary_key": "article_1_summary",
        "body_key": "article_1_body",
        "date": "31 Aug 2026",
        "image": "books/photo_i_will_always_love_you.jpg",
        "skin": "skin-a",
    },
    {
        "slug": "best-live-shows",
        "title_key": "article_2_title",
        "summary_key": "article_2_summary",
        "body_key": "article_2_body",
        "date": "03 Oct 2026",
        "image": "books/photo_i_want_to_know_what_love_is.jpg",
        "skin": "skin-b",
    },
    {
        "slug": "playlist-for-evening",
        "title_key": "article_3_title",
        "summary_key": "article_3_summary",
        "body_key": "article_3_body",
        "date": "31 Oct 2026",
        "image": "books/photo_hotel_california.jpg",
        "skin": "skin-c",
    },
]


def _artist_tracks(slug, image):
    covers = [
        "cover-a",
        "cover-b",
        "cover-c",
        "cover-d",
        "cover-e",
    ]
    tracks = []
    for index, (title, plays, duration) in enumerate(ARTIST_TRACKS.get(slug, [])):
        tracks.append({
            "title": title,
            "plays": plays,
            "duration": duration,
            "image": image,
            "cover_skin": covers[index % len(covers)],
            "logo": "".join(word[0] for word in title.split()[:3]).upper(),
        })
    return tracks


def _artist_image(index):
    return ARTIST_IMAGES[index % len(ARTIST_IMAGES)]


def _popular_artists(books):
    return [
        {
            "name": artist["name"],
            "slug": artist["slug"],
            "image_url": artist["image"],
            "track_count": 0,
        }
        for artist in POPULAR_ARTISTS
    ]


def _page_sections():
    ui = get_ui_text(get_language())
    return {
        "articles": [
            {
                "slug": article["slug"],
                "title": ui[article["title_key"]],
                "summary": ui[article["summary_key"]],
                "date": article["date"],
                "skin": article["skin"],
                "image": article["image"],
            }
            for article in ARTICLES
        ],
        "videos": [
            {"title": "I Miss You", "artist": "Clean Bandit", "skin": "skin-d", "image": "books/photo_i_miss_you.jpg"},
            {"title": "Hotel California", "artist": "Eagles", "skin": "skin-e", "image": "books/photo_hotel_california.jpg"},
            {"title": "I'll Play The Blues", "artist": "Daniel Castro", "skin": "skin-f", "image": "books/photo_golden_dragon_internal_flight.jpg"},
            {"title": "Stay With Me", "artist": "Sam Smith", "skin": "skin-g", "image": "books/photo_stay_with_me.jpg"},
        ],
        "posts": [
            {"title": ui["post_1_title"], "date": "22 Feb 2026", "skin": "skin-h", "image": "books/photo_all_woman.jpg"},
            {"title": ui["post_2_title"], "date": "25 Feb 2026", "skin": "skin-i", "image": "books/photo_she_will_be_loved.jpg"},
            {"title": ui["post_3_title"], "date": "27 Feb 2026", "skin": "skin-j", "image": "books/photo_stay_with_me.jpg"},
        ],
    }


def _book_list_context(books, **extra):
    context = {
        "books": books,
        "top_albums": books[:5],
        "latest_songs": books[:4],
        "featured": books.first(),
        "hero_image": "/media/books/photo_golden_dragon_internal_flight.jpg",
        "artists": _popular_artists(books),
    }
    context.update(_page_sections())
    context.update(extra)
    return context


def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", _book_list_context(books))


def book_search(request, slug):
    books = Book.objects.filter(title__icontains=slug)
    return render(request, "books/book_list.html", _book_list_context(books, search_query=slug))


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_detail.html", {"book": book})


def artist_detail(request, pk):
    books = Book.objects.select_related("author").filter(author_id=pk)
    artist_book = get_object_or_404(books, author_id=pk)
    artist_books = books.order_by("-created_at")
    artist = artist_book.author
    artist_index = max(0, artist.pk - 1)
    context = {
        "artist": artist,
        "artist_books": artist_books,
        "artist_image": f"/media/{_artist_image(artist_index)}",
    }
    return render(request, "books/artist_detail.html", context)


def artist_profile(request, slug):
    ui = get_ui_text(get_language())
    artist = next((item for item in POPULAR_ARTISTS if item["slug"] == slug), None)
    if artist is None:
        return HttpResponseRedirect(reverse("home"))
    context = {
        "artist": {"name": artist["name"]},
        "artist_image": artist["image"],
        "artist_bio": ui.get(artist["bio_key"], ""),
        "popular_tracks": _artist_tracks(slug, artist["image"]),
    }
    return render(request, "books/artist_detail.html", context)


def article_detail(request, slug):
    ui = get_ui_text(get_language())
    article = next((item for item in ARTICLES if item["slug"] == slug), None)
    if article is None:
        return HttpResponseRedirect(reverse("home"))
    context = {
        "article": {
            "title": ui[article["title_key"]],
            "summary": ui[article["summary_key"]],
            "body": ui[article["body_key"]],
            "date": article["date"],
            "image": f"/media/{article['image']}",
        }
    }
    return render(request, "books/article_detail.html", context)


def about(request):
    ui = get_ui_text(get_language())
    return HttpResponse(ui["about"])


def user_profile(request, user_id):
    return HttpResponse(f"User profile: {user_id}")


def home_redirect(request):
    return HttpResponseRedirect(reverse("home"))


def digits_only(request, digits):
    return HttpResponse(f"Digits: {digits}")


def template_demo(request):
    items = [
        "Python",
        "Django",
        "HTML",
        "CSS",
        "Templates",
    ]
    status = "student"
    context = {
        "name": "TuneSpace",
        "items": items,
        "status": status,
    }
    return render(request, "index.html", context)
