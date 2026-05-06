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
│   │   ├── forms.py         # SeriesForm, UserSeriesForm, ReadingEntryForm
│   │   ├── models.py        # Genre, Series, UserSeries, ReadingEntry
│   │   ├── urls.py
│   │   ├── views.py         # 12 vues avec @login_required
│   │   ├── __init__.py
│   │   ├── fixtures/
│   │   │   └── genres.json   # 20 genres prépopulés
│   │   ├── migrations/
│   │   │   └── 0001_initial.py
│   │   └── templates/
│   │       └── tracker/
│   │           ├── dashboard.html
│   │           ├── library.html
│   │           ├── reading_history.html
│   │           ├── reading_history_global.html
│   │           ├── series_confirm_delete.html
│   │           ├── series_detail.html
│   │           ├── series_form.html
│   │           └── profile.html
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
series_type = CharField(max_length=10)  # manga / manhwa / manhua
author = CharField(max_length=200)
cover = ImageField(upload_to='covers/', blank=True, null=True)
total_chapters = PositiveIntegerField(default=0)
genres = ManyToManyField(Genre, blank=True)
created_by = ForeignKey(User, related_name='created_series')
created_at = DateTimeField(auto_now_add=True)
# Série partagée entre users — created_by = créateur initial
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
| Suppression en cascade | Suppression UserSeries → supprime tous ses ReadingEntry |
| Auth obligatoire | `@login_required` sur toutes les vues métier — redirect vers `/dashboard/` |
| Logout POST | Déconnexion via POST avec CSRF token (pas de GET) |

---

## 6. Fonctionnalités implémentées

### ✅ Authentification
- Inscription (`register`)
- Connexion (`login`)
- Déconnexion (`logout`) via POST avec CSRF
- Django Auth natif (session-based)

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
- Ajout de série (formulaire avec upload couverture)
- Détail de série (progression, historique, infos)
- Édition UserSeries (statut, favori, note, notes)
- Suppression avec confirmation

### ✅ Tracker de lecture
- Ajout de chapitre lu
- Historique paginé (20 par page)
- Historique global de lecture
- Dernier chapitre calculé via ORM
- Progression visuelle (barre de progression)

### ✅ Profil utilisateur
- Page de profil avec statistiques
- Total séries, chapitres lus, favoris
- Score moyen
- Séries par statut
- Favoris récents

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

### Fonctionnalités futures
| Fonctionnalité | État |
|----------------|------|
| Supabase Storage | ❌ À faire |
| Tests unitaires | ❌ À faire |
| Admin Django | ❌ À faire |
| API REST | ❌ À faire |
| API MangaDex | ❌ À faire |

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

---

## 9. Points d'amélioration

### 1. **Stockage des couvertures**
- Actuellement local → pas adapté pour la prod
- À migrer vers AWS S3 Storage (S3-compatible via django-storages)

### 2. **Toggle favoris sans JS**
- Actuellement nécessite un POST → pourrait être amélioré avec HTMX ou JS

### 3. **Pas de tests**
- Aucun test unitaire/intégration
- À ajouter pour assurer la qualité

### 4. **Pas de validation avancée**
- Pas de validation du numéro de chapitre (ex: ne peut pas dépasser total_chapters)
- Pas de validation de l'image (taille, format)

### 5. **Admin Django non configuré**
- `admin.py` vide ou inexistant
- À configurer pour gérer les données

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

4. **Configurer l'admin Django**
   - Enregistrer les modèles
   - Personnaliser les listes
   - Ajouter des filtres

5. **Préparer le déploiement**
   - Configurer `collectstatic`
   - Mettre à jour les variables d'environnement
   - Tester sur Railway ou Render

---

## 11. Fonctionnalités futures (hors MVP)

- Connexion API MangaDex pour auto-complétion à l'ajout
- Notifications email — nouveaux chapitres
- Profil public et bibliothèque partageable
- Import / export CSV
- Recommandations basées sur les genres favoris
- API REST publique (DRF)
- PWA avec support offline
- Système social : amis, comparaison de bibliothèques
