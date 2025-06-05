# HomeSuites - Application de location de propriétés style Airbnb

Une application web développée avec Django pour permettre aux utilisateurs de publier, rechercher et réserver des hébergements, similaire à Airbnb.

## Caractéristiques

- Authentification des utilisateurs (inscription, connexion, profil)
- Gestion des propriétés (création, modification, suppression)
- Système de réservation
- Recherche et filtrage des propriétés
- Interface responsive avec Bootstrap

## Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
   ```
   git clone <URL_DU_DEPOT>
   cd rental_project
   ```

2. **Créer un environnement virtuel**
   ```
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```
   pip install django django-crispy-forms django-widget-tweaks pillow
   ```

5. **Configurer la base de données**
   ```
   python manage.py migrate
   ```

6. **Créer un super utilisateur**
   ```
   python manage.py createsuperuser
   ```

7. **Créer les aménités de base**
   ```
   python manage.py shell -c "from properties.models import Amenity; amenities = ['Wi-Fi', 'Air Conditioning', 'Kitchen', 'Heating', 'Washer', 'Dryer', 'Free Parking', 'TV', 'Pool', 'Hot Tub', 'Gym', 'Breakfast']; [Amenity.objects.get_or_create(name=amenity) for amenity in amenities]; print('Amenities created successfully!')"
   ```

8. **Lancer le serveur de développement**
   ```
   python manage.py runserver
   ```

9. **Accéder à l'application**
   Ouvrez votre navigateur et accédez à `http://127.0.0.1:8000/`

## Structure du Projet

- **users** : Gestion des utilisateurs et profils
- **properties** : Gestion des annonces de location
- **bookings** : Gestion des réservations
- **templates** : Fichiers HTML
- **static** : Fichiers CSS, JavaScript, images

## Utilisation

1. Créez un compte utilisateur ou connectez-vous
2. Parcourez les propriétés disponibles
3. Créez votre propre annonce en tant qu'hôte
4. Réservez des séjours en tant qu'invité

## Technologies utilisées

- **Backend** : Django
- **Frontend** : HTML, CSS, JavaScript, Bootstrap
- **Base de données** : SQLite (par défaut)
- **Dépendances** : Pillow, django-crispy-forms, django-widget-tweaks