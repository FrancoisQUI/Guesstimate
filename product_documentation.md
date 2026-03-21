# Documentation Produit : Jeu de cartes multijoueur (Style Timeline/Cardline)

## 1. Vision du Produit
Créer un jeu de cartes en ligne multijoueur intuitif et personnalisable où les joueurs doivent placer à tour de rôle des cartes dans un ordre croissant ou décroissant selon un critère spécifique. Le jeu est facilement extensible grâce à un éditeur de cartes intégré et à un système de tags permettant des thématiques croisées.

## 2. Public Cible
- Joueurs occasionnels cherchant un jeu rapide entre amis (party game).
- Amateurs de jeux de culture générale, d'estimation et de déduction.

## 3. Fonctionnalités Principales

### 3.1. Gestion des Cartes et Thématiques
- **Base de Données Dynamique** : Les cartes sont stockées dans une base SQLite gérée via SQLAlchemy.
- **Système de Tags** : Permet d'associer chaque carte à plusieurs thématiques. Filtres disponibles lors de la création de partie.
- **Bibliothèque Étendue** : Plus de 400 cartes réparties sur divers thèmes :
    - **Cinéma** : MCU, Disney, Pixar, Studio Ghibli.
    - **Savoir & Culture** : Sciences & Technologies, Transports, Médecine, Communication, Objets du quotidien, Exploration Spatiale, Histoire & Archéologie.
    - **Nature** : Animaux, Littérature, Sci-Fi.
- **Attributs Variés** : Selon le thème, les cartes possèdent des attributs tels que : Année de sortie/invention, Box-office, Budget, Note IMDb, Poids, Taille, etc.

### 3.2. Mécanique de Jeu (Core Gameplay)
- **Configuration** : Le créateur du salon choisit le critère de comparaison (ex : "Box-office") et les tags.
- **Modes de Jeu** :
    - **Classique** : Style "Timeline", placement correct obligatoire pour se débarrasser de ses cartes.
    - **Complet** : Score basé sur la précision du placement pour toutes les cartes.
- **Déroulement** : Les joueurs placent leurs cartes sur une ligne chronologique/numérique. Une erreur entraîne une pioche de pénalité (en mode classique).
- **Condition de Victoire** : Premier joueur sans cartes en main (Classique) ou meilleur score (Complet).

### 3.3. Multijoueur & Social
- **Salons (Rooms)** : Création de lobbies privés avec lien de partage.
- **Stabilité Renforcée** : 
    - **Gestion d'hôte** : Seul le créateur peut lancer la partie.
    - **Migration d'hôte** : Si l'hôte quitte, le rôle est automatiquement transféré au joueur suivant.
    - **Persistance** : Utilisation du `sessionStorage` pour maintenir l'identité du joueur (`clientId`) lors des rafraîchissements.
- **Chat Intégré** : Messagerie en temps réel dans le salon.

## 4. Architecture Technique
- **Frontend** : React avec Vite.js pour la rapidité de développement et Tailwind CSS pour un design moderne et responsive.
- **Backend** : FastAPI (Python) fournissant une API REST performante et une gestion des WebSockets pour le temps réel.
- **Stockage** : SQLite (via SQLAlchemy) pour la persistance des cartes et des tags. Gestion des salons en mémoire (RAM) pour une réactivité maximale.
- **Temps Réel** : Synchronisation bidirectionnelle via WebSockets pour les actions de jeu et le chat.
