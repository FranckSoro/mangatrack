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
| Stockage médias   | Local (mediafiles/) — à migrer vers Supabase Storage |
| Auth              | Django Auth natif (session-based, pas JWT)|
| UI Framework      | Tailwind CSS + DaisyUI                   |
| Rendu             | Django Templates (classique)             |
| ORM               | Django ORM (psycopg2)                    |
| Upload fichiers   | Django ImageField (local)                |
| Hébergement cible | Railway ou Render                        |

### Notes Supabase importantes
- Django se connecte à Supabase PostgreSQL via **psycopg2** — connexion standard, **pas de SDK Supabase**
- Stockage médias actuellement **local** (`mediafiles/`) — à migrer vers Supabase Storage
- **Pas d'auth Supabase côté client** — Django Auth natif gère les sessions

---

## 3. Structure du projet

```
mangatrack/
├── CLAUDE.md
├── entities.json
├── mangatrack_cdc.js         # Cahier des charges source
├── mempalace.yaml
├── proxy.py
├── .env                      # Variables d'environnement (racine)
│
├── src/                      # Dossier source principal
│   ├── manage.py
│   ├── config/               # Configuration Django
│   │   ├── settings.py       # Configuration principale
│   │   ├── urls.py           # URLs racines
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── .env              # Variables d'environnement locales
│   │
│   ├── theme/                # App Tailwind + DaisyUI
│   │   ├── apps.py
│   │   ├── templates/
│   │   │   └── base.html     # Layout DaisyUI principal
│   │   ├── static/           # Fichiers statiques compilés
│   │   └── static_src/       # Source Tailwind (node_modules/)
│   │
│   ├── tracker/              # App métier principale
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py         # SeriesForm, UserSeriesForm, ReadingEntryForm, ProfileForm
│   │   ├── models.py        # Genre, Series, UserSeries, ReadingEntry
│   │   ├── urls.py
│   │   ├── views.py         # 16 vues avec @login_required
│   │   ├── __init__.py
│   │   ├── fixtures/
│   │   │   └── genres.json   # 20 genres prépopulés
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_genre_slug.py
│   │   │   └── 0003_alter_series_total_chapters.py
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
│   │           └── reading_entry_confirm_delete.html
│   │
│   ├── templates/            # Templates globaux
│   │   ├── base.html
│   │   └── registration/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── logged_out.html
│   │
│   └── static/               # Fichiers statiques globaux
│
└── mediafiles/               # Stockage local des images (à migrer)
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
| Upload couverture | Stockage local (`mediafiles/covers/`) — à migrer vers Supabase Storage |
| Score optionnel | `null=True, blank=True` — une série peut exister sans note |
| total_chapters optionnel | `null=True, blank=True` — peut être laissé vide lors de l'ajout |
| Suppression en cascade | Suppression UserSeries → supprime tous ses ReadingEntry |
| Auth obligatoire | `@login_required` sur toutes les vues métier — redirect vers `/dashboard/` |
| Logout POST | Déconnexion via POST avec CSRF token (pas de GET) |
| Suppression compte | Nécessite de taper le nom d'utilisateur pour confirmer |
| Genres prépopulés | 20 genres chargés via fixtures au démarrage |
| Slug auto-généré | Slug généré automatiquement à partir du titre si non fourni |

---

## 6. Fonctionnalités implémentées

### ✅ Authentification
- Inscription (`register`)
- Connexion (`login`)
- Déconnexion (`logout`) via POST avec CSRF
- Django Auth natif (session-based)
- **Réinitialisation du mot de passe** (`password_reset`, `password_reset_confirm`)

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

### Fonctionnalités futures
| Fonctionnalité | État |
|----------------|------|
| Supabase Storage | ❌ À faire |
| Tests unitaires | ❌ À faire |
| Admin Django | ❌ À faire |
| API REST | ❌ À faire |
| API MangaDex | ❌ À faire |
| Notifications | ⏳ En cours |
| Toggle favoris HTMX | ❌ À faire |

---

## 8. Variables d'environnement

### `.env` (racine)
```env
SECRET_KEY=django-insecure-*
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres.pwcosoziibpefwqyfuue:6YihxbsCHcGzKEMi@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
MEDIA_URL=/media/
MEDIA_ROOT=mediafiles
```

### `src/config/.env` (local)
```env
SECRET_KEY=django-insecure-*
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres.pwcosoziibpefwqyfuue:6YihxbsCHcGzKEMi@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
MEDIA_URL=/media/
MEDIA_ROOT=mediafiles
```

### Variables AWS S3 Storage (à ajouter pour migration)
```.env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_FILE_OVERWRITE = False       # Ne pas écraser les fichiers dupliqués
AWS_DEFAULT_ACL = None              # Sécurité : pas d'accès public par défaut
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
```

### Variables Email Configuration (réinitialisation mot de passe)
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

### 1. **Stockage des couvertures**
- Actuellement local → pas adapté pour la prod
- À migrer vers AWS S3 Storage (S3-compatible via django-storages)
- Méthode `cover_url()` implémentée pour générer les URLs

### 2. **Toggle favoris sans JS**
- Actuellement nécessite un POST → pourrait être amélioré avec HTMX ou JS

### 3. **Pas de tests**
- Aucun test unitaire/intégration
- À ajouter pour assurer la qualité

### 4. **Validation avancée**
- Validation du numéro de chapitre (ex: ne peut pas dépasser total_chapters)
- Validation de l'image (taille, format)

### 5. **Admin Django non configuré**
- `admin.py` vide ou inexistant
- À configurer pour gérer les données

### 6. **Notifications**
- Section notifications présente mais non implémentée
- À implémenter pour les alertes de nouveaux chapitres

---

## 10. Prochaines étapes suggérées

1. **Migrer le stockage vers Supabase Storage**
   - Installer `django-storages` et `boto3`
   - Configurer les variables AWS_* pour Supabase
   - Mettre à jour `settings.py`

2. **Ajouter des tests**
   - Tests unitaires pour les modèles
   - Tests d'intégration pour les vues
   - Tests de formulaire

3. **Améliorer l'UX**
   - Toggle favoris avec HTMX
   - Ajouter des animations de transition
   - Améliorer la validation des formulaires

4. **Configurer l'admin Django**
   - Enregistrer les modèles
   - Personnaliser les listes
   - Ajouter des filtres

5. **Implémenter les notifications**
   - Système de notifications pour les nouveaux chapitres
   - Préférences de notification par utilisateur
   - Email de notification

6. **Préparer le déploiement**
   - Configurer `collectstatic`
   - Mettre à jour les variables d'environnement
   - Tester sur Railway ou Render

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
