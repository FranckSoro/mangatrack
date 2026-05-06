from django.contrib import admin
from .models import Genre, Series, UserSeries, ReadingEntry


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'series_type', 'author', 'total_chapters', 'created_by']
    list_filter = ['series_type', 'created_by']
    search_fields = ['title', 'author']
    filter_horizontal = ['genres']


@admin.register(UserSeries)
class UserSeriesAdmin(admin.ModelAdmin):
    list_display = ['user', 'series', 'status', 'is_favorite', 'score', 'added_at']
    list_filter = ['status', 'is_favorite']
    search_fields = ['user__username', 'series__title']
    raw_id_fields = ['user', 'series']


@admin.register(ReadingEntry)
class ReadingEntryAdmin(admin.ModelAdmin):
    list_display = ['user_series', 'chapter_number', 'read_at']
    list_filter = ['read_at']
    search_fields = ['user_series__series__title', 'user_series__user__username']
    raw_id_fields = ['user_series']
