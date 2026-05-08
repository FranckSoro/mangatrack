from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg, Max
from django.urls import reverse
from django.utils import timezone
from .models import Genre, Series, UserSeries, ReadingEntry, ReadingSite


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'series_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(series_count=Count('series'))

    @admin.display(description='Séries')
    def series_count(self, obj):
        return obj.series_count


class ReadingEntryInline(admin.TabularInline):
    model = ReadingEntry
    extra = 0
    readonly_fields = ['read_at']
    fields = ['chapter_number', 'read_at']
    can_delete = True


class UserSeriesInline(admin.TabularInline):
    model = UserSeries
    extra = 0
    fields = ['user', 'status', 'is_favorite', 'score', 'added_at']
    readonly_fields = ['added_at']
    can_delete = True


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'series_type', 'author', 'total_chapters', 'readers_count', 'avg_score', 'created_by', 'created_at']
    list_filter = ['series_type', 'genres', 'created_by', 'created_at']
    search_fields = ['title', 'author']
    filter_horizontal = ['genres']
    readonly_fields = ['slug', 'created_at', 'cover_preview']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    inlines = [UserSeriesInline]

    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'slug', 'series_type', 'author', 'total_chapters')
        }),
        ('Médias', {
            'fields': ('cover', 'cover_preview')
        }),
        ('Genres', {
            'fields': ('genres',)
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            readers_count=Count('user_series', distinct=True),
            avg_score=Avg('user_series__score')
        )

    @admin.display(description='Lecteurs')
    def readers_count(self, obj):
        count = obj.readers_count or 0
        url = reverse('admin:tracker_userseries_changelist')
        return mark_safe(f'<a href="{url}?series__id__exact={obj.id}">{count}</a>')

    @admin.display(description='Note moyenne')
    def avg_score(self, obj):
        if obj.avg_score:
            score = float(obj.avg_score)
            color = self._get_score_color(score)
            return mark_safe(f'<span style="color: {color}; font-weight: bold;">{score:.1f}/10</span>')
        return '-'

    def _get_score_color(self, score):
        if score >= 8:
            return '#16a34a'  # green
        elif score >= 6:
            return '#ca8a04'  # yellow
        elif score >= 4:
            return '#ea580c'  # orange
        else:
            return '#dc2626'  # red

    @admin.display(description='Aperçu')
    def cover_preview(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" style="max-width: 200px; max-height: 300px; object-fit: cover;" />')
        return 'Aucune image'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserSeries)
class UserSeriesAdmin(admin.ModelAdmin):
    list_display = ['user', 'series', 'status', 'is_favorite', 'score', 'progress', 'added_at']
    list_filter = ['status', 'is_favorite', 'score', 'added_at']
    search_fields = ['user__username', 'user__email', 'series__title', 'series__author']
    raw_id_fields = ['user', 'series']
    readonly_fields = ['added_at', 'last_chapter_read', 'total_chapters_read']
    ordering = ['-added_at']
    date_hierarchy = 'added_at'
    inlines = [ReadingEntryInline]

    fieldsets = (
        ('Relation', {
            'fields': ('user', 'series')
        }),
        ('Statut et préférences', {
            'fields': ('status', 'is_favorite', 'score')
        }),
        ('Progression', {
            'fields': ('last_chapter_read', 'total_chapters_read'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Métadonnées', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Progression')
    def progress(self, obj):
        last_chapter = obj.last_chapter_read()
        total_chapters = obj.series.total_chapters

        if total_chapters and last_chapter:
            percentage = (int(last_chapter) / int(total_chapters)) * 100
            percentage = int(min(percentage, 100))
            return mark_safe(
                f'<div style="width: 100px; background-color: #e5e7eb; border-radius: 4px; overflow: hidden;">'
                f'<div style="width: {percentage}%; background-color: #3b82f6; height: 8px;"></div>'
                f'</div>'
                f'<small>{int(last_chapter)} / {int(total_chapters)}</small>'
            )
        return '-'

    @admin.display(description='Dernier chapitre')
    def last_chapter_read(self, obj):
        return obj.last_chapter_read() or '-'

    @admin.display(description='Chapitres lus')
    def total_chapters_read(self, obj):
        return obj.total_chapters_read()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'series')


@admin.register(ReadingEntry)
class ReadingEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'series', 'chapter_number', 'read_at']
    list_filter = ['read_at', 'chapter_number']
    search_fields = ['user_series__user__username', 'user_series__series__title']
    raw_id_fields = ['user_series']
    readonly_fields = ['read_at', 'user', 'series']
    ordering = ['-read_at']
    date_hierarchy = 'read_at'

    def user(self, obj):
        return obj.user_series.user

    user.short_description = 'Utilisateur'

    def series(self, obj):
        return obj.user_series.series

    series.short_description = 'Série'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user_series__user', 'user_series__series')


@admin.register(ReadingSite)
class ReadingSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'logo_preview', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name', 'url', 'description']
    readonly_fields = ['created_at', 'logo_preview', 'created_by']
    ordering = ['name']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'url')
        }),
        ('Médias', {
            'fields': ('logo', 'logo_preview')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Aperçu')
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo_url()}" style="max-width: 100px; max-height: 100px; object-fit: contain;" />')
        return 'Aucun logo'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Personnalisation de l'admin site
admin.site.site_header = 'MangaTrack Administration'
admin.site.site_title = 'MangaTrack'
admin.site.index_title = 'Bienvenue dans l\'administration de MangaTrack'
