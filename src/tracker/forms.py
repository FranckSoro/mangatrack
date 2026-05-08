from django import forms
from .models import Genre, Series, UserSeries, ReadingEntry, ReadingSite


class SeriesForm(forms.ModelForm):
    """Formulaire d'ajout/édition d'une série"""

    class Meta:
        model = Series
        fields = ['title', 'series_type', 'author', 'cover', 'total_chapters', 'genres']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres'].widget = forms.CheckboxSelectMultiple()
        self.fields['genres'].queryset = Genre.objects.all()
        self.fields['total_chapters'].required = False


class UserSeriesForm(forms.ModelForm):
    """Formulaire d'édition d'une série dans la bibliothèque"""
    class Meta:
        model = UserSeries
        fields = ['status', 'is_favorite', 'score', 'notes']


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
