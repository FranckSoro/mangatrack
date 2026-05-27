# MangaTrack — Contexte Projet pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Il contient tout le contexte nécessaire pour reprendre le projet sans explication.

---

## 1. Description du projet

Application web Django permettant à des utilisateurs de suivre leur lecture de mangas, manhwas et manhuas.
L'utilisateur peut ajouter des séries, enregistrer chaque chapitre lu, attribuer un statut et une note, et consulter un dashboard récapitulatif.

- Usage d'abord **personnel**, mais architecture **multi-utilisateurs dès le départ**
- **Aucun CMS** — toutes les données sont saisies manuellement
- Rendu **Django Templates classiques** (pas de SPA, pas de React)

---

## 2. Stack technique

| Composant         | Technologie                              |
|-------------------|------------------------------------------|
| Backend           | Django 6.0.4                             |
| Base de données   | Supabase PostgreSQL (via psycopg2)        |
| Stockage médias   | AWS S3 Storage (via django-storages)    |
| Auth              | Django Auth natif (session-based, pas JWT)|
| UI Framework      | Tailwind CSS + DaisyUI                   |
| Rendu             | Django Templates (classique)             |
| ORM               | Django ORM (psycopg2)                    |
| Upload fichiers   | Django ImageField (AWS S3)               |
| Hébergement cible | Vercel (déployé sur mangatrackk.vercel.app) |

### Notes Supabase importantes
- Django se connecte à Supabase PostgreSQL via **psycopg2** — connexion standard, **pas de SDK Supabase**
- Stockage médias sur **AWS S3 Storage** (via django-storages + boto3)
- **Pas d'auth Supabase côté client** — Django Auth natif gère les sessions

### Notes AWS S3 importantes
- Stockage des médias (couvertures, logos) sur AWS S3
- Configuration via variables d'environnement AWS_*
- Bucket sans ACLs (politique de bucket pour l'accès public)
- URLs signées avec expiration de 1h

---

## 3. Structure du projet

```
mangatrack/
├── CLAUDE.md
├── .env                      # Variables d'environnement (racine)
│
├── src/                      # Dossier source principal
│   ├── manage.py
│   ├── config/               # Configuration Django
│   │   ├── settings.py       # Configuration principale
│   │   ├── urls.py           # URLs racines
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   └── .env              # Variables d'environnement locales
│   │
│   ├── theme/                # App Tailwind + DaisyUI
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── templates/
│   │   │   └── base.html     # Layout DaisyUI principal
│   │   ├── static_src/       # Source Tailwind (node_modules/)
│   │   │   ├── .gitignore
│   │   │   ├── package.json
│   │   │   ├── postcss.config.js
│   │   │   └── src/
│   │   │       └── styles.css
│   │   └── node_modules/     # Dépendances Node.js
│   │
│   ├── tracker/              # App métier principale
│   │   ├── admin.py         # Admin Django configuré (Genre, Series, UserSeries, ReadingEntry, ReadingSite)
│   │   ├── apps.py
│   │   ├── forms.py         # SeriesForm, UserSeriesForm, ReadingEntryForm, ReadingSiteForm
│   │   ├── models.py        # Genre, Series, UserSeries, ReadingEntry, ReadingSite
│   │   ├── urls.py
│   │   ├── views.py         # 23 vues avec @login_required
│   │   ├── __init__.py
│   │   ├── tests.py         # Tests (à implémenter)
│   │   ├── fixtures/
│   │   │   └── genres.json   # 20 genres prépopulés
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_alter_series_slug.py
│   │   │   ├── 0003_alter_series_total_chapters.py
│   │   │   └── 0004_readingsite.py
│   │   └── templates/
│   │       └── tracker/
│   │           ├── dashboard.html
│   │           ├── library.html
│   │           ├── reading_history.html
│   │           ├── reading_history_global.html
│   │           ├── series_confirm_delete.html
│   │           ├── series_detail.html
│   │           ├── series_form.html
│   │           ├── profile.html
│   │           ├── edit_profile.html
│   │           ├── change_password.html
│   │           ├── delete_account.html
│   │           ├── reading_entry_confirm_delete.html
│   │           ├── list_site.html
│   │           ├── site_form.html
│   │           └── site_confirm_delete.html
│   │
│   ├── templates/            # Templates globaux
│   │   ├── base.html
│   │   └── registration/
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── logged_out.html
│   │       ├── password_reset_form.html
│   │       ├── password_reset_email.html
│   │       ├── password_reset_confirm.html
│   │       └── password_reset_subject.txt
│   │
│   └── static/               # Fichiers statiques globaux
│       └── img/
│           ├── favicon.svg
│           ├── favicon.ico
│           └── apple-touch-icon.png
│
└── mediafiles/               # Stockage local des images (déplacé vers AWS S3)
```

---

## 3.1 Fichiers statiques

### Favicons
Les favicons sont situés dans `src/static/img/` et utilisent les couleurs DaisyUI du thème :
- **Primary**: `rgb(0, 82, 180)` — bleu (correspond à `--color-primary:oklch(45% .24 277.023)`)
- **Secondary**: `rgb(255, 66, 142)` — rose (correspond à `--color-secondary:oklch(65% .241 354.308)`)

**Fichiers disponibles :**
- `favicon.svg` — Format vectoriel SVG avec dégradé
- `favicon.ico` — Format ICO avec multiples tailles (16x16, 32x32, 48x48, 64x64)
- `apple-touch-icon.png` — Format PNG pour iOS (180x180)

**Style :**
- Fond avec dégradé `from-primary to-secondary`
- Coins arrondis
- Lettre "M" blanche centrée
- Correspond exactement au logo dans la sidebar

**Pour régénérer les favicons :**
```bash
python create_favicon.py
python manage.py collectstatic --noinput
```

---

## 4. Modèles de données

### Genre
```python
name = CharField(max_length=100, unique=True)
slug = SlugField(unique=True)
# Prépopulé en fixtures (20 genres)
```

### Series
```python
title = CharField(max_length=200)
slug = SlugField(max_length=200, unique=True, blank=True)
series_type = CharField(max_length=10)  # manga / manhwa / manhua
author = CharField(max_length=200)
cover = ImageField(upload_to='covers/', blank=True, null=True)
total_chapters = PositiveIntegerField(null=True, blank=True)
genres = ManyToManyField(Genre, blank=True)
created_by = ForeignKey(User, related_name='created_series')
created_at = DateTimeField(auto_now_add=True)
# Série partagée entre users — created_by = créateur initial
# total_chapters nullable (optionnel)
# Méthode cover_url() pour générer l'URL de l'image
```

### UserSeries
```python
user = ForeignKey(User, related_name='library')
series = ForeignKey(Series, related_name='user_series')
status = CharField(max_length=20)  # en_cours / termine / pause / abandonne
is_favorite = BooleanField(default=False)
score = IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
notes = TextField(blank=True, null=True)
added_at = DateTimeField(auto_now_add=True)
# unique_together: (user, series) — isolation totale par user
# indexes: (user, status), (user, is_favorite)
# Méthodes: last_chapter_read(), total_chapters_read()
```

### ReadingEntry
```python
user_series = ForeignKey(UserSeries, related_name='reading_entries')
chapter_number = PositiveIntegerField()
read_at = DateTimeField(auto_now_add=True)
# Historique complet — dernier chapitre = MAX(chapter_number), jamais stocké
# index: (user_series, -chapter_number)
```

### ReadingSite
```python
name = CharField(max_length=200, unique=True)
url = URLField(max_length=500)
logo = ImageField(upload_to='site_logos/', blank=True, null=True)
description = TextField(blank=True, null=True)
created_by = ForeignKey(User, related_name='created_sites')
created_at = DateTimeField(auto_now_add=True)
# Sites de lecture de manga/manhwa/manhua
# Ajout/modification/suppression réservés aux superusers
# Méthode logo_url() pour générer l'URL de l'image
# Options: verbose_name='Site de lecture', verbose_name_plural='Sites de lecture', ordering=['name']
```

### Relations
- `User` → `UserSeries` (one-to-many)
- `Series` → `UserSeries` (one-to-many) — une série peut être dans plusieurs bibliothèques
- `UserSeries` → `ReadingEntry` (one-to-many, CASCADE à la suppression)
- `Series` → `Genre` (many-to-many)

---

## 5. Règles métier clés

| Règle | Description |
|-------|-------------|
| Isolation utilisateur | Toutes les vues filtrent sur `request.user` — jamais de données croisées |
| Unicité UserSeries | `unique_together: (user, series)` — un user ne peut ajouter une série qu'une seule fois |
| Dernier chapitre lu | `MAX(chapter_number)` des ReadingEntry — calculé via ORM, **jamais stocké** |
| Upload couverture | Stockage sur AWS S3 (via django-storages + boto3) |
| Score optionnel | `null=True, blank=True` — une série peut exister sans note |
| total_chapters optionnel | `null=True, blank=True` — peut être laissé vide lors de l'ajout |
| Suppression en cascade | Suppression UserSeries → supprime tous ses ReadingEntry |
| Auth obligatoire | `@login_required` sur toutes les vues métier — redirect vers `/dashboard/` |
| Logout POST | Déconnexion via POST avec CSRF token (pas de GET) |
| Suppression compte | Nécessite de taper le nom d'utilisateur pour confirmer |
| Genres prépopulés | 20 genres chargés via fixtures au démarrage |
| Slug auto-généré | Slug généré automatiquement à partir du titre si non fourni |
| Sites de lecture | Ajout/modification/suppression réservés aux superusers |
| Admin Django | Configuré avec inlines, filtres, et champs calculés |

---

## 6. Fonctionnalités implémentées

### ✅ Authentification
- Inscription (`register`) avec formulaire personnalisé incluant email
- Connexion (`login`) avec champs de même largeur
- Déconnexion (`logout`) via POST avec CSRF
- Django Auth natif (session-based)
- **Réinitialisation du mot de passe** (`password_reset`, `password_reset_confirm`)
- **Email de réinitialisation** avec template personnalisé
- **CustomPasswordResetConfirmView** pour la confirmation
- UI responsive optimisée pour les formulaires d'authentification

### ✅ Dashboard
- Statistiques globales (total séries, chapitres lus, score moyen)
- Séries par statut
- Favoris récents
- Activité récente

### ✅ Bibliothèque
- Liste paginée (12 par page)
- Filtres: statut, type, favoris
- Recherche par titre
- Tri: titre, date d'ajout, score
- Grille responsive avec couvertures
- Badges de statut colorés

### ✅ Gestion des séries
- Ajout de série (formulaire avec upload couverture, genres)
- Détail de série (progression, historique, infos)
- Édition UserSeries (statut, favori, note, notes)
- Édition Series (titre, type, auteur, couverture, genres, total_chapters)
- Suppression avec confirmation
- Genres prépopulés (20 genres via fixtures)
- UI optimisée pour le formulaire de série (section "Couverture" compacte)

### ✅ Tracker de lecture
- Ajout de chapitre lu
- Historique paginé (20 par page)
- Historique global de lecture
- Suppression d'entrées d'historique (avec confirmation)
- Dernier chapitre calculé via ORM
- Progression visuelle (barre de progression)

### ✅ Profil utilisateur
- Page de profil avec statistiques
- Total séries, chapitres lus, favoris
- Score moyen
- Séries par statut
- Favoris récents
- Modification du profil (username, email)
- Changement de mot de passe
- Suppression du compte (avec confirmation)

### ✅ Sites de lecture
- Liste des sites de lecture (accessible à tous les utilisateurs connectés)
- Ajout de site (réservé aux superusers)
- Modification de site (réservé aux superusers)
- Suppression de site (réservé aux superusers)
- Grille responsive avec logos et descriptions
- Liens externes vers les sites

### ✅ Admin Django
- Interface d'administration configurée
- GenreAdmin avec comptage de séries
- SeriesAdmin avec inlines et champs calculés
- UserSeriesAdmin avec progression visuelle
- ReadingEntryAdmin avec filtres et recherche
- ReadingSiteAdmin avec aperçu de logo
- Personnalisation de l'interface (header, title, index_title)

---

## 7. État du projet

### Fonctionnalités MVP
| Fonctionnalité | État |
|----------------|------|
| Authentification | ✅ Complet |
| CRUD séries | ✅ Complet |
| Tracker chapitres | ✅ Complet |
| Dashboard | ✅ Complet |
| UI responsive | ✅ Complet |
| Recherche | ✅ Complet |
| Tri | ✅ Complet |
| Profil utilisateur | ✅ Complet |
| Gestion du compte | ✅ Complet |
| Historique de lecture | ✅ Complet |
| Suppression d'historique | ✅ Complet |
| Genres | ✅ Complet |
| Sites de lecture | ✅ Complet |
| Admin Django | ✅ Complet |
| Réinitialisation mot de passe | ✅ Complet |
| AWS S3 Storage | ✅ Complet |
| Optimisation UI | ✅ En cours |
| Responsive design formulaires | ✅ Complet |
| Validation visuelle mot de passe (animation) | ✅ v1.7.0 |

### Fonctionnalités futures
| Fonctionnalité | État |
|----------------|------|
| Tests unitaires | ❌ À faire |
| API REST | ❌ À faire |
| API MangaDex | ❌ À faire |
| Notifications | ⏳ En cours |
| Optimisation UI continue | ✅ v1.8.0 |
| Améliorations responsive | ✅ v1.5.0 |
| Validation mot de passe visuelle | ✅ v1.7.0 |

### HTMX Implementation
| Fonctionnalité | État |
|----------------|------|
| Intégration HTMX de base | ✅ v1.8.0 |
| Toggle favoris (card/detail) | ✅ v1.8.0 |
| Ajout chapitre avec toast | ✅ v1.8.0 |
| Filtrage bibliothèque dynamique | ✅ v1.8.0 |
| Recherche en temps réel | ✅ v1.8.0 |

**Notes HTMX (v1.8.0)** :
- HTMX est maintenant entièrement fonctionnel sans bugs
- Les formulaires utilisent `hx-post` avec gestion d'erreurs côté serveur
- Les réponses HTMX incluent des en-têtes `HX-Trigger` pour les notifications
- La bibliothèque supporte la pagination HTMX via `hx-get` sur les liens
- Les boutons de favoris utilisent `hx-swap="outerHTML"` pour un affichage instantané

---

## 8. Variables d'environnement

### `.env` (racine)
```env
SECRET_KEY=django-insecure-*
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,mangatrackk.vercel.app
DATABASE_URL=postgresql://postgres.pwcosoziibpefwqyfuue:6YihxbsCHcGzKEMi@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
MEDIA_URL=/media/
MEDIA_ROOT=mediafiles
```

### `src/config/.env` (local)
```env
SECRET_KEY=django-insecure-*
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,mangatrackk.vercel.app
DATABASE_URL=postgresql://postgres.pwcosoziibpefwqyfuue:6YihxbsCHcGzKEMi@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
MEDIA_URL=/media/
MEDIA_ROOT=mediafiles
```

### Variables AWS S3 Storage (configuré)
```.env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="eu-west-3")
AWS_S3_FILE_OVERWRITE = False       # Ne pas écraser les fichiers dupliqués
AWS_DEFAULT_ACL = None              # Sécurité : pas d'accès public par défaut
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 3600        # 1h d'expiration
AWS_S3_VERIFY = True
```

### Variables Email Configuration (réinitialisation mot de passe - configuré)
```.env
# Email Configuration
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@mangatrack.com")

# Site URL pour les liens de réinitialisation
SITE_URL = env("SITE_URL", default="http://127.0.0.1:8000")
```

---

## 9. Points d'amélioration

### 1. **Tests**
- Aucun test unitaire/intégration
- À ajouter pour assurer la qualité

### 2. **Toggle favoris sans JS**
- Actuellement nécessite un POST → pourrait être amélioré avec HTMX ou JS

### 3. **Validation avancée**
- Validation du numéro de chapitre (ex: ne peut pas dépasser total_chapters)
- Validation de l'image (taille, format)

### 4. **Notifications**
- Section notifications présente mais non implémentée
- À implémenter pour les alertes de nouveaux chapitres

### 5. **Bug dans add_chapter** ✅ CORRIGÉ (v1.7.1)
- ~~Référence à `pk` qui n'existe pas à la ligne 278 de views.py~~
- Corrigé : `return redirect('tracker:series_detail', slug=slug)`

---

## 10. Prochaines étapes suggérées

1. **Ajouter des tests**
   - Tests unitaires pour les modèles
   - Tests d'intégration pour les vues
   - Tests de formulaire

2. **Améliorer l'UX**
   - Toggle favoris avec HTMX
   - Ajouter des animations de transition
   - Continuer l'optimisation de l'interface utilisateur

3. **Implémenter les notifications**
   - Système de notifications pour les nouveaux chapitres
   - Préférences de notification par utilisateur
   - Email de notification

4. **Optimiser le déploiement**
   - Configurer `collectstatic` pour Vercel
   - Mettre à jour les variables d'environnement
   - Optimiser les images pour le web

## 11. URLs principales

| URL | Vue | Description |
|-----|-----|-------------|
| `/` | `dashboard` | Dashboard utilisateur |
| `/library/` | `library` | Bibliothèque avec filtres |
| `/library/add/` | `add_series` | Ajouter une série |
| `/library/<slug>/` | `series_detail` | Détail d'une série |
| `/library/<slug>/edit/` | `edit_user_series` | Éditer UserSeries |
| `/library/<slug>/edit-info/` | `edit_series` | Éditer Series |
| `/library/<slug>/delete/` | `delete_user_series` | Supprimer une série |
| `/library/<slug>/add-chapter/` | `add_chapter` | Ajouter un chapitre lu |
| `/library/<slug>/history/` | `reading_history` | Historique d'une série |
| `/library/<slug>/history/<id>/delete/` | `delete_reading_entry` | Supprimer une entrée |
| `/history/` | `reading_history_global` | Historique global |
| `/profile/` | `profile` | Profil utilisateur |
| `/profile/edit/` | `edit_profile` | Modifier le profil |
| `/profile/change-password/` | `change_password` | Changer le mot de passe |
| `/profile/delete/` | `delete_account` | Supprimer le compte |
| `/login/` | `login` | Connexion |
| `/logout/` | `logout` | Déconnexion |
| `/register/` | `register` | Inscription |
| `/password-reset/` | `password_reset` | Demander la réinitialisation du mot de passe |
| `/password-reset/<uidb64>/<token>/` | `password_reset_confirm` | Confirmer et réinitialiser le mot de passe |
| `/sites/` | `list_sites` | Liste des sites de lecture |
| `/sites/add/` | `add_site` | Ajouter un site de lecture (superuser) |
| `/sites/<id>/edit/` | `edit_site` | Modifier un site de lecture (superuser) |
| `/sites/<id>/delete/` | `delete_site` | Supprimer un site de lecture (superuser) |
| `/admin/` | `admin` | Interface d'administration Django |

---

## 12. Fonctionnalités futures (hors MVP)

- Connexion API MangaDex pour auto-complétion à l'ajout
- Notifications email — nouveaux chapitres
- Profil public et bibliothèque partageable
- Import / export CSV
- Recommandations basées sur les genres favoris
- API REST publique (DRF)
- PWA avec support offline
- Système social : amis, comparaison de bibliothèques
- Système de commentaires sur les séries
- Listes personnalisées (to-read, reading-list, etc.)
- Statistiques avancées (temps de lecture, genres préférés, etc.)

## 13. Fichiers de configuration

### `.gitignore`
- Exclut les fichiers Python compilés
- Exclut les fichiers de base de données
- Exclut les fichiers d'environnement
- Exclut les médias et fichiers statiques

### `requirements.txt`
- Django 6.0.4
- psycopg2-binary
- django-storages
- boto3
- django-environ
- whitenoise
- Autres dépendances

### `README.md`
- Documentation complète du projet
- Instructions d'installation
- Guide d'utilisation
- Structure du projet

### `CONTRIBUTING.md`
- Guide pour les contributeurs
- Processus de développement
- Conventions de code

### `LICENSE`
- Licence MIT

### `.env.example`
- Exemple de configuration des variables d'environnement

---

## 14. Admin Django

L'interface d'administration Django est configurée avec les modèles suivants :

### GenreAdmin
- list_display: name, slug, series_count
- prepopulated_fields: slug
- search_fields: name
- ordering: name

### SeriesAdmin
- list_display: title, series_type, author, total_chapters, readers_count, avg_score, created_by, created_at
- list_filter: series_type, genres, created_by, created_at
- search_fields: title, author
- filter_horizontal: genres
- readonly_fields: slug, created_at, cover_preview
- prepopulated_fields: slug
- date_hierarchy: created_at
- inlines: UserSeriesInline
- Champs calculés: readers_count, avg_score, cover_preview

### UserSeriesAdmin
- list_display: user, series, status, is_favorite, score, progress, added_at
- list_filter: status, is_favorite, score, added_at
- search_fields: user__username, user__email, series__title, series__author
- raw_id_fields: user, series
- readonly_fields: added_at, last_chapter_read, total_chapters_read
- date_hierarchy: added_at
- inlines: ReadingEntryInline
- Champs calculés: progress, last_chapter_read, total_chapters_read

### ReadingEntryAdmin
- list_display: user, series, chapter_number, read_at
- list_filter: read_at, chapter_number
- search_fields: user_series__user__username, user_series__series__title
- raw_id_fields: user_series
- readonly_fields: read_at, user, series
- date_hierarchy: read_at

### ReadingSiteAdmin
- list_display: name, url, logo_preview, created_by, created_at
- list_filter: created_at, created_by
- search_fields: name, url, description
- readonly_fields: created_at, logo_preview, created_by
- date_hierarchy: created_at
- Champs calculés: logo_preview

### Personnalisation
- site_header: 'MangaTrack Administration'
- site_title: 'MangaTrack'
- index_title: 'Bienvenue dans l\'administration de MangaTrack'

---

## 16. Formulaires

### CustomUserCreationForm
- Formulaire d'inscription personnalisé
- Champs: username, email, password1, password2
- Email requis et sauvegardé lors de la création
- Hérite de UserCreationForm de Django
- **Défini dans `views.py`** (pas dans `forms.py`)

### SeriesForm
- Formulaire d'ajout/édition d'une série
- Champs: title, series_type, author, cover, total_chapters, genres
- Widgets avec classes Tailwind (input, select, checkbox)
- total_chapters non requis
- Section "Couverture" optimisée avec file-input DaisyUI natif
- Prévisualisation miniature intégrée en mode édition

### UserSeriesForm
- Formulaire d'édition d'une série dans la bibliothèque
- Champs: status, is_favorite, score, notes
- Widgets avec classes Tailwind (select, checkbox, input, textarea)

### ReadingEntryForm
- Formulaire d'ajout d'un chapitre lu
- Champs: chapter_number
- Widget NumberInput avec classes Tailwind et min=1

### ReadingSiteForm
- Formulaire d'ajout/édition d'un site de lecture
- Champs: name, url, logo, description
- Widgets personnalisés avec classes Tailwind pour chaque champ

### ProfileForm
- Formulaire de modification du profil utilisateur
- Champs: username, email
- Widgets avec classes Tailwind (input, email)
- email non requis

### CustomPasswordChangeForm
- Formulaire de changement de mot de passe personnalisé
- Champs: old_password, new_password1, new_password2
- Widgets PasswordInput avec classes Tailwind
- Hérite de PasswordChangeForm de Django

---

## 17. Bugs connus

### Bug dans add_chapter ✅ CORRIGÉ (v1.7.1)
- **Problème**: ~~Référence à `pk` qui n'existe pas~~
- **Correction appliquée**: `return redirect('tracker:series_detail', slug=slug)`

### ProfileForm double définition ✅ CORRIGÉ (v1.7.1)
- **Problème**: `ProfileForm` était défini deux fois (dans `views.py` ET `forms.py`) avec des héritages différents
- **Correction**: Suppression de la redéfinition locale dans `views.py`, `forms.py` utilise désormais `forms.ModelForm` au lieu de `UserChangeForm`

### Bug Tailwind CSS ✅ CORRIGÉ (v1.4.0)
- **Problème**: Classes Tailwind générées dynamiquement via JavaScript non détectées en production
- **Cause**: JavaScript ajoutait des classes (input, select, textarea, checkbox) non présentes dans les templates
- **Correction**: Classes ajoutées directement dans les widgets Django (forms.py)
- **Impact**: Les formulaires fonctionnent maintenant correctement en production

---

## 18. Migrations

### 0001_initial.py
- Création des modèles initiaux: Genre, Series, UserSeries, ReadingEntry

### 0002_alter_series_slug.py
- Ajout du champ slug au modèle Series

### 0003_alter_series_total_chapters.py
- Modification du champ total_chapters pour le rendre nullable

### 0004_readingsite.py
- Création du modèle ReadingSite
- Champs: name, url, logo, description, created_by, created_at
- Options: verbose_name, verbose_name_plural, ordering

---

## 19. Templates

### Templates globaux
- `base.html` - Layout principal
- `registration/login.html` - Page de connexion (champs de même largeur)
- `registration/register.html` - Page d'inscription (UI responsive optimisée)
- `registration/logged_out.html` - Page de déconnexion
- `registration/password_reset_form.html` - Formulaire de demande de réinitialisation
- `registration/password_reset_email.html` - Template d'email de réinitialisation
- `registration/password_reset_confirm.html` - Formulaire de confirmation de réinitialisation
- `registration/password_reset_subject.txt` - Sujet de l'email de réinitialisation

### Templates tracker
- `dashboard.html` - Dashboard utilisateur
- `library.html` - Bibliothèque avec filtres
- `series_form.html` - Formulaire d'ajout/édition de série (UI optimisée)
- `series_detail.html` - Détail d'une série
- `series_confirm_delete.html` - Confirmation de suppression de série
- `reading_history.html` - Historique de lecture d'une série
- `reading_history_global.html` - Historique global de lecture
- `reading_entry_confirm_delete.html` - Confirmation de suppression d'entrée
- `profile.html` - Profil utilisateur
- `edit_profile.html` - Formulaire de modification de profil
- `change_password.html` - Formulaire de changement de mot de passe
- `delete_account.html` - Formulaire de suppression de compte
- `list_site.html` - Liste des sites de lecture
- `site_form.html` - Formulaire d'ajout/édition de site
- `site_confirm_delete.html` - Confirmation de suppression de site

---

## 20. Vues

### Vues principales (23 vues)
- `dashboard` - Tableau de bord avec statistiques
- `library` - Bibliothèque avec filtres et pagination
- `add_series` - Ajouter une nouvelle série
- `series_detail` - Détail d'une série
- `edit_user_series` - Éditer UserSeries
- `edit_series` - Éditer Series
- `delete_user_series` - Supprimer une série
- `add_chapter` - Ajouter un chapitre lu
- `reading_history` - Historique d'une série
- `delete_reading_entry` - Supprimer une entrée d'historique
- `reading_history_global` - Historique global de lecture
- `profile` - Profil utilisateur
- `edit_profile` - Modifier le profil
- `change_password` - Changer le mot de passe
- `delete_account` - Supprimer le compte

### Vues d'authentification
- `register` - Inscription avec CustomUserCreationForm (email sauvegardé)
- `password_reset_request` - Demander la réinitialisation du mot de passe
- `CustomPasswordResetConfirmView` - Confirmer la réinitialisation du mot de passe

### Vues pour les sites de lecture
- `list_sites` - Liste des sites de lecture
- `add_site` - Ajouter un site de lecture (superuser)
- `edit_site` - Modifier un site de lecture (superuser)
- `delete_site` - Supprimer un site de lecture (superuser)

### Classes de formulaires
- `ProfileForm` - Formulaire de modification du profil utilisateur
- `CustomUserCreationForm` - Formulaire d'inscription personnalisé avec email

---

## 21. Configuration Django

### Apps installées
- `django.contrib.admin` - Interface d'administration
- `django.contrib.auth` - Système d'authentification
- `django.contrib.contenttypes` - Types de contenu
- `django.contrib.sessions` - Gestion des sessions
- `django.contrib.messages` - Messages framework
- `django.contrib.staticfiles` - Fichiers statiques
- `tailwind` - Framework CSS Tailwind
- `theme` - App thème personnalisée
- `storages` - Stockage S3
- `tracker` - App métier principale
- `django_browser_reload` (DEBUG only) - Rechargement automatique

### Middlewares
- `django.middleware.security.SecurityMiddleware` - Sécurité
- `whitenoise.middleware.WhiteNoiseMiddleware` - Fichiers statiques
- `django.contrib.sessions.middleware.SessionMiddleware` - Sessions
- `django.middleware.common.CommonMiddleware` - Middleware commun
- `django.middleware.csrf.CsrfViewMiddleware` - Protection CSRF
- `django.contrib.auth.middleware.AuthenticationMiddleware` - Authentification
- `django.contrib.messages.middleware.MessageMiddleware` - Messages
- `django.middleware.clickjacking.XFrameOptionsMiddleware` - Protection clickjacking
- `django_browser_reload.middleware.BrowserReloadMiddleware` (DEBUG only) - Rechargement automatique

### Configuration de stockage
- `STORAGES["default"]` - S3Boto3Storage pour les médias
- `STORAGES["staticfiles"]` - CompressedManifestStaticFilesStorage pour les fichiers statiques
- `MEDIA_URL` - URL des médias (AWS S3)
- `STATIC_URL` - URL des fichiers statiques
- `STATIC_ROOT` - Racine des fichiers statiques

### Configuration email
- `EMAIL_BACKEND` - Backend d'envoi d'emails
- `EMAIL_HOST` - Serveur SMTP
- `EMAIL_PORT` - Port SMTP
- `EMAIL_USE_TLS` - Utilisation de TLS
- `EMAIL_HOST_USER` - Utilisateur SMTP
- `EMAIL_HOST_PASSWORD` - Mot de passe SMTP
- `DEFAULT_FROM_EMAIL` - Email d'expéditeur par défaut
- `SITE_URL` - URL du site pour les liens de réinitialisation

---

## 22. Fixtures

### genres.json
- 20 genres prépopulés pour les séries
- Chargement via `python manage.py loaddata genres.json`
- Genres inclus: Action, Aventure, Comédie, Drame, Fantastique, Horreur, Mystère, Romance, Science-fiction, Thriller, etc.

---

## 23. Commandes de gestion utiles

### Commandes Django
```bash
# Lancer le serveur de développement
python src/manage.py runserver

# Créer et appliquer les migrations
python src/manage.py makemigrations
python src/manage.py migrate

# Charger les fixtures
python src/manage.py loaddata genres

# Créer un superutilisateur
python src/manage.py createsuperuser

# Collecter les fichiers statiques
python src/manage.py collectstatic

# Ouvrir le shell Django
python src/manage.py shell
```

### Commandes Tailwind
```bash
# Compiler les fichiers CSS
npm run build

# Watcher les fichiers CSS en développement
npm run dev
```

### Commandes de test
```bash
# Lancer les tests (à implémenter)
python src/manage.py test
```

---

## 24. Dépendances du projet

### Dépendances Python
- `Django==6.0.4` - Framework web
- `psycopg2-binary` - Adaptateur PostgreSQL
- `django-storages` - Stockage S3
- `boto3` - SDK AWS
- `django-environ` - Gestion des variables d'environnement
- `whitenoise` - Servir les fichiers statiques
- `django-browser-reload` - Rechargement automatique (DEBUG only)

### Dépendances Node.js
- `tailwindcss` - Framework CSS
- `daisyui` - Composants UI
- `postcss` - Traitement CSS
- `autoprefixer` - Préfixes CSS automatiques

---

## 25. Performances et optimisation

### Optimisations ORM
- `select_related` pour les relations ForeignKey
- `prefetch_related` pour les relations ManyToMany
- `annotate` pour les champs calculés
- Pagination pour les listes (12 par page pour la bibliothèque, 20 pour l'historique)

### Optimisations de stockage
- Compression des fichiers statiques avec WhiteNoise
- URLs signées avec expiration de 1h pour les médias S3
- Bucket sans ACLs pour la sécurité

### Optimisations de templates
- Utilisation de `lazy` pour les évaluations différées
- Caching des requêtes fréquentes (à implémenter)
- Minification des fichiers CSS (à implémenter)

---

## 26. Sécurité

### Mesures de sécurité implémentées
- Protection CSRF via `CsrfViewMiddleware`
- Protection clickjacking via `XFrameOptionsMiddleware`
- Validation des mots de passe via `AUTH_PASSWORD_VALIDATORS`
- Isolation des données par utilisateur
- URLs signées avec expiration pour les médias S3
- Bucket S3 sans ACLs publics

### Mesures de sécurité à implémenter
- Rate limiting pour les API
- Protection contre les attaques par force brute
- Validation des entrées utilisateur
- Sanitization des données
- HTTPS obligatoire en production
- Headers de sécurité (CSP, HSTS, etc.)

---

## 27. Déploiement

### Configuration Vercel
- Déployé sur `mangatrackk.vercel.app`
- Variables d'environnement configurées
- Base de données Supabase PostgreSQL
- Stockage AWS S3 pour les médias
- Fichiers statiques servis via WhiteNoise

### Étapes de déploiement
1. Configurer les variables d'environnement
2. Exécuter les migrations
3. Collecter les fichiers statiques
4. Compiler les fichiers CSS
5. Déployer sur Vercel

### Variables d'environnement de production
- `SECRET_KEY` - Clé secrète Django
- `DEBUG=False` - Mode production
- `ALLOWED_HOSTS` - Hosts autorisés
- `DATABASE_URL` - URL de la base de données
- `AWS_ACCESS_KEY_ID` - Clé d'accès AWS
- `AWS_SECRET_ACCESS_KEY` - Clé secrète AWS
- `AWS_STORAGE_BUCKET_NAME` - Nom du bucket S3
- `AWS_S3_REGION_NAME` - Région AWS
- `EMAIL_BACKEND` - Backend d'envoi d'emails
- `EMAIL_HOST` - Serveur SMTP
- `EMAIL_PORT` - Port SMTP
- `EMAIL_USE_TLS` - Utilisation de TLS
- `EMAIL_HOST_USER` - Utilisateur SMTP
- `EMAIL_HOST_PASSWORD` - Mot de passe SMTP
- `DEFAULT_FROM_EMAIL` - Email d'expéditeur par défaut
- `SITE_URL` - URL du site pour les liens de réinitialisation

---

## 28. Tests et qualité du code

### Tests à implémenter
- Tests unitaires pour les modèles
- Tests d'intégration pour les vues
- Tests de formulaire
- Tests d'API (si implémentée)
- Tests de performance
- Tests de sécurité

### Outils de qualité de code
- `flake8` - Linter Python
- `black` - Formateur Python
- `isort` - Tri des imports
- `pylint` - Analyse de code statique
- `mypy` - Vérification de types

### Couverture de code
- Objectif: 80% de couverture
- Outil: `coverage.py`
- Rapport: HTML et JSON

---

## 29. Documentation et ressources

### Documentation Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/)

### Documentation AWS S3
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Documentation Tailwind CSS
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [DaisyUI Documentation](https://daisyui.com/docs/)

### Documentation Supabase
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase PostgreSQL Documentation](https://supabase.com/docs/guides/database)

---

## 30. Contributeurs et licence

### Contributeurs
- Soro Franck Albert - Développeur principal

### Licence
- Ce projet est sous licence MIT
- Voir le fichier LICENSE pour plus de détails

### Remerciements
- Django Team pour le framework Django
- Supabase pour l'hébergement de la base de données
- AWS pour le stockage S3
- Tailwind CSS et DaisyUI pour le framework UI
- La communauté open source pour les outils et bibliothèques utilisés

---

## 31. Changements récents et historique des versions

### Version 1.7.1 (2026-05-23)
- **Correction bug critique `add_chapter`** : `pk=pk` → `slug=slug` dans la vue `add_chapter` (`views.py`). L'ajout de chapitres fonctionne désormais correctement.
- **Suppression double définition `ProfileForm`** : `ProfileForm` était défini dans `views.py` ET `forms.py`. La redéfinition locale dans `views.py` a été supprimée. `forms.py` utilise maintenant `forms.ModelForm` au lieu de `UserChangeForm` (qui exposait un champ `password` non désiré).
- **Nettoyage imports inutilisés** dans `views.py` : suppression de `default_token_generator`, `force_str`, `urlsafe_base64_decode`, `Sum`, `F`, `SetPasswordForm`.
- **`email.required = False`** ajouté dans `ProfileForm` de `forms.py` pour cohérence avec le comportement attendu.

### Version 1.7.0 (2026-05-17)
- **Refonte complète de la validation visuelle des mots de passe** : Système d'animation fluide sur les 3 templates (`register.html`, `change_password.html`, `password_reset_confirm.html`).
- **Animation "sliding eye"** : Le bouton œil 👁 démarre à `right-3` et glisse vers `right-10` (`transition-all duration-300 ease-in-out`) quand la validation s'active, libérant l'espace pour les icônes de validation.
- **Icône ✓ verte (password-match)** : Apparaît avec animation pop-in (`@keyframes iconPopIn` : opacity + scale) quand les mots de passe correspondent. Bordure verte (`input-success`).
- **Icône ✗ rouge (password-mismatch)** : Apparaît avec la même animation quand les mots de passe ne correspondent pas. Bordure rouge (`input-error`).
- **3 états de validation** : vide (œil à droite, aucune icône), match (✓ vert + bordure verte), mismatch (✗ rouge + bordure rouge).
- **Correction alignement icônes** : Utilisation de la propriété CSS `scale` séparée au lieu de `transform: scale()` dans les `@keyframes` pour éviter les conflits avec `-translate-y-1/2` de Tailwind.
- **Icônes non-interactives** : Les icônes ✓/✗ sont des `<span>` avec `pointer-events-none` au lieu de `<button>`.
- **setTimeout 200ms** : Les icônes de validation apparaissent avec un délai de 200ms après le début du slide de l'œil pour un effet séquentiel propre.
- **Correction bug chevauchement** : Les boutons œil et ✓ ne se superposent plus dans `register.html` (ancien `right-4` → `right-3` animé).
- **Correction centrage vertical** : Ajout de `-translate-y-1/2` manquant sur les boutons œil dans `password_reset_confirm.html`.
- **Harmonisation des styles** : Couleurs œil uniformisées (`text-base-content/50 hover:text-base-content`), double espace CSS corrigé.
- **Padding inputs** : `pr-12` par défaut (compact), le texte ne passe plus sous les icônes grâce au slide de l'œil.

### Version 1.6.0 (2026-05-16)
- **Correction togglePassword change_password.html** : La fonction `togglePassword()` ciblait toujours le premier input (mot de passe actuel) au lieu du bon champ. Correction en utilisant `container.querySelector('input')` pour cibler l'input dans le conteneur parent du bouton cliqué.
- **Correction fonction vérification change_password.html** : La fonction `checkPasswordMatch()` comparait `old_password` avec `new_password1` au lieu de comparer `new_password1` avec `new_password2`. Correction en utilisant `document.querySelector('input[name="new_password1"]')` et `document.querySelector('input[name="new_password2"]')` pour cibler explicitement les nouveaux mots de passe.
- **Harmonisation espacement boutons "œil"** : Uniformisation des positions `right-4` et `right-10` sur tous les templates (register.html, change_password.html, password_reset_confirm.html) pour un espacement cohérent entre le bouton "œil" et le "V" de validation.
- **Écouteurs événements input** : Ajout d'écouteurs `input` sur les champs de nouveau mot de passe et confirmation pour la validation en temps réel dans `change_password.html`.

### Version 1.5.0 (2026-05-13)
- **Validation visuelle mot de passe** : Icône verte de confirmation quand les mots de passe correspondent
- **Responsive des formulaires** : Correction des largeurs exagérées sur tous les formulaires
- **Formulaire inscription** ([register.html](src/templates/registration/register.html)) : Icône validation ✓ + bordure verte
- **Formulaire changement mot de passe** ([change_password.html](src/tracker/templates/tracker/change_password.html)) : Icône validation ✓ + bordure verte
- **Formulaire réinitialisation mot de passe** ([password_reset_confirm.html](src/templates/registration/password_reset_confirm.html)) : Icône validation ✓ + bordure verte
- **Login** : Ajout de padding pour centrage vertical sur mobile
- **edit_profile** : Max-width ajusté à 448px (was 672px)
- **change_password** : Max-width ajusté à 448px (was 672px)
- **series_form** : Max-width ajusté à 672px (was 768px)
- **site_form/site_confirm_delete** : Max-width ajusté à 448px (was 672px)
- **series_form** : Boutons de note 1-10 responsive (flex-wrap, flex-shrink-0)
- **site_form/site_confirm_delete** : Boutons empilés sur mobile, côte à côte sur desktop
- **CSS** : Ajout de classe `.input-success` pour bordure verte de validation

### Version 1.4.0 (2026-05-09)
- **Correction critique** : Classes Tailwind générées dynamiquement via JavaScript
- Ajout des classes Tailwind directement dans les widgets Django (forms.py)
- Création de CustomPasswordChangeForm pour le formulaire de changement de mot de passe
- Suppression du JavaScript dynamique dans les templates (series_form.html, edit_profile.html, change_password.html, series_detail.html)
- Correction des chemins de compilation CSS dans package.json (src/staticfiles au lieu de src/theme/static)
- Les formulaires fonctionnent maintenant correctement en production

### Version 1.3.0 (2026-05-09)
- Ajout d'un effet toggle sur la section "Filtres" dans library.html
- Utilisation du composant collapse-arrow de DaisyUI pour un meilleur UX
- Les filtres sont maintenant repliables pour gagner de l'espace

### Version 1.2.0 (2026-05-09)
- Correction du bug : email non sauvegardé lors de l'inscription
- Création de CustomUserCreationForm avec champ email requis
- Optimisation UI du formulaire de login (champs de même largeur)
- Optimisation responsive du formulaire d'inscription (conditions d'utilisation)
- Réduction du padding et espacement pour éviter les débordements

### Version 1.1.0 (2026-05-09)
- Refonte de la section "Couverture" dans le formulaire de série
- Optimisation de l'UI pour une meilleure intégration avec les autres champs
- Utilisation de file-input DaisyUI natif pour un rendu cohérent
- Prévisualisation miniature intégrée dans le label en mode édition
- Simplification du JavaScript pour le file upload

### Version 1.0.0 (2026-05-08)
- Implémentation complète de l'application
- Authentification avec réinitialisation de mot de passe
- CRUD séries avec upload de couvertures
- Tracker de lecture avec historique
- Dashboard avec statistiques
- Bibliothèque avec filtres et recherche
- Profil utilisateur avec gestion du compte
- Sites de lecture avec gestion par superuser
- Admin Django configuré
- AWS S3 Storage pour les médias
- Déploiement sur Vercel

### Version 0.9.0 (2026-05-07)
- Ajout du modèle ReadingSite
- Implémentation des vues pour les sites de lecture
- Configuration de l'admin Django
- Templates pour les sites de lecture

### Version 0.8.0 (2026-05-06)
- Implémentation de la réinitialisation de mot de passe
- Templates de réinitialisation de mot de passe
- Configuration email

### Version 0.7.0 (2026-05-05)
- Implémentation de l'historique global de lecture
- Suppression d'entrées d'historique
- Amélioration de la bibliothèque

### Version 0.6.0 (2026-05-04)
- Implémentation du profil utilisateur
- Modification du profil
- Changement de mot de passe
- Suppression du compte

### Version 0.5.0 (2026-05-03)
- Implémentation du dashboard
- Statistiques globales
- Séries par statut
- Favoris récents
- Activité récente

### Version 0.4.0 (2026-05-02)
- Implémentation de la bibliothèque
- Filtres et recherche
- Pagination
- Tri

### Version 0.3.0 (2026-05-01)
- Implémentation du CRUD séries
- Ajout de série
- Édition de série
- Suppression de série
- Détail de série

### Version 0.2.0 (2026-04-30)
- Implémentation du tracker de lecture
- Ajout de chapitre lu
- Historique de lecture
- Progression visuelle

### Version 0.1.0 (2026-04-29)
- Initialisation du projet
- Configuration Django
- Modèles de données
- Authentification
- Templates de base

---

## 32. Problèmes connus et limitations

### Problèmes connus
- ~~Bug dans add_chapter (views.py) - Référence à `pk` qui n'existe pas~~ ✅ CORRIGÉ en v1.7.1
- Pas de tests unitaires/intégration
- Pas de système de notifications
- Toggle favoris nécessite un POST

### Limitations actuelles
- Pas d'API REST publique
- Pas d'intégration avec MangaDex
- Pas de profil public
- Pas de système social
- Pas de recommandations
- Pas d'import/export CSV
- Pas de PWA
- Pas de support offline

### Limitations techniques
- Pagination fixe (12 par page pour la bibliothèque, 20 pour l'historique)
- Pas de caching des requêtes
- Pas de minification des fichiers CSS
- Pas de compression des images
- Pas de lazy loading des images

---

## 33. Futures améliorations

### Améliorations UX
- Toggle favoris avec HTMX
- Animations de transition
- Validation des formulaires en temps réel
- Mode sombre/clair
- Thèmes personnalisables
- Raccourcis clavier
- Optimisation continue de l'interface utilisateur
- Meilleure intégration des composants DaisyUI
- Responsive design optimisé pour tous les formulaires
- Correction des débordements sur mobile

### Améliorations fonctionnelles
- Système de notifications
- Recommandations basées sur les genres favoris
- Import/Export CSV
- Profil public et bibliothèque partageable
- Système social (amis, comparaison de bibliothèques)
- Commentaires sur les séries
- Listes personnalisées (to-read, reading-list, etc.)
- Statistiques avancées (temps de lecture, genres préférés, etc.)

### Améliorations techniques
- Tests unitaires/intégration
- API REST publique (DRF)
- Intégration MangaDex
- PWA avec support offline
- Caching des requêtes
- Minification des fichiers CSS
- Compression des images
- Lazy loading des images
- Optimisation des performances

### Améliorations de sécurité
- Rate limiting
- Protection contre les attaques par force brute
- Validation des entrées utilisateur
- Sanitization des données
- HTTPS obligatoire en production
- Headers de sécurité (CSP, HSTS, etc.)

---

## 34. Ressources d'apprentissage et tutoriels

### Tutoriels Django
- [Django Tutorial - Official Documentation](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)

### Tutoriels Tailwind CSS
- [Tailwind CSS Tutorial](https://tailwindcss.com/docs/installation)
- [DaisyUI Tutorial](https://daisyui.com/docs/install/)

### Tutoriels AWS S3
- [AWS S3 Tutorial](https://docs.aws.amazon.com/s3/)
- [django-storages Tutorial](https://django-storages.readthedocs.io/)

### Tutoriels Supabase
- [Supabase Tutorial](https://supabase.com/docs/guides/getting-started)
- [Supabase PostgreSQL Tutorial](https://supabase.com/docs/guides/database)

---

## 35. Contacts et support

### Support
- Pour les questions techniques: [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- Pour les questions générales: [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)

### Signalement de bugs
- Pour signaler un bug: [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- Inclure les détails suivants:
  - Description du bug
  - Étapes pour reproduire
  - Comportement attendu
  - Comportement actuel
  - Environnement (OS, Python, Django)

### Demandes de fonctionnalités
- Pour proposer une fonctionnalité: [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- Inclure les détails suivants:
  - Description de la fonctionnalité
  - Cas d'utilisation
  - Avantages pour les utilisateurs
  - Implémentation suggérée (si applicable)

---

## 36. Remerciements et crédits

### Remerciements
- Django Team pour le framework Django
- Supabase pour l'hébergement de la base de données
- AWS pour le stockage S3
- Tailwind CSS et DaisyUI pour le framework UI
- La communauté open source pour les outils et bibliothèques utilisés

### Crédits
- Développé par Soro Franck Albert
- Design UI avec Tailwind CSS et DaisyUI
- Hébergement sur Vercel
- Base de données sur Supabase
- Stockage sur AWS S3

### Licence
- Ce projet est sous licence MIT
- Voir le fichier LICENSE pour plus de détails

---

## 37. Notes de fin et informations supplémentaires

### Notes de développement
- Ce projet a été développé avec Django 6.0.4
- L'interface utilisateur utilise Tailwind CSS et DaisyUI
- La base de données est hébergée sur Supabase PostgreSQL
- Les médias sont stockés sur AWS S3
- L'application est déployée sur Vercel

### Notes de maintenance
- Les migrations doivent être appliquées régulièrement
- Les fichiers statiques doivent être collectés après chaque déploiement
- Les variables d'environnement doivent être configurées correctement
- Les tests doivent être exécutés avant chaque déploiement

### Notes de sécurité
- Les mots de passe doivent être forts et uniques
- Les clés API doivent être conservées en sécurité
- Les données sensibles ne doivent pas être stockées en clair
- Les connexions doivent être chiffrées en production

### Notes de performance
- Les requêtes doivent être optimisées avec select_related et prefetch_related
- Les fichiers statiques doivent être compressés
- Les images doivent être optimisées
- Le caching doit être utilisé pour les requêtes fréquentes

---

**Fin du document CLAUDE.md**
