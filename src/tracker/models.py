from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import re


class Genre(models.Model):
    """Genre de manga/manhwa/manhua"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Series(models.Model):
    """Série partagée entre tous les utilisateurs"""
    SERIES_TYPE_CHOICES = [
        ('manga', 'Manga'),
        ('manhwa', 'Manhwa'),
        ('manhua', 'Manhua'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    series_type = models.CharField(max_length=10, choices=SERIES_TYPE_CHOICES)
    author = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    total_chapters = models.PositiveIntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_series')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_series_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def cover_url(self):
        if not self.cover:
            return None
        import boto3
        from django.conf import settings
        s3 = boto3.client(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        return s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': self.cover.name,
            },
            ExpiresIn=3600
        )


class UserSeries(models.Model):
    """Série dans la bibliothèque d'un utilisateur"""
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('pause', 'En pause'),
        ('abandonne', 'Abandonné'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='user_series')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')
    is_favorite = models.BooleanField(default=False)
    score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    notes = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'series']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'is_favorite']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.series.title}"

    def last_chapter_read(self):
        """Dernier chapitre lu (calculé via ORM)"""
        entry = self.reading_entries.order_by('-chapter_number').first()
        return entry.chapter_number if entry else 0

    def total_chapters_read(self):
        """Nombre total de chapitres lus"""
        return self.reading_entries.count()


class ReadingEntry(models.Model):
    """Entrée d'historique de lecture"""
    user_series = models.ForeignKey(
        UserSeries, on_delete=models.CASCADE, related_name='reading_entries'
    )
    chapter_number = models.PositiveIntegerField()
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-read_at']
        indexes = [
            models.Index(fields=['user_series', '-chapter_number']),
        ]

    def __str__(self):
        return f"{self.user_series.series.title} - Chapitre {self.chapter_number}"
