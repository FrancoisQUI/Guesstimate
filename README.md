# Timeline CardGame

Un jeu de société multijoueur en ligne inspiré du célèbre jeu *Timeline*. Les joueurs doivent placer des cartes (événements historiques, inventions, films, etc.) dans le bon ordre chronologique ou selon d'autres critères numériques (budget, recettes au box-office, etc.).

## 🚀 Fonctionnalités

*   **Multijoueur en temps réel** : Jouez avec vos amis dans des salons privés synchronisés par WebSockets.
*   **Plusieurs thèmes et attributs** : Jouez avec les dates de sorties de films (MCU, Disney), l'année d'inventions historiques, etc.
*   **Deux modes de jeu** : 
    *   **Classique** : Le but est d'être le premier joueur à vider sa main en plaçant correctement toutes ses cartes.
    *   **Marathon** : Un mode axé sur le score total, visant à faire le plus grand nombre de placements corrects d'affilée.
*   **Paramètres personnalisés** : L'hôte du salon peut configurer la taille de la main de départ, la taille du deck, les thèmes et l'attribut de victoire avant de commencer.

## 🛠️ Stack Technique

*   **Frontend** : Vue 3, Vite, Tailwind CSS, Pinia (State Management).
*   **Backend** : Python 3, FastAPI, WebSockets, SQLAlchemy (SQLite).


## 📦 Installation et Lancement

### Prérequis
*   [Node.js](https://nodejs.org/) (pour Vue.js / Vite)
*   [Python 3.9+](https://www.python.org/)

### Lancement Rapide (Windows)

Si vous êtes sous Windows, vous pouvez lancer l'intégralité du projet en double-cliquant simplement sur le script situé à la racine :

```cmd
run_game.bat
```
*(Ce script démarre le serveur backend et le serveur frontend et ouvre automatiquement l'application dans votre navigateur par défaut).*

---

### Lancement Manuel

Si vous préférez démarrer les services manuellement ou que vous êtes sur Mac/Linux :

**1. Lancer le Backend (API & WebSockets)**
```bash
cd backend
python -m venv venv
# Activer l'environnement virtuel (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
```
Le backend sera accessible sur `http://localhost:8000`.

**2. Lancer le Frontend (Interface Utilisateur)**
```bash
cd frontend
npm install
npm run dev
```
L'application sera accessible sur `http://localhost:5173`.


## 📝 Notes de développement

* Le comportement des WebSockets est défini dans `backend/main.py` à l'aide de la classe `ConnectionManager`.
* La logique de l'interface et du plateau de jeu est concentrée sur `frontend/src/views/GameRoom.vue` et le store centralisé `frontend/src/store/game.js`.
