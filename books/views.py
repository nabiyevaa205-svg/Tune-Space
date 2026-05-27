from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Book


def book_list(request):
    books = Book.objects.all()

    events = [
        {"title": "Off Rock Fan", "date": "31 Aug", "place": "Almaty Arena", "skin": "skin-a"},
        {"title": "Rock Wall Music", "date": "03 Oct", "place": "Shymkent Hall", "skin": "skin-b"},
        {"title": "Ultra Music Festival", "date": "31 Oct", "place": "Astana Live", "skin": "skin-c"},
    ]

    videos = [
        {"title": "I Miss You", "artist": "Clean Bandit", "skin": "skin-d"},
        {"title": "Hotel California", "artist": "Eagles", "skin": "skin-e"},
        {"title": "I'll Play The Blues", "artist": "Daniel Castro", "skin": "skin-f"},
        {"title": "Stay With Me", "artist": "Sam Smith", "skin": "skin-g"},
    ]

    posts = [
        {"title": "Remember those great Volkswagen ads?", "date": "22 Feb 2026", "skin": "skin-h"},
        {"title": "Top 10 design albums this month", "date": "25 Feb 2026", "skin": "skin-i"},
        {"title": "Half of what we know about coffee is wrong", "date": "27 Feb 2026", "skin": "skin-j"},
    ]

    context = {
        "books": books,
        "events": events,
        "videos": videos,
        "posts": posts,
        "top_albums": books[:5],
        "latest_songs": books[:4],
        "featured": books.first(),
    }
    return render(request, "books/book_list.html", context)


def book_search(request, slug):
    books = Book.objects.filter(title__icontains=slug)

    events = [
        {"title": "Off Rock Fan", "date": "31 Aug", "place": "Almaty Arena", "skin": "skin-a"},
        {"title": "Rock Wall Music", "date": "03 Oct", "place": "Shymkent Hall", "skin": "skin-b"},
        {"title": "Ultra Music Festival", "date": "31 Oct", "place": "Astana Live", "skin": "skin-c"},
    ]

    videos = [
        {"title": "I Miss You", "artist": "Clean Bandit", "skin": "skin-d"},
        {"title": "Hotel California", "artist": "Eagles", "skin": "skin-e"},
        {"title": "I'll Play The Blues", "artist": "Daniel Castro", "skin": "skin-f"},
        {"title": "Stay With Me", "artist": "Sam Smith", "skin": "skin-g"},
    ]

    posts = [
        {"title": "Remember those great Volkswagen ads?", "date": "22 Feb 2026", "skin": "skin-h"},
        {"title": "Top 10 design albums this month", "date": "25 Feb 2026", "skin": "skin-i"},
        {"title": "Half of what we know about coffee is wrong", "date": "27 Feb 2026", "skin": "skin-j"},
    ]

    context = {
        "books": books,
        "events": events,
        "videos": videos,
        "posts": posts,
        "top_albums": books[:5],
        "latest_songs": books[:4],
        "featured": books.first(),
        "search_query": slug,
    }
    return render(request, "books/book_list.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_detail.html", {"book": book})


def about(request):
    return HttpResponse("About page")


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
        "name": "online library",
        "items": items,
        "status": status,
    }
    return render(request, "index.html", context)
