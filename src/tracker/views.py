from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.db.models import Count, Avg, Sum, F, Max
from django.contrib import messages
from django.core.paginator import Paginator
from django import forms
from django.conf import settings

from .models import Series, UserSeries, ReadingEntry, Genre, ReadingSite
from .forms import SeriesForm, UserSeriesForm, ReadingEntryForm, ReadingSiteForm, ProfileForm, CustomPasswordChangeForm


class ProfileForm(forms.ModelForm):
    """Formulaire de modification du profil utilisateur"""
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False


class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription personnalisé avec email"""
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


@login_required
def dashboard(request):
    """Tableau de bord avec statistiques"""
    user = request.user

    # Statistiques globales
    total_series = UserSeries.objects.filter(user=user).count()
    total_chapters_read = ReadingEntry.objects.filter(
        user_series__user=user
    ).count()

    # Séries par statut
    status_stats = UserSeries.objects.filter(user=user).values('status').annotate(
        count=Count('id')
    )

    # Score moyen
    avg_score = UserSeries.objects.filter(
        user=user, score__isnull=False
    ).aggregate(avg=Avg('score'))['avg']

    # Activité récente
    recent_entries = ReadingEntry.objects.filter(
        user_series__user=user
    ).select_related('user_series__series')[:5]

    # Favoris
    favorites = UserSeries.objects.filter(user=user, is_favorite=True)[:4]

    context = {
        'total_series': total_series,
        'total_chapters_read': total_chapters_read,
        'status_stats': {s['status']: s['count'] for s in status_stats},
        'avg_score': round(avg_score, 1) if avg_score else None,
        'recent_entries': recent_entries,
        'favorites': favorites,
    }

    return render(request, 'tracker/dashboard.html', context)


@login_required
def library(request):
    """Bibliothèque de l'utilisateur avec filtres"""
    user = request.user

    queryset = UserSeries.objects.filter(user=user).select_related('series')

    # Filtres
    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)

    if request.GET.get('favorites') == 'on':
        queryset = queryset.filter(is_favorite=True)

    series_type = request.GET.get('type')
    if series_type:
        queryset = queryset.filter(series__series_type=series_type)

    # Recherche
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(series__title__icontains=search)

    # Tri
    sort = request.GET.get('sort')
    if sort:
        if sort == 'title':
            queryset = queryset.order_by('series__title')
        elif sort == '-title':
            queryset = queryset.order_by('-series__title')
        elif sort == '-added_at':
            queryset = queryset.order_by('-added_at')
        elif sort == 'added_at':
            queryset = queryset.order_by('added_at')
        elif sort == '-score':
            queryset = queryset.order_by('-score')
        elif sort == 'score':
            queryset = queryset.order_by('score')
    else:
        queryset = queryset.order_by('-added_at')

    # Annotation du dernier chapitre lu
    queryset = queryset.annotate(
        last_chapter=Max('reading_entries__chapter_number')
    )

    # Pagination
    paginator = Paginator(queryset, 12)
    page = request.GET.get('page')
    user_series_list = paginator.get_page(page)

    context = {
        'user_series_list': user_series_list,
        'status_choices': UserSeries.STATUS_CHOICES,
        'type_choices': Series.SERIES_TYPE_CHOICES,
    }

    return render(request, 'tracker/library.html', context)


@login_required
def add_series(request):
    """Ajouter une nouvelle série"""
    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series = form.save(commit=False)
            series.created_by = request.user
            series.save()
            form.save_m2m()

            # Créer l'entrée UserSeries
            user_series = UserSeries.objects.create(
                user=request.user,
                series=series,
                status='en_cours'
            )

            messages.success(request, f"{series.title} a été ajoutée à votre bibliothèque !")
            return redirect('tracker:series_detail', slug=series.slug)
    else:
        form = SeriesForm()

    return render(request, 'tracker/series_form.html', {'form': form, 'action': 'add'})


@login_required
def series_detail(request, slug):
    """Détail d'une série dans la bibliothèque"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series').prefetch_related('series__genres'),
        series=series,
        user=request.user
    )

    # Dernier chapitre lu
    last_entry = user_series.reading_entries.order_by('-chapter_number').first()
    last_chapter = last_entry.chapter_number if last_entry else 0

    # Historique récent (pagination)
    history = user_series.reading_entries.order_by('-read_at')[:20]

    # Formulaire pour ajout rapide de chapitre
    chapter_form = ReadingEntryForm()

    context = {
        'user_series': user_series,
        'last_chapter': last_chapter,
        'history': history,
        'chapter_form': chapter_form,
    }

    return render(request, 'tracker/series_detail.html', context)


@login_required
def edit_user_series(request, slug):
    """Éditer une série dans la bibliothèque"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )

    if request.method == 'POST':
        form = UserSeriesForm(request.POST, instance=user_series)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre bibliothèque a été mise à jour !")
            return redirect('tracker:series_detail', slug=slug)
    else:
        form = UserSeriesForm(instance=user_series)

    return render(request, 'tracker/series_form.html', {'form': form, 'user_series': user_series, 'action': 'edit'})


@login_required
def edit_series(request, slug):
    """Éditer les informations de la série (y compris la couverture)"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )

    if request.method == 'POST':
        form = SeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations de {series.title} ont été mises à jour !")
            return redirect('tracker:series_detail', slug=slug)
    else:
        form = SeriesForm(instance=series)

    return render(request, 'tracker/series_form.html', {'form': form, 'user_series': user_series, 'action': 'edit_series'})


@login_required
def delete_user_series(request, slug):
    """Supprimer une série de la bibliothèque"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )

    if request.method == 'POST':
        series_title = user_series.series.title
        user_series.delete()
        messages.success(request, f"{series_title} a été supprimée de votre bibliothèque.")
        return redirect('tracker:library')

    return render(request, 'tracker/series_confirm_delete.html', {'user_series': user_series})


@login_required
def add_chapter(request, slug):
    """Ajouter un chapitre lu"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )

    if request.method == 'POST':
        form = ReadingEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user_series = user_series
            entry.save()
            messages.success(request, f"Chapitre {entry.chapter_number} enregistré !")
            return redirect('tracker:series_detail', slug=slug)
    else:
        form = ReadingEntryForm()

    return redirect('tracker:series_detail', pk=pk)


@login_required
def reading_history(request, slug):
    """Historique complet de lecture d'une série"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )

    entries = user_series.reading_entries.order_by('-read_at')
    paginator = Paginator(entries, 20)
    page = request.GET.get('page')
    entries_page = paginator.get_page(page)

    context = {
        'user_series': user_series,
        'entries': entries_page,
    }

    return render(request, 'tracker/reading_history.html', context)


@login_required
def delete_reading_entry(request, slug, entry_id):
    """Supprimer une entrée d'historique de lecture"""
    series = get_object_or_404(Series, slug=slug)
    user_series = get_object_or_404(
        UserSeries.objects.select_related('series'),
        series=series,
        user=request.user
    )
    entry = get_object_or_404(ReadingEntry, id=entry_id, user_series=user_series)

    if request.method == 'POST':
        chapter_number = entry.chapter_number
        entry.delete()
        messages.success(request, f"Chapitre {chapter_number} supprimé de l'historique !")
        return redirect('tracker:reading_history', slug=slug)

    return render(request, 'tracker/reading_entry_confirm_delete.html', {
        'user_series': user_series,
        'entry': entry
    })


@login_required
def edit_profile(request):
    """Modifier le profil utilisateur"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('tracker:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'tracker/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    """Changer le mot de passe"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été changé avec succès !")
            return redirect('tracker:profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'tracker/change_password.html', {'form': form})


@login_required
def delete_account(request):
    """Supprimer le compte utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        if username == request.user.username:
            user = request.user
            user.delete()
            messages.success(request, "Votre compte a été supprimé avec succès.")
            return redirect('tracker:login')
        else:
            messages.error(request, "Le nom d'utilisateur ne correspond pas.")
            return redirect('tracker:delete_account')

    return render(request, 'tracker/delete_account.html')


@login_required
def reading_history_global(request):
    """Historique global de lecture de l'utilisateur"""
    user = request.user

    entries = ReadingEntry.objects.filter(
        user_series__user=user
    ).select_related('user_series__series').order_by('-read_at')

    paginator = Paginator(entries, 20)
    page = request.GET.get('page')
    entries_page = paginator.get_page(page)

    context = {
        'entries': entries_page,
    }
    return render(request, 'tracker/reading_history_global.html', context)


@login_required
def profile(request):
    """Profil utilisateur"""
    user = request.user

    # Statistiques
    total_series = UserSeries.objects.filter(user=user).count()
    total_chapters_read = ReadingEntry.objects.filter(
        user_series__user=user
    ).count()

    # Favoris
    total_favorites = UserSeries.objects.filter(user=user, is_favorite=True).count()
    recent_favorites = UserSeries.objects.filter(user=user, is_favorite=True).select_related('series')[:4]

    # Score moyen
    avg_score = UserSeries.objects.filter(
        user=user, score__isnull=False
    ).aggregate(avg=Avg('score'))['avg']

    # Séries par statut
    status_stats = UserSeries.objects.filter(user=user).values('status').annotate(
        count=Count('id')
    )

    context = {
        'user': user,
        'total_series': total_series,
        'total_chapters_read': total_chapters_read,
        'total_favorites': total_favorites,
        'avg_score': round(avg_score, 1) if avg_score else None,
        'status_stats': {s['status']: s['count'] for s in status_stats},
        'recent_favorites': recent_favorites,
    }
    return render(request, 'tracker/profile.html', context)


def register(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte créé avec succès ! Bienvenue sur MangaTrack.")
            return redirect('tracker:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def password_reset_request(request):
    """Vue pour demander la réinitialisation du mot de passe"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Utiliser le SITE_URL configuré pour les liens de réinitialisation
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@mangatrack.com'),
            )
            messages.success(
                request,
                "Si un compte existe avec cet email, vous recevrez un lien pour réinitialiser votre mot de passe."
            )
            return redirect('tracker:login')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vue personnalisée pour confirmer la réinitialisation du mot de passe"""
    template_name = 'registration/password_reset_confirm.html'
    success_url = '/login/'
    post_reset_login = False

    def form_valid(self, form):
        messages.success(
            self.request,
            "Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter."
        )
        return super().form_valid(form)


# Vues pour les sites de lecture
@login_required
def list_sites(request):
    """Liste des sites de lecture"""
    sites = ReadingSite.objects.all()
    is_superuser = request.user.is_superuser
    return render(request, 'tracker/list_site.html', {
        'sites': sites,
        'is_superuser': is_superuser
    })


@login_required
def add_site(request):
    """Ajouter un site de lecture (réservé aux superusers)"""
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission d'ajouter un site.")
        return redirect('tracker:list_sites')

    if request.method == 'POST':
        form = ReadingSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.created_by = request.user
            site.save()
            messages.success(request, f"Le site {site.name} a été ajouté avec succès.")
            return redirect('tracker:list_sites')
    else:
        form = ReadingSiteForm()

    return render(request, 'tracker/site_form.html', {
        'form': form,
        'title': 'Ajouter un site de lecture'
    })


@login_required
def edit_site(request, site_id):
    """Modifier un site de lecture (réservé aux superusers)"""
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission de modifier un site.")
        return redirect('tracker:list_sites')

    site = get_object_or_404(ReadingSite, id=site_id)

    if request.method == 'POST':
        form = ReadingSiteForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le site {site.name} a été modifié avec succès.")
            return redirect('tracker:list_sites')
    else:
        form = ReadingSiteForm(instance=site)

    return render(request, 'tracker/site_form.html', {
        'form': form,
        'title': f'Modifier {site.name}',
        'site': site
    })


@login_required
def delete_site(request, site_id):
    """Supprimer un site de lecture (réservé aux superusers)"""
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission de supprimer un site.")
        return redirect('tracker:list_sites')

    site = get_object_or_404(ReadingSite, id=site_id)

    if request.method == 'POST':
        site_name = site.name
        site.delete()
        messages.success(request, f"Le site {site_name} a été supprimé avec succès.")
        return redirect('tracker:list_sites')

    return render(request, 'tracker/site_confirm_delete.html', {
        'site': site
    })
