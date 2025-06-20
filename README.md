# **Plan d'API pour le MVP Hackathon : Gestion Participative des Déchets**

## **1. Objectif du MVP**

Créer une application fonctionnelle de gestion participative des déchets. Le but est de démontrer le cycle de vie complet d'un signalement : sa création par un citoyen, sa visualisation sur une carte par la communauté, et la possibilité d'interagir via des commentaires pour encourager l'action.

## **2. Fonctionnalités Clés (Périmètre du Hackathon)**

1.  **Signalement des Déchets :**
    * Géolocalisation (automatique ou manuelle).
    * Prise de photo.
    * Description simple (type de déchet, niveau de gravité).
    * Option de signalement anonyme ou en étant connecté.

2.  **Carte Interactive :**
    * Visualisation de tous les signalements avec des "pins".
    * Filtres essentiels : statut du signalement (signalé, nettoyé).
    * Aperçu rapide des informations en cliquant sur un pin.

3.  **Interactions Sociales Simplifiées :**
    * Ajout de commentaires sur un signalement **(par des utilisateurs authentifiés uniquement)**.

4.  **Gestion des Comptes & Gamification :**
    * Création de compte et authentification.
    * Attribution de points pour chaque signalement et commentaire.
    * Affichage d'un classement des meilleurs contributeurs.

---

## **3. Architecture de l'API REST (Plan d'Action)**

### **Endpoints & Routes**

```
# Authentification & Comptes
POST   /api/register/                 # Créer un compte utilisateur
POST   /api/login/                    # Authentification (récupérer un token JWT)
GET    /api/profile/                  # Voir son propre profil
GET    /api/users/leaderboard/        # Classement des top contributeurs

# Signalements (Reports)
GET    /api/reports/                  # Liste des signalements (avec filtres: statut, zone)
POST   /api/reports/                  # Créer un nouveau signalement
GET    /api/reports/{id}/             # Voir le détail d'un signalement
PATCH  /api/reports/{id}/             # Modifier le statut (ex: "nettoyé") (Admin ou auteur)
DELETE /api/reports/{id}/             # Supprimer un signalement (Admin ou auteur)

# Endpoint optimisé pour la carte
GET    /api/reports/map/              # **[HAUTE PRIORITÉ]** Retourne une liste légère de tous les signalements (id, lat, lng, statut)

# Commentaires (Comments)
GET    /api/reports/{report_id}/comments/  # Liste des commentaires d'un signalement (accessible à tous)
POST   /api/reports/{report_id}/comments/  # Ajouter un commentaire (authentification requise)
DELETE /api/comments/{id}/                 # Supprimer un commentaire (Admin ou auteur)
```

### **Modèles de Données (Base de Données)**

```python
# Modèle Utilisateur
User:
  - username (string)
  - email (string)
  - password (hashed string)
  - statut (string, CHOIX: 'citoyen', 'admin')
  - points (integer, default: 0)

# Modèle Signalement
Report:
  - user (relation -> User, peut être null pour l'anonymat)
  - latitude (float)
  - longitude (float)
  - photo (file/URL)
  - description (text)
  - statut (string, CHOIX: 'signalé', 'en_cours', 'nettoyé', default: 'signalé')
  - gravite (integer, CHOIX: 1:'Faible', 2:'Moyenne', 3:'Élevée')
  - created_at (datetime)

# Modèle Commentaire
Comment:
  - user (relation -> User, NON null)
  - report (relation -> Report)
  - content (text)
  - created_at (datetime)
```

## **4. Points Techniques Clés à Mettre en Place**

* **Authentification :**
    * **Méthode :** Token JWT.
    * **Librairie Suggérée (Django) :** `djangorestframework-simplejwt`.

* **Gamification :**
    * La logique d'incrémentation des points se fait côté serveur à la création réussie d'un `Report` ou d'un `Comment`.
    * L'endpoint `/api/users/leaderboard/` retourne simplement le top 10 des `User` triés par `points`.

* **Sécurité Essentielle :**
    * **CORS :** Autoriser les requêtes provenant de votre application Flutter.
    * **Permissions :**
        * Les routes de création de commentaire (`POST /.../comments/`) doivent exiger l'authentification (`IsAuthenticated`).
        * Les routes de modification/suppression (`PATCH`, `DELETE`) doivent vérifier que l'utilisateur est l'auteur de l'objet ou un administrateur.

* **Intégration Flutter :**
    * **Réseau :** Utiliser le package `dio` ou `http` pour les appels API.
    * **Stockage Token :** Utiliser `flutter_secure_storage` pour garder le token JWT en sécurité.
    * **Géolocalisation :** Package `geolocator`.
    * **Image :** Package `image_picker` pour la sélection de photos.
