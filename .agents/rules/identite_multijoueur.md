---
trigger: always_on
---

Pour permettre le test de plusieurs joueurs sur un même navigateur, les informations d'identification (clientId, nickname, etc.) doivent impérativement être stockées dans le `sessionStorage` et non dans le `localStorage`. Chaque onglet doit être traité comme une session joueur unique et indépendante.
