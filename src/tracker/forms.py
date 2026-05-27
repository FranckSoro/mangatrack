from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Genre, Series, UserSeries, ReadingEntry, ReadingSite


class SeriesForm(forms.ModelForm):
    """Formulaire d'ajout/édition d'une série"""

    class Meta:
        model = Series
        fields = ['title', 'series_type', 'author', 'cover', 'total_chapters', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Titre de la série'
            }),
            'series_type': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'author': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Auteur'
            }),
            'total_chapters': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nombre total de chapitres',
                'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres'].widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'checkbox checkbox-primary'
        })
        self.fields['genres'].queryset = Genre.objects.all()
        self.fields['total_chapters'].required = False


class UserSeriesForm(forms.ModelForm):
    """Formulaire d'édition d'une série dans la bibliothèque"""
    class Meta:
        model = UserSeries
        fields = ['status', 'is_favorite', 'score', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
            'score': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': 1,
                'max': 10,
                'placeholder': 'Note (1-10)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-32',
                'placeholder': 'Vos impressions, pensées ou mémos sur cette série'
            })
        }


class ReadingEntryForm(forms.ModelForm):
    """Formulaire d'ajout d'un chapitre lu"""
    class Meta:
        model = ReadingEntry
        fields = ['chapter_number']
        widgets = {
            'chapter_number': forms.NumberInput(attrs={
                'min': 1,
                'class': 'input input-bordered w-full',
                'placeholder': 'Numéro du chapitre'
            })
        }


class ReadingSiteForm(forms.ModelForm):
    """Formulaire d'ajout/édition d'un site de lecture"""
    class Meta:
        model = ReadingSite
        fields = ['name', 'url', 'logo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nom du site'
            }),
            'url': forms.URLInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'https://exemple.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Description du site...',
                'rows': 4
            })
        }


class ProfileForm(forms.ModelForm):
    """Formulaire de modification du profil utilisateur"""
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nom d\'utilisateur'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'votre@email.com'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulaire de changement de mot de passe personnalisé"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full pl-12 pr-12',
            'placeholder': 'Mot de passe actuel'
        })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full pl-12 pr-12',
            'placeholder': 'Nouveau mot de passe'
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full pl-12 pr-12',
            'placeholder': 'Confirmer le mot de passe'
        })
        self.fields['new_password1'].help_text = (
            "8 caractères minimum · Pas similaire à vos infos personnelles · "
            "Pas un mot de passe courant · Pas entièrement numérique"
        )
