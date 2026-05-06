# MangaTrack 📚

Application web Django pour suivre votre lecture de mangas, manhwas et manhuas.

## 🌟 Fonctionnalités

- **Gestion de bibliothèque** : Ajoutez et organisez vos séries préférées
- **Suivi de lecture** : Marquez les chapitres lus et suivez votre progression
- **Statistiques** : Visualisez vos statistiques de lecture (séries, chapitres, notes)
- **Favoris** : Marquez vos séries favorites pour y accéder rapidement
- **Historique** : Consultez l'historique complet de vos lectures
- **Profils utilisateurs** : Gestion multi-utilisateurs avec profils personnalisés
- **Filtres et tri** : Recherchez et triez votre bibliothèque selon vos critères
- **Responsive Design** : Interface adaptée mobile, tablette et desktop

## 🛠 Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 6.0.4 |
| Base de données | PostgreSQL (Supabase) |
| Authentification | Django Auth (session-based) |
| UI Framework | Tailwind CSS + DaisyUI |
| ORM | Django ORM (psycopg2) |
| Stockage médias | Local (à migrer vers Supabase Storage) |

## 📁 Structure du projet

```
mangatrack/
├── src/                      # Dossier source principal
│   ├── manage.py
│   ├── config/               # Configuration Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tracker/              # App métier principale
│   │   ├── models.py        # Modèles de données
│   │   ├── views.py         # Vues et logique
│   │   ├── forms.py         # Formulaires
│   │   ├── urls.py          # URLs de l'app
│   │   └── templates/       # Templates HTML
│   └── static/              # Fichiers statiques
├── mediafiles/              # Stockage local des images
├── .env                     # Variables d'environnement
└── README.md
```

## 🚀 Installation

### Prérequis

- Python 3.10+
- PostgreSQL (ou compte Supabase)
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/mangatrack.git
cd mangatrack
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre-secret-key-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/database
MEDIA_URL=/media/
MEDIA_ROOT=mediafiles
```

5. **Exécuter les migrations**
```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

6. **Charger les fixtures de genres**
```bash
python manage.py loaddata tracker/fixtures/genres.json
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

L'application sera accessible sur `http://localhost:8000`

## 📖 Utilisation

### Premiers pas

1. **Créer un compte** : Inscrivez-vous via le formulaire d'inscription
2. **Ajouter une série** : Cliquez sur "Ajouter une série" dans votre bibliothèque
3. **Suivre votre lecture** : Marquez les chapitres lus sur la page de détail
4. **Organiser** : Utilisez les statuts (En cours, Terminé, En pause, Abandonné)
5. **Noter** : Attribuez une note de 1 à 10 à vos séries

### Fonctionnalités principales

- **Dashboard** : Vue d'ensemble de votre activité de lecture
- **Bibliothèque** : Liste de toutes vos séries avec filtres et tri
- **Détail de série** : Informations complètes et historique de lecture
- **Profil** : Statistiques personnelles et paramètres du compte

## 🗄️ Modèles de données

### Series
- Informations partagées entre tous les utilisateurs
- Champs : titre, type (manga/manhwa/manhua), auteur, couverture, genres

### UserSeries
- Série dans la bibliothèque d'un utilisateur
- Champs : statut, favori, note, notes personnelles

### ReadingEntry
- Entrée d'historique de lecture
- Champs : numéro de chapitre, date de lecture

## 🔧 Configuration

### Base de données

Le projet utilise PostgreSQL via Supabase. Pour configurer votre propre base de données :

1. Modifiez `DATABASE_URL` dans le fichier `.env`
2. Exécutez les migrations

### Stockage des médias

Actuellement, les images sont stockées localement dans `mediafiles/`. Pour migrer vers Supabase Storage :

1. Installez les dépendances :
```bash
pip install django-storages boto3
```

2. Configurez les variables d'environnement :
```env
AWS_ACCESS_KEY_ID=votre-access-key
AWS_SECRET_ACCESS_KEY=votre-secret-key
AWS_STORAGE_BUCKET_NAME=votre-bucket
AWS_S3_REGION_NAME=us-east-1
```

3. Mettez à jour `settings.py` pour utiliser `S3Boto3Storage`

## 🧪 Tests

Pour exécuter les tests :

```bash
cd src
python manage.py test
```

## 📝 Développement

### Conventions de code

- Suivez les conventions PEP 8
- Utilisez des noms descriptifs pour les variables et fonctions
- Commentez le code complexe

### Structure des vues

Toutes les vues sont décorées avec `@login_required` pour protéger l'accès.

### Templates

Les templates utilisent Tailwind CSS et DaisyUI pour le styling.

## 🚢 Déploiement

### Railway

1. Connectez votre repository GitHub à Railway
2. Configurez les variables d'environnement
3. Déployez automatiquement

### Render

1. Connectez votre repository GitHub à Render
2. Configurez les variables d'environnement
3. Déployez automatiquement

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Travail initial* - [votre-profile](https://github.com/votre-username)

## 🙏 Remerciements

- Django pour le framework web
- Tailwind CSS et DaisyUI pour le design
- Supabase pour l'hébergement de la base de données

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Note** : Ce projet est développé à des fins éducatives et personnelles.
