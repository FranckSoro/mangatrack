# Contribuer à MangaTrack

Merci de votre intérêt pour contribuer à MangaTrack ! Ce document vous guidera à travers le processus de contribution.

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Processus de développement](#processus-de-développement)
- [Conventions de code](#conventions-de-code)
- [Soumission de Pull Requests](#soumission-de-pull-requests)

## 🤝 Code de conduite

En participant à ce projet, vous acceptez de respecter notre code de conduite :

- Traiter tout le monde avec respect et considération
- Être ouvert et constructif dans les discussions
- Accepter les critiques constructives
- Se concentrer sur ce qui est le mieux pour la communauté

## 💡 Comment contribuer

### Signaler des bugs

Si vous trouvez un bug :

1. Vérifiez si le bug a déjà été signalé
2. Créez une nouvelle issue avec :
   - Un titre descriptif
   - Une description détaillée du problème
   - Les étapes pour reproduire le bug
   - Le comportement attendu vs le comportement actuel
   - Captures d'écran si applicable

### Proposer des fonctionnalités

Pour proposer une nouvelle fonctionnalité :

1. Vérifiez si la fonctionnalité a déjà été demandée
2. Créez une nouvelle issue avec :
   - Un titre descriptif
   - Une description détaillée de la fonctionnalité
   - Le cas d'utilisation
   - Des exemples ou maquettes si possible

### Contribuer au code

Pour contribuer au code :

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Faites vos changements
4. Testez vos changements
5. Soumettez une Pull Request

## 🔧 Processus de développement

### 1. Fork et Clone

```bash
git clone https://github.com/votre-username/mangatrack.git
cd mangatrack
```

### 2. Créer une branche

```bash
git checkout -b feature/nom-de-la-fonctionnalite
```

### 3. Faire vos changements

- Suivez les conventions de code
- Ajoutez des tests si nécessaire
- Mettez à jour la documentation

### 4. Tester

```bash
cd src
python manage.py test
```

### 5. Commit

```bash
git add .
git commit -m "Description des changements"
```

### 6. Push et Pull Request

```bash
git push origin feature/nom-de-la-fonctionnalite
```

Ensuite, ouvrez une Pull Request sur GitHub.

## 📝 Conventions de code

### Python

- Suivez PEP 8
- Utilisez des noms descriptifs
- Ajoutez des docstrings pour les fonctions complexes
- Limitez la longueur des lignes à 100 caractères

### Django

- Utilisez les vues basées sur les classes quand approprié
- Séparez la logique métier dans les services
- Utilisez les migrations pour les changements de schéma

### Templates

- Utilisez Tailwind CSS et DaisyUI
- Gardez les templates simples et lisibles
- Utilisez les composants réutilisables

### Git

- Utilisez des messages de commit clairs
- Commitez souvent mais avec des changements logiques
- Évitez de commiter du code en cours de développement

## 📤 Soumission de Pull Requests

### Titre de la PR

Utilisez un titre descriptif :

- ✅ `feat: Ajouter la fonctionnalité de recherche`
- ✅ `fix: Corriger le bug de pagination`
- ❌ `Update code`
- ❌ `Fix stuff`

### Description de la PR

Incluez dans votre description :

- Une description des changements
- Les problèmes résolus (avec liens vers les issues)
- Des captures d'écran si applicable
- Des instructions pour tester les changements

### Checklist avant de soumettre

- [ ] Le code suit les conventions de style
- [ ] Les tests passent
- [ ] La documentation est mise à jour
- [ ] Les changements sont testés manuellement
- [ ] La description de la PR est complète

## 🎯 Types de contributions

### Documentation

- Améliorer le README
- Ajouter des exemples d'utilisation
- Traduire la documentation

### Tests

- Ajouter des tests unitaires
- Améliorer la couverture de tests
- Ajouter des tests d'intégration

### Fonctionnalités

- Implémenter de nouvelles fonctionnalités
- Améliorer les fonctionnalités existantes
- Optimiser les performances

### Bug fixes

- Corriger les bugs signalés
- Améliorer la gestion des erreurs
- Corriger les problèmes de sécurité

## 📚 Ressources

- [Documentation Django](https://docs.djangoproject.com/)
- [Guide de style PEP 8](https://peps8.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [DaisyUI](https://daisyui.com/)

## ❓ Questions

Si vous avez des questions :

- Ouvrez une issue sur GitHub
- Contactez les mainteneurs
- Consultez la documentation

---

Merci de contribuer à MangaTrack ! 🎉
