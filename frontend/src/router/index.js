import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import GameRoom from '../views/GameRoom.vue'
import Editor from '../views/Editor.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/room/:id',
      name: 'room',
      component: GameRoom
    },
    {
      path: '/editor',
      name: 'editor',
      component: Editor,
      beforeEnter: async (to, from, next) => {
        let key = sessionStorage.getItem('admin_key')
        if (!key) {
          key = window.prompt("Accès restreint. Entrez le mot de passe :")
          if (!key) return next('/')
        }
        
        try {
          const res = await fetch('http://localhost:8000/verify-admin', {
            headers: { 'X-Admin-Key': key }
          })
          if (res.ok) {
            sessionStorage.setItem('admin_key', key)
            next()
          } else {
            alert("Mot de passe incorrect")
            sessionStorage.removeItem('admin_key')
            next('/')
          }
        } catch (e) {
          alert("Erreur de connexion au serveur")
          next('/')
        }
      }
    }
  ]
})

export default router
