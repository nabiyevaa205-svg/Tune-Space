from django.db import models


class RecentBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_year__gt=2000)


class Author(models.Model):
    name = models.CharField(max_length=150, unique=True)
    birthdate = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField()
    cover = models.ImageField(upload_to="books/", blank=True, null=True)
    audio_file = models.FileField(upload_to="tracks/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    published_year = models.PositiveIntegerField(default=2001)
    genres = models.ManyToManyField(Genre, blank=True, related_name="books")

    objects = models.Manager()
    recent_books = RecentBookManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
