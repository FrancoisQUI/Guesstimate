<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../store/game'

const router = useRouter()
const gameStore = useGameStore()
const roomIdToJoin = ref('')
const joinError = ref('')

const animals = ['Castor', 'Pingouin', 'Hibou', 'Loutre', 'Hérisson', 'Raton Laveur', 'Écureuil', 'Blaireau', 'Tortue', 'Panda', 'Renard', 'Koala', 'Paresseux', 'Kangourou', 'Suricate'];
const adjectives = ['Malicieux', 'Cascadeur', 'Érudit', 'Bavard', 'Distrait', 'Intrépide', 'Gourmand', 'Zélé', 'Farfelu', 'Serein', 'Gaffeur', 'Savant', 'Lunatique', 'Robuste', 'Joyeux'];

const generateRandomNickname = () => {
    const animal = animals[Math.floor(Math.random() * animals.length)];
    const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
    return `${animal} ${adj}`;
}

const ensureNickname = () => {
    if (!gameStore.nickname || gameStore.nickname.trim() === '') {
        const randomName = generateRandomNickname();
        gameStore.setNickname(randomName);
    }
}

const createRoom = () => {
    ensureNickname();
    const roomId = Math.random().toString(36).substring(2, 8)
    
    router.push({
        path: `/room/${roomId}`,
        state: { isCreator: true }
    })
}

const joinRoom = async () => {
    if (roomIdToJoin.value && roomIdToJoin.value.trim() !== '') {
        ensureNickname();
        const id = roomIdToJoin.value.trim()
        
        try {
            const res = await fetch(`http://localhost:8000/rooms/${id}/exists`)
            const data = await res.json()
            if (data.exists) {
                joinError.value = ''
                router.push(`/room/${id}`)
            } else {
                joinError.value = `Le salon "${id}" est introuvable.`
            }
        } catch (e) {
            joinError.value = "Erreur de connexion au serveur."
        }
    }
}

const goToEditor = () => {
    router.push('/editor')
}

</script>

<template>
  <div class="min-h-screen w-full flex flex-col items-center justify-center p-8 font-sans bg-slate-950 text-slate-100 overflow-x-hidden">
    <div class="max-w-3xl w-full flex flex-col items-center text-center space-y-8 animate-fade-in-up">
      <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-500 mb-4 drop-shadow-sm uppercase">
        Guesstimate
      </h1>
      <p class="text-xl md:text-2xl font-light text-slate-400 max-w-2xl leading-relaxed">
        Défiez vos amis dans une course aux estimations. <br class="hidden md:block" /> Placez vos cartes, évitez les erreurs.
      </p>

      <div class="w-full bg-slate-900/50 backdrop-blur-xl p-8 md:p-12 rounded-[3.5rem] border border-white/5 shadow-2xl relative overflow-hidden group">
        <!-- Background Glow -->
        <div class="absolute -top-24 -left-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-[100px] group-hover:bg-indigo-500/20 transition-colors duration-700"></div>
        <div class="absolute -bottom-24 -right-24 w-64 h-64 bg-teal-500/10 rounded-full blur-[100px] group-hover:bg-teal-500/20 transition-colors duration-700"></div>

        <!-- Nickname Section -->
        <div class="mb-10 relative z-10">
          <label class="block text-xs font-black text-slate-500 mb-4 uppercase tracking-[0.2em] text-center">Votre identité</label>
          <div class="max-w-xs mx-auto relative group/nick">
            <input 
              v-model="gameStore.nickname" 
              @input="gameStore.setNickname($event.target.value)"
              type="text" 
              placeholder="Saisir un pseudo..."
              class="w-full bg-slate-800/80 border-2 border-white/5 rounded-2xl px-12 py-4 text-center text-white font-black placeholder:text-slate-600 focus:outline-none focus:border-indigo-500/50 transition-all shadow-2xl tracking-wide group-hover/nick:bg-slate-800"
            />
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
          </div>
        </div>

        <div class="h-px w-full bg-gradient-to-r from-transparent via-white/5 to-transparent mb-10"></div>
        
        <p v-if="joinError" class="text-rose-400 font-bold mb-6 animate-pulse">{{ joinError }}</p>

        <div class="flex flex-col gap-6 w-full max-w-md mx-auto relative z-10">
          <!-- Create Section -->
          <button @click="createRoom" class="w-full px-8 py-5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white rounded-2xl font-black text-lg shadow-2xl transform transition hover:-translate-y-1 active:scale-95">
            CRÉER UN NOUVEAU SALON
          </button>

          <div class="flex items-center gap-4 my-2">
            <div class="h-px flex-1 bg-white/5"></div>
            <span class="text-[10px] font-black text-slate-600 uppercase tracking-widest">OU</span>
            <div class="h-px flex-1 bg-white/5"></div>
          </div>

          <!-- Join Section -->
          <div class="flex flex-col sm:flex-row gap-3">
            <div class="flex-1 relative group/join">
              <input 
                v-model="roomIdToJoin"
                type="text" 
                placeholder="ID du salon..."
                class="w-full bg-slate-800 border border-white/10 rounded-2xl px-6 py-4 text-white font-bold focus:outline-none focus:border-teal-500/50 transition shadow-xl placeholder:text-slate-600"
              />
            </div>
            <button @click="joinRoom" class="px-8 py-4 bg-slate-800 hover:bg-slate-750 text-white rounded-2xl font-black text-lg border border-white/5 transform transition hover:-translate-y-1 active:scale-95">
              REJOINDRE
            </button>
          </div>
        </div>
      </div>

      <div class="mt-8 text-center cursor-pointer group" @click="goToEditor">
        <span class="text-slate-500 group-hover:text-teal-400 transition duration-300 font-bold uppercase tracking-widest text-xs">Accéder au laboratoire d'édition</span>
      </div>

      <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl text-left">
        <div class="p-8 rounded-[2.5rem] bg-slate-900/40 border border-white/5 hover:border-teal-500/30 transition-all duration-500">
          <h3 class="text-lg font-black text-white mb-2 uppercase tracking-tight">Thèmes</h3>
          <p class="text-slate-500 text-sm leading-relaxed">Combinez plusieurs thèmes pour des parties imprévisibles et variées.</p>
        </div>
        <div class="p-8 rounded-[2.5rem] bg-slate-900/40 border border-white/5 hover:border-indigo-500/30 transition-all duration-500">
          <h3 class="text-lg font-black text-white mb-2 uppercase tracking-tight">Multijoueur</h3>
          <p class="text-slate-500 text-sm leading-relaxed">Partagez votre ID de salon et jouez à plusieurs en temps réel.</p>
        </div>
        <div class="p-8 rounded-[2.5rem] bg-slate-900/40 border border-white/5 hover:border-rose-500/30 transition-all duration-500">
          <h3 class="text-lg font-black text-white mb-2 uppercase tracking-tight">Marathon</h3>
          <p class="text-slate-500 text-sm leading-relaxed">Tentez le score parfait en plaçant l'intégralité du paquet sans faute.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
