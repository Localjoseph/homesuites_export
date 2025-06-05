# HomeSuites - Application de location de propriétés

Une application web développée avec Django pour permettre aux utilisateurs de publier, rechercher et réserver des hébergements.

## Caractéristiques

- Authentification des utilisateurs
- Gestion des propriétés
- Système de réservation
- Recherche et filtrage des propriétés
- Interface responsive avec Bootstrap

## Installation

1. **Prérequis**
- Python 3.10+
- pip

2. **Installation**
```bash
git clone https://github.com/Localjoseph/homesuites_export.git
cd homesuites_export
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Technologies

- Backend: Django
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Base de données: SQLite
