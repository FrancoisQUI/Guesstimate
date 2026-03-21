<script setup>
import { ref, onMounted, computed } from 'vue'

const singleCard = ref({
    name: '',
    image_url: '',
    wiki_link: '',
    attributes: {},
    tags_array: []
})

const importStatus = ref('')
const singleStatus = ref('')
const cardsList = ref([])
const editMode = ref(false)
const activeCardId = ref(null)

const searchQuery = ref('')
const searchTag = ref('')

const availableAttributes = ref([])
const availableTags = ref([])

// Tags Builder state
const newTagValue = ref('')
const showTagSuggestions = ref(false)

const filteredSuggestedTags = computed(() => {
    const q = newTagValue.value.trim().toLowerCase()
    return availableTags.value.filter(t => 
        t.toLowerCase().includes(q) && !singleCard.value.tags_array.map(tt => tt.toLowerCase()).includes(t.toLowerCase())
    )
})

const addTag = (tagStr = null) => {
    const t = (tagStr || newTagValue.value).trim()
    if (t && !singleCard.value.tags_array.map(tt => tt.toLowerCase()).includes(t.toLowerCase())) {
        singleCard.value.tags_array.push(t)
    }
    newTagValue.value = ''
    showTagSuggestions.value = false
}

const removeTag = (t) => {
    singleCard.value.tags_array = singleCard.value.tags_array.filter(tag => tag !== t)
}

// Attributes Builder state
const newAttrKey = ref('')
const newAttrValue = ref('')
const isCreatingNewType = ref(false)
const customAttrKey = ref('')

const filteredCards = computed(() => {
    return cardsList.value.filter(card => {
        const matchName = card.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchTag = searchTag.value === '' || card.tags.some(t => t.name.toLowerCase().includes(searchTag.value.toLowerCase()))
        return matchName && matchTag
    })
})

const fetchCards = async () => {
    try {
        const response = await fetch('http://localhost:8000/cards/?limit=5000')
        cardsList.value = await response.json()
    } catch (e) {
        console.error("Erreur de chargement des cartes:", e)
    }
}

const fetchMetadata = async () => {
    try {
        const response = await fetch('http://localhost:8000/metadata/')
        const data = await response.json()
        availableAttributes.value = data.attributes || []
        availableTags.value = data.tags || []
        
        if (availableAttributes.value.length > 0 && !newAttrKey.value) {
            newAttrKey.value = availableAttributes.value[0]
        }
    } catch (e) {
        console.error("Failed to fetch metadata:", e)
    }
}

onMounted(() => {
    fetchCards()
    fetchMetadata()
})

const addAttribute = () => {
    const key = isCreatingNewType.value ? customAttrKey.value.trim() : newAttrKey.value
    if (key && newAttrValue.value !== '') {
        const valStr = newAttrValue.value.toString().trim()
        const val = isNaN(valStr) || valStr === '' ? valStr : Number(valStr)
        singleCard.value.attributes[key] = val
        
        newAttrKey.value = availableAttributes.value.length ? availableAttributes.value[0] : ''
        newAttrValue.value = ''
        customAttrKey.value = ''
        isCreatingNewType.value = false
    }
}

const removeAttribute = (key) => {
    delete singleCard.value.attributes[key]
}

const saveSingleCard = async () => {
    try {
        const payload = {
            name: singleCard.value.name,
            image_url: singleCard.value.image_url || null,
            wiki_link: singleCard.value.wiki_link || null,
            attributes: singleCard.value.attributes,
            tag_names: singleCard.value.tags_array
        }
        
        const url = editMode.value ? `http://localhost:8000/cards/${activeCardId.value}` : 'http://localhost:8000/cards/'
        const method = editMode.value ? 'PUT' : 'POST'

        await fetch(url, {
            method: method,
            headers: { 
                'Content-Type': 'application/json',
                'X-Admin-Key': sessionStorage.getItem('admin_key')
            },
            body: JSON.stringify(payload)
        })
        
        singleStatus.value = editMode.value ? "Carte modifiée avec succès!" : "Carte créée avec succès!"
        resetForm()
        fetchCards()
        fetchMetadata()
        setTimeout(() => singleStatus.value = '', 3000)
    } catch (e) {
        console.error(e)
        singleStatus.value = "Erreur lors de la sauvegarde."
    }
}

const deleteCard = async (id) => {
    if (!confirm("Voulez-vous vraiment supprimer cette carte ?")) return;
    try {
        await fetch(`http://localhost:8000/cards/${id}`, { 
            method: 'DELETE',
            headers: { 'X-Admin-Key': sessionStorage.getItem('admin_key') }
        })
        fetchCards()
        fetchMetadata()
        if (activeCardId.value === id) resetForm()
    } catch(e) { console.error(e) }
}

const selectCard = (card) => {
    editMode.value = true
    activeCardId.value = card.id
    singleCard.value = {
        name: card.name,
        image_url: card.image_url || '',
        wiki_link: card.wiki_link || '',
        attributes: card.attributes ? { ...card.attributes } : {},
        tags_array: card.tags ? card.tags.map(t => t.name) : []
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetForm = () => {
    editMode.value = false
    activeCardId.value = null
    singleCard.value = { name: '', image_url: '', wiki_link: '', attributes: {}, tags_array: [] }
    isCreatingNewType.value = false
    newTagValue.value = ''
}

const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = async (e) => {
        try {
            const cardsArray = JSON.parse(e.target.result)
            importStatus.value = "Importation en cours..."
            await fetch('http://localhost:8000/cards/bulk', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-Admin-Key': sessionStorage.getItem('admin_key')
                },
                body: JSON.stringify(cardsArray)
            })
            importStatus.value = "Importation réussie !"
            fetchCards()
            fetchMetadata()
            setTimeout(() => importStatus.value = '', 5000)
        } catch (err) {
            importStatus.value = "Erreur : fichier JSON invalide."
        }
    }
    reader.readAsText(file)
}

const getProceduralColor = (name) => {
  if (!name) return 'hsl(0, 0%, 20%)';
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const h = Math.abs(hash) % 360;
  return `hsl(${h}, 45%, 35%)`;
};

const imageErrors = ref(new Set());
const handleImageError = (cardId) => {
  imageErrors.value.add(cardId);
};
</script>

<template>
  <div class="min-h-screen text-slate-100 p-8 w-full flex flex-col items-center font-sans">
    <div class="w-full max-w-6xl mb-8 flex justify-between items-center bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl gap-4">
        <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-500">
            Éditeur de Cartes
        </h1>
        <router-link to="/" class="text-slate-400 hover:text-white transition duration-300 font-semibold bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg whitespace-nowrap">Retour à l'accueil</router-link>
    </div>

    <!-- Forms Section -->
    <div class="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
      <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-white">{{ editMode ? 'Modifier la carte' : 'Nouvelle carte' }}</h2>
            <button v-if="editMode" @click="resetForm" class="text-sm bg-slate-700 px-3 py-1 rounded text-slate-300 hover:text-white transition">Annuler Edition</button>
        </div>
        
        <div class="space-y-4">
            <input v-model="singleCard.name" type="text" placeholder="Nom de la carte*" class="w-full bg-slate-900 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-teal-500 transition-colors">
            <input v-model="singleCard.image_url" type="text" placeholder="URL Image (Optionnel)" class="w-full bg-slate-900 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-teal-500 transition-colors">
            <input v-model="singleCard.wiki_link" type="text" placeholder="Lien Wikipedia (Optionnel)" class="w-full bg-slate-900 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-teal-500 transition-colors">
            
            <!-- Tags Builder -->
            <div class="p-4 bg-slate-900/50 rounded-xl border border-slate-700 pt-3 relative">
                <h4 class="text-slate-300 font-medium mb-3 text-sm uppercase tracking-wider">Thèmes (Tags)</h4>
                
                <div v-if="singleCard.tags_array.length > 0" class="flex flex-wrap gap-2 mb-4">
                    <span v-for="tag in singleCard.tags_array" :key="tag" class="bg-indigo-600/30 text-indigo-300 border border-indigo-500/50 px-3 py-1.5 rounded-full text-sm font-black flex items-center gap-2 shadow-sm uppercase tracking-wide">
                        {{ tag }}
                        <button @click="removeTag(tag)" class="text-indigo-400 hover:text-white transition-colors flex items-center justify-center w-4 h-4 rounded-full hover:bg-indigo-500/50" title="Retirer ce tag">×</button>
                    </span>
                </div>
                <div v-else class="text-sm text-slate-500 mb-4 italic text-center">Aucun tag défini.</div>

                <div class="flex gap-2 relative">
                    <div class="flex-1 relative">
                        <input 
                            v-model="newTagValue" 
                            @focus="showTagSuggestions = true"
                            @blur="setTimeout(() => showTagSuggestions = false, 200)"
                            @keydown.enter="addTag()"
                            type="text" 
                            placeholder="Taper un tag (ex: nintendo, rpg)..." 
                            class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500 transition shadow-inner"
                        >
                        <!-- Suggestions Dropdown -->
                        <ul v-if="showTagSuggestions && filteredSuggestedTags.length > 0" class="absolute z-50 w-full mt-1 bg-slate-800 border border-slate-600 rounded-lg shadow-2xl max-h-48 overflow-y-auto">
                            <li 
                                v-for="suggestedTag in filteredSuggestedTags" 
                                :key="suggestedTag" 
                                @mousedown.prevent="addTag(suggestedTag)" 
                                class="px-4 py-2 hover:bg-slate-700 cursor-pointer text-sm text-slate-300 font-medium transition"
                            >
                                {{ suggestedTag }}
                            </li>
                        </ul>
                    </div>
                    <button @click="addTag()" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg px-4 py-2 transition active:scale-95 shadow-md flex-none text-sm">Ajouter</button>
                </div>
            </div>

            <!-- Attributes Builder -->
            <div class="p-4 bg-slate-900/50 rounded-xl border border-slate-700 pt-3">
                <h4 class="text-slate-300 font-medium mb-3 text-sm uppercase tracking-wider">Attributs mathématiques</h4>
                
                <div v-if="Object.keys(singleCard.attributes).length > 0" class="mb-4 space-y-2">
                    <div v-for="(val, key) in singleCard.attributes" :key="key" class="flex justify-between items-center bg-slate-800 p-2 rounded-lg border border-slate-600 shadow-sm">
                        <span class="text-sm font-semibold text-teal-400 truncate w-24 sm:w-32">{{ key }}</span>
                        <span class="text-sm text-white flex-1 text-right mr-3 truncate">{{ val }}</span>
                        <button @click="removeAttribute(key)" class="text-xs bg-red-900/50 hover:bg-red-600 text-white px-2 py-1 rounded transition" title="Supprimer cet attribut">X</button>
                    </div>
                </div>
                <div v-else class="text-sm text-slate-500 mb-4 italic text-center">Aucun attribut défini.</div>

                <div class="border-t border-slate-700 pt-4 flex flex-col gap-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-400 font-medium">{{ isCreatingNewType ? 'Créer un nouvel attribut' : 'Sélectionner un attribut existant' }}</span>
                        <button v-if="!isCreatingNewType" @click="isCreatingNewType = true" class="text-xs text-teal-400 hover:text-teal-300 underline font-semibold transition">+ Nouveau type</button>
                        <button v-else @click="isCreatingNewType = false" class="text-xs text-slate-400 hover:text-slate-300 underline font-semibold transition">Annuler création</button>
                    </div>

                    <div class="flex flex-col sm:flex-row gap-2">
                        <select v-if="!isCreatingNewType" v-model="newAttrKey" class="flex-1 min-w-[120px] bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-teal-500 transition cursor-pointer appearance-none">
                            <option value="" disabled>Choisir l'attribut...</option>
                            <option v-for="attr in availableAttributes" :key="attr" :value="attr">{{ attr }}</option>
                        </select>
                        <input v-else v-model="customAttrKey" type="text" placeholder="Le nouveau critère" class="flex-1 min-w-[120px] bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-teal-500 transition shadow-inner">
                        
                        <input v-model="newAttrValue" type="text" placeholder="Valeur" class="flex-1 min-w-[80px] bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-teal-500 transition shadow-inner" @keyup.enter="addAttribute">
                        
                        <button @click="addAttribute" class="bg-teal-600 hover:bg-teal-500 text-white font-bold rounded-lg px-4 py-2 transition active:scale-95 shadow-md flex-none">Ajouter</button>
                    </div>
                </div>
            </div>
            
            <button @click="saveSingleCard" class="w-full px-6 py-4 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-bold font-lg shadow-lg transform transition active:scale-95">
                {{ editMode ? 'Mettre à jour la carte' : 'Créer la carte' }}
            </button>
            <p v-if="singleStatus" class="text-teal-400 text-sm mt-2 text-center font-bold">{{ singleStatus }}</p>
        </div>
      </div>

      <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl flex flex-col">
        <h2 class="text-2xl font-bold text-white mb-4">Bibliothèque (Import)</h2>
        <p class="text-slate-400 text-sm mb-4">Glissez un fichier JSON ici pour l'importer dans la base d'un seul coup.</p>
        <label class="flex-grow flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-xl bg-slate-900/50 text-slate-500 hover:text-slate-300 hover:border-slate-500 transition cursor-pointer p-8 text-center relative group min-h-[250px]">
            <input type="file" accept=".json" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" @change="handleFileUpload">
            <svg class="w-12 h-12 mb-4 group-hover:text-indigo-400 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            <span class="font-medium">Déposez un fichier JSON.</span>
        </label>
        <div v-if="importStatus" class="mt-4 p-4 rounded-xl bg-slate-900 border border-slate-700 text-center shadow-inner"><span class="text-indigo-400 font-semibold">{{ importStatus }}</span></div>
      </div>
    </div>

    <!-- Cards Browser Section -->
    <div class="w-full max-w-6xl">
        <div class="flex flex-col md:flex-row justify-between md:items-end mb-6 border-b border-slate-700 pb-4 gap-4">
            <h2 class="text-2xl font-bold text-white mt-4 md:mt-0">Cartes enregistrées ({{ filteredCards.length }}/{{ cardsList.length }})</h2>
            <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
                <div class="relative w-full sm:w-48 group">
                    <input v-model="searchQuery" type="text" placeholder="Rechercher par nom..." class="bg-slate-900 border border-slate-600 rounded-xl px-4 py-2 pr-10 text-sm text-white focus:outline-none focus:border-teal-500 transition w-full shadow-inner">
                    <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white transition">×</button>
                </div>
                <div class="relative w-full sm:w-48 group">
                    <input v-model="searchTag" type="text" placeholder="Filtrer par tag..." class="bg-slate-900 border border-slate-600 rounded-xl px-4 py-2 pr-10 text-sm text-white focus:outline-none focus:border-indigo-500 transition w-full shadow-inner">
                    <button v-if="searchTag" @click="searchTag = ''" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white transition">×</button>
                </div>
            </div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            <div v-for="card in filteredCards" :key="card.id" class="bg-slate-800 border border-slate-600 rounded-xl overflow-hidden hover:border-teal-400 transition-colors group relative flex flex-col shadow-lg">
                <div class="h-28 bg-slate-900 flex items-center justify-center p-2 text-center text-xs text-slate-500 border-b border-slate-700 relative overflow-hidden">
                    <div v-if="!card.image_url || imageErrors.has(card.id)" 
                         class="absolute inset-0 flex items-center justify-center p-2"
                         :style="{ backgroundColor: getProceduralColor(card.name) }">
                        <span class="text-3xl font-black opacity-20 uppercase">{{ card.name[0] }}</span>
                    </div>
                    <img v-else :src="card.image_url" 
                         @error="handleImageError(card.id)"
                         class="h-full object-contain relative z-10" />
                </div>
                <div class="p-3 flex-grow flex flex-col bg-slate-800">
                    <h3 class="text-sm font-bold text-white truncate mb-1" :title="card.name">{{ card.name }}</h3>
                    <p class="text-[11px] text-slate-400 line-clamp-2 leading-tight mb-3 flex-grow uppercase tracking-tighter">{{ card.tags.map(t=>t.name).join(', ') }}</p>
                    <div class="flex gap-2 mt-auto">
                        <button @click="selectCard(card)" class="flex-1 bg-slate-700 hover:bg-teal-600 text-white text-xs font-bold py-1.5 rounded transition shadow">Éditer</button>
                        <button @click="deleteCard(card.id)" class="flex-none bg-red-900/50 hover:bg-red-600 text-white text-xs font-bold px-3 rounded transition shadow">X</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
