from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import get_language

from online_library.translations import get_ui_text

from .models import Book


def _page_sections():
    ui = get_ui_text(get_language())
    return {
        "events": [
            {"title": ui["event_1_title"], "date": "31 Aug", "place": "Almaty Arena", "skin": "skin-a", "image": "books/photo_i_will_always_love_you.jpg"},
            {"title": ui["event_2_title"], "date": "03 Oct", "place": "Shymkent Hall", "skin": "skin-b", "image": "books/photo_i_want_to_know_what_love_is.jpg"},
            {"title": ui["event_3_title"], "date": "31 Oct", "place": "Astana Live", "skin": "skin-c", "image": "books/photo_hotel_california.jpg"},
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
