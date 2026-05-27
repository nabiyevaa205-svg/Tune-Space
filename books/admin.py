from django.contrib import admin

from .models import Author, Book, Genre

admin.site.site_header = "Online Library Admin"
admin.site.site_title = "Online Library"
admin.site.index_title = "Administration"


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ("title ", "published_year", "status")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_year", "has_cover", "has_audio", "created_at")
    list_filter = ("published_year", "status")
    readonly_fields = ("created_at",)
    search_fields = ("title", "author__name")
    actions = ("mark_published",)

    @admin.action(description="Mark selected books as published")
    def mark_published(self, request, queryset):
        queryset.update(status=Book.STATUS_PUBLISHED)

    @admin.display(boolean=True, description="Cover")
    def has_cover(self, obj):
        return bool(obj.cover)

    @admin.display(boolean=True, description="Audio")
    def has_audio(self, obj):
        return bool(obj.audio_file)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate")
    search_fields = ("name",)
    inlines = [BookInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
