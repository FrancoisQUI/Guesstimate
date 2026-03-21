<script setup>
import { ref, onMounted, computed, onUnmounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useGameStore } from '../store/game';

const route = useRoute();
const router = useRouter();
const gameStore = useGameStore();

const roomId = computed(() => route.params.id);
const selectedAttribute = ref('année');
const selectedTags = ref([]);
const selectedMode = ref('classique');
const selectedDeckLimit = ref(0); // 0 = Maximum
const selectedHandSize = ref(5);

const deckLimitOptions = [
  { label: '20', value: 20 },
  { label: '50', value: 50 },
  { label: '80', value: 80 },
  { label: '100', value: 100 },
  { label: 'Maximum', value: 0 }
];

const availableAttributes = ref([]);
const availableTags = ref([]);
const allCards = ref([]);
const loading = ref(true);

const creatorName = computed(() => {
  const creator = gameStore.players.find(p => p.id === gameStore.creatorId);
  return creator ? creator.name : "l'hôte";
});

const currentTurnName = computed(() => {
  const current = gameStore.players.find(p => p.id === gameStore.currentTurnId);
  if (!current) return "";
  return current.name;
});

const isMyTurn = computed(() => gameStore.currentTurnId === gameStore.clientId);

const selectedHandCard = ref(null);
const gameContainer = ref(null);
const chatOpen = ref(false);
const chatMessage = ref("");
const wikiSummary = ref(null);
const wikiLoading = ref(false);
const copyRoomLink = () => {
  const id = Date.now() + Math.random();
  navigator.clipboard.writeText(roomId.value).then(() => {
    gameStore.messages.push({
      id,
      text: "Identifiant du salon copié !",
      type: "info"
    });
    // Remove after 3 seconds
    setTimeout(() => {
      gameStore.messages = gameStore.messages.filter(m => m.id !== id);
    }, 3000);
  });
};
const hoverTimeout = ref(null);
const isEditingName = ref(false);
const newName = ref(gameStore.nickname);
const nameInput = ref(null);
const hoveredInfoCard = ref(null);

const startEditing = () => {
  newName.value = gameStore.nickname;
  isEditingName.value = true;
  nextTick(() => {
    nameInput.value?.focus();
  });
};

const saveName = () => {
  if (newName.value && newName.value.trim() !== '' && newName.value !== gameStore.nickname) {
    gameStore.updateNickname(newName.value.trim());
  }
  isEditingName.value = false;
};

const startGame = () => {
  const tagsParam = selectedTags.value.length > 0 ? selectedTags.value.join(',') : 'tous';
  gameStore.startGame(selectedAttribute.value, tagsParam, selectedMode.value, selectedDeckLimit.value, selectedHandSize.value);
};

const resetGame = () => {
    gameStore.resetGame();
};

const toggleTag = (tag) => {
    const idx = selectedTags.value.indexOf(tag)
    if (idx > -1) {
        selectedTags.value.splice(idx, 1)
    } else {
        selectedTags.value.push(tag)
    }
}

const cardsMatchingTags = computed(() => {
    if (selectedTags.value.length === 0) return allCards.value
    // Logic: AND (Intersection) - Card must have ALL selected tags
    return allCards.value.filter(card => {
        const cardTagNames = card.tags.map(t => t.name)
        return selectedTags.value.every(tagName => cardTagNames.includes(tagName))
    })
})

const tagCounts = computed(() => {
    const counts = {}
    allCards.value.forEach(card => {
        card.tags.forEach(tag => {
            counts[tag.name] = (counts[tag.name] || 0) + 1
        })
    })
    return counts
})

const majorThemes = computed(() => {
    return availableTags.value.filter(tag => (tagCounts.value[tag] || 0) > 40).sort()
})

const otherThemes = computed(() => {
    return availableTags.value.filter(tag => (tagCounts.value[tag] || 0) <= 40).sort()
})

const canStart = computed(() => {
    const minCards = gameStore.players.length * selectedHandSize.value
    return finalCount.value >= minCards
})

const dynamicAttributes = computed(() => {
    const attrs = new Set()
    cardsMatchingTags.value.forEach(card => {
        if (card.attributes) {
            Object.keys(card.attributes).forEach(k => attrs.add(k))
        }
    })
    return [...attrs].sort()
})

const finalCount = computed(() => {
    if (!selectedAttribute.value) return 0
    return cardsMatchingTags.value.filter(card => 
        card.attributes && card.attributes[selectedAttribute.value] !== undefined
    ).length
})

const maxHandSize = computed(() => {
  const playersCount = Math.max(1, gameStore.players.length);
  const count = finalCount.value;
  return Math.max(3, Math.floor(count / (playersCount + 2)));
});

watch(maxHandSize, (newMax) => {
  if (selectedHandSize.value > newMax) {
    selectedHandSize.value = newMax;
  }
});

const changeHandSize = (delta) => {
  const newValue = selectedHandSize.value + delta;
  if (newValue >= 3 && newValue <= maxHandSize.value) {
    selectedHandSize.value = newValue;
  }
};

watch(dynamicAttributes, (newAttrs) => {
  if (selectedAttribute.value && !newAttrs.includes(selectedAttribute.value)) {
    selectedAttribute.value = newAttrs.length > 0 ? newAttrs[0] : '';
  } else if (!selectedAttribute.value && newAttrs.length > 0) {
    selectedAttribute.value = newAttrs[0];
  }
}, { immediate: true });

const showLogs = ref(localStorage.getItem('show_game_logs') !== 'false');
watch(showLogs, (val) => localStorage.setItem('show_game_logs', val));

const toasts = ref([]);
watch(() => gameStore.messages.length, (newLen, oldLen) => {
  if (newLen > (oldLen || 0)) {
    const newMsg = gameStore.messages[newLen - 1];
    if (newMsg && newMsg.type !== 'chat') {
      toasts.value.push(newMsg);
      setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== newMsg.id);
      }, 5000);
    }
  }
});

const visibleMessages = computed(() => {
  if (showLogs.value) return gameStore.messages;
  return gameStore.messages.filter(m => m.type === 'chat');
});

const attributesByTag = computed(() => {
    const map = {}
    allCards.value.forEach(card => {
        const cardTagNames = card.tags.map(t => t.name)
        cardTagNames.forEach(tagName => {
            if (!map[tagName]) map[tagName] = new Set()
            if (card.attributes) {
                Object.keys(card.attributes).forEach(k => map[tagName].add(k))
            }
        })
    })
    return map
})

watch(() => gameStore.lastPlacement, (newVal) => {
    if (newVal && gameContainer.value) {
        nextTick(() => {
            const cardEl = gameContainer.value.querySelector('.last-placed');
            if (cardEl) {
                cardEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
        });
    }
}, { deep: true });

// Centering at start and when container appears
watch(gameContainer, (el) => {
  if (el && gameStore.status === 'playing') {
    // Minimize chat at start
    chatOpen.value = false;
    
    nextTick(() => {
      // Small delay to let rendering stabilize and avoid race conditions with transitions
      setTimeout(() => {
        const firstCard = el.querySelector('.first-card');
        if (firstCard) {
          firstCard.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        } else {
            const scrollTarget = (el.scrollWidth - el.clientWidth) / 2;
            el.scrollTo({ left: scrollTarget, behavior: 'smooth' });
        }
      }, 500);
    });
  }
});

const isTagCompatible = (tag) => {
    const tagAttrs = attributesByTag.value[tag] || new Set()

    // Show all tags initially so the user can see new categories
    if (selectedTags.value.length === 0) return true

    // 1. If an attribute is selected, the tag MUST possess it
    if (selectedAttribute.value && !tagAttrs.has(selectedAttribute.value)) {
        return false
    }

    // 2. If other tags are selected, ensure we can still find at least one shared attribute
    if (selectedTags.value.length === 0) return true
    
    // Calculate the attribute intersection of currently selected tags
    let currentIntersection = null
    selectedTags.value.forEach(t => {
        const tAttrs = attributesByTag.value[t] || new Set()
        if (currentIntersection === null) currentIntersection = new Set(tAttrs)
        else {
            currentIntersection = new Set([...currentIntersection].filter(a => tAttrs.has(a)))
        }
    })
    
    // Tag must share at least one attribute with all already selected tags
    return [...tagAttrs].some(a => currentIntersection.has(a))
}

const selectCard = (card) => {
  if (selectedHandCard.value?.id === card.id) {
    selectedHandCard.value = null;
  } else {
    selectedHandCard.value = card;
  }
};

const placeCard = (index) => {
  if (selectedHandCard.value) {
    gameStore.placeCard(selectedHandCard.value.id, index);
    selectedHandCard.value = null;
  }
};

const fetchWikiSummary = async (card) => {
  if (!card.wiki_link || !card.wiki_link.includes('wikipedia.org')) return;
  
  const title = card.wiki_link.split('/wiki/').pop();
  wikiLoading.value = true;
  try {
    const res = await fetch(`https://fr.wikipedia.org/api/rest_v1/page/summary/${title}`);
    const data = await res.json();
    wikiSummary.value = data.extract;
  } catch (e) {
    console.error("Wiki fetch error", e);
  } finally {
    wikiLoading.value = false;
  }
};

const handleWikiHover = (card) => {
  clearTimeout(hoverTimeout.value);
  hoverTimeout.value = setTimeout(() => fetchWikiSummary(card), 500);
};

const closeWiki = () => {
  clearTimeout(hoverTimeout.value);
  wikiSummary.value = null;
};

const openWiki = (card) => {
  if (card.wiki_link) {
    window.open(card.wiki_link, '_blank');
  } else {
    window.open(`https://www.google.com/search?q=site:wikipedia.org+${encodeURIComponent(card.name)}`, '_blank');
  }
};

const accuracy = computed(() => {
  if (gameStore.scoreTotal === 0) return 0;
  return ((gameStore.scoreCorrect / gameStore.scoreTotal) * 100).toFixed(1);
});

// Scroll handling
const handleWheel = (e) => {
  if (gameContainer.value) {
    gameContainer.value.scrollLeft += e.deltaY;
  }
};

const scroll = (dir) => {
  if (gameContainer.value) {
    const itemWidth = 192 + 32; // Card width (w-48 = 12rem = 192px) + gap (8 = 32px)
    gameContainer.value.scrollLeft += dir * itemWidth;
  }
};

const sendChat = () => { // Added
  if (chatMessage.value.trim()) {
    gameStore.sendMessage(chatMessage.value);
    chatMessage.value = "";
  }
};

watch(() => gameStore.status, (newStatus) => {
  if (newStatus === 'waiting') {
    chatOpen.value = true;
  }
}, { immediate: true });

onMounted(async () => {
  gameStore.connect(roomId.value);
  window.addEventListener('keydown', handleKey);

  // Fetch metadata for creator
  try {
      const [metaRes, cardsRes] = await Promise.all([
          fetch('http://localhost:8000/metadata/'),
          fetch('http://localhost:8000/cards/')
      ])
      
      const metaData = await metaRes.json()
      availableAttributes.value = metaData.attributes || []
      availableTags.value = metaData.tags || []
      
      allCards.value = await cardsRes.json()
      loading.value = false

      if (availableAttributes.value.length > 0) {
          selectedAttribute.value = availableAttributes.value[0]
      }
  } catch (e) {
      console.error("Failed to fetch data:", e)
      loading.value = false
  }
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKey);
});

const handleKey = (e) => {
  const key = e.key.toLowerCase();
  if (key === 'arrowleft' || key === 'a' || key === 'q') scroll(-1);
  if (key === 'arrowright' || key === 'd') scroll(1);
};

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
  <div class="h-screen w-full bg-slate-950 text-slate-100 flex flex-col overflow-hidden font-sans">
    <!-- Header / Stats (Flex Header) -->
    <header class="h-[72px] md:h-[88px] px-4 md:px-8 flex items-center justify-between bg-slate-900/90 backdrop-blur-xl border-b border-white/10 z-[70] shadow-2xl flex-shrink-0">
      <div class="flex items-center gap-3 md:gap-4">
        <button @click="router.push('/')" class="p-2 hover:bg-white/10 rounded-xl transition-all" title="Quitter le salon">
          <svg class="w-5 h-5 md:w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="flex flex-col">
          <div class="flex items-center gap-2 md:gap-3 group/title">
            <h1 class="text-lg md:text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-400 tracking-tight whitespace-nowrap">
              Salon {{ roomId }}
            </h1>
            <button 
              @click="copyRoomLink"
              class="p-1.5 rounded-lg bg-slate-800/50 hover:bg-indigo-500 hover:text-white text-slate-500 transition-all border border-white/5 opacity-0 group-hover/title:opacity-100 flex items-center gap-2"
              title="Copier l'identifiant"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span class="text-[9px] font-black uppercase tracking-widest pr-1">ID</span>
            </button>
          </div>
          <p class="text-[10px] text-slate-500 font-black uppercase tracking-[0.2em]">{{ gameStore.mode }} • {{ gameStore.attribute }}</p>
        </div>
      </div>

      <!-- Center Turn Info -->
      <div v-if="gameStore.status === 'playing'" class="w-full md:w-auto order-3 md:order-2 md:absolute md:left-1/2 md:-translate-x-1/2 flex flex-col items-center pointer-events-none group">
        <div 
          class="px-4 py-2 md:px-8 md:py-3 rounded-xl md:rounded-2xl flex items-center gap-2 md:gap-4 transition-all duration-500 shadow-2xl border backdrop-blur-xl"
          :class="isMyTurn 
            ? 'bg-emerald-500/10 border-emerald-500/40 shadow-[0_0_40px_rgba(16,185,129,0.2)]' 
            : 'bg-orange-500/10 border-orange-500/40 shadow-[0_0_40px_rgba(249,115,22,0.1)]'"
        >
            <div 
              class="w-2 h-2 md:w-3 h-3 rounded-full animate-pulse"
              :class="isMyTurn ? 'bg-emerald-400 shadow-[0_0_15px_rgba(52,211,153,1)]' : 'bg-orange-400 shadow-[0_0_15px_rgba(251,146,60,1)]'"
            ></div>
            <span class="text-sm md:text-lg font-black text-white tracking-widest uppercase flex items-center gap-1 md:gap-2">
              <span v-if="isMyTurn">C'est <span class="text-emerald-400 border-b-2 border-emerald-400/50">votre</span> tour</span>
              <span v-else>C'est le tour de <span class="text-orange-400 border-b-2 border-orange-400/50">{{ currentTurnName }}</span></span>
            </span>
        </div>
      </div>

      <div class="flex gap-4 md:gap-6 items-center order-2 md:order-3 ml-auto md:ml-0">
        <!-- Players List (Compact on mobile) -->
        <div class="flex gap-1 md:gap-2 items-center">
          <div v-for="p in gameStore.players" :key="p.id" 
               class="relative flex flex-col items-center group/player"
               :class="gameStore.currentTurnId === p.id ? 'z-10' : 'z-0'">
            <div class="w-8 h-8 md:w-10 md:h-10 rounded-full border-2 flex items-center justify-center text-[10px] md:text-xs font-bold transition-all duration-300 shadow-xl relative"
                 :class="[
                   gameStore.currentTurnId === p.id ? 'border-teal-400 bg-teal-400/20 scale-110' : 'border-slate-700 bg-slate-800 opacity-60',
                   gameStore.clientId === p.id ? 'ring-2 ring-indigo-500 ring-offset-2 ring-offset-slate-900 shadow-[0_0_20px_rgba(99,102,241,0.3)]' : ''
                 ]">
              {{ p.name[0] }}
              <div v-if="gameStore.creatorId === p.id" class="absolute -top-2 -left-2 text-amber-400 fill-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.6)]">
                <svg class="w-4 h-4 md:w-6 h-6 transform -rotate-12" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5M19 19C19 19.6 18.6 20 18 20H6C5.4 20 5 19.6 5 19V18H19V19Z" />
                </svg>
              </div>
            </div>
            <div v-if="gameStore.currentTurnId === p.id" class="absolute -bottom-1 w-1.5 h-1.5 md:w-2 md:h-2 bg-teal-400 rounded-full animate-pulse shadow-[0_0_10px_rgba(45,212,191,1)]"></div>
            <span class="absolute -top-1 -right-1 md:-top-2 md:-right-2 bg-slate-800 border border-white/10 text-[7px] md:text-[8px] font-black px-1 md:px-1.5 py-0.5 rounded-full z-10 text-white">{{ p.hand_count }}</span>
          </div>
        </div>

        <div v-if="selectedMode === 'complet'" class="hidden sm:block text-right">
          <p class="text-[8px] md:text-xs text-slate-500 uppercase">Précision</p>
          <p class="text-sm md:text-2xl font-black text-teal-400">{{ accuracy }}%</p>
        </div>
        <div v-if="gameStore.status !== 'waiting'" class="text-right">
          <p class="text-[8px] md:text-xs text-slate-500 uppercase">Pioche</p>
          <p class="text-sm md:text-2xl font-black text-indigo-400">{{ gameStore.deckCount }}</p>
        </div>
      </div>
    </header>

    <div class="flex-1 relative flex flex-col overflow-hidden w-full">
      <div class="flex-1 flex overflow-hidden relative w-full">
      <!-- Player Sidebar (Lobby only) -->
      <div 
        v-if="gameStore.status === 'waiting'"
        class="h-full w-full sm:w-80 bg-slate-900/40 border-r border-white/10 z-50 flex flex-col flex-shrink-0 animate-fade-in"
      >
      <div class="p-6 border-b border-white/5 flex items-center justify-between">
        <h3 class="font-black uppercase tracking-widest text-xs text-slate-500">Joueurs Connectés</h3>
        <span class="bg-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full text-[10px] font-black">{{ gameStore.players.length }}</span>
      </div>

      <div class="flex-1 overflow-y-auto p-6 space-y-4 no-scrollbar">
        <div v-for="p in gameStore.players" :key="p.id" 
             class="p-5 bg-white/5 border border-white/5 rounded-[2rem] flex items-center gap-4 transition-all hover:bg-white/10"
             :class="gameStore.clientId === p.id ? 'border-indigo-500/30 ring-2 ring-indigo-500/10' : ''"
        >
          <div class="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center font-black text-white relative border-2 border-white/10">
            {{ p.name[0] }}
            <div v-if="gameStore.creatorId === p.id" class="absolute -top-4 -left-3 text-amber-400 fill-amber-400 drop-shadow-[0_0_12px_rgba(251,191,36,0.6)]">
              <svg class="w-8 h-8 transform -rotate-[15deg]" viewBox="0 0 24 24" fill="currentColor">
                <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5M19 19C19 19.6 18.6 20 18 20H6C5.4 20 5 19.6 5 19V18H19V19Z" />
              </svg>
            </div>
          </div>
          <div class="flex flex-col text-left overflow-hidden">
            <div v-if="gameStore.clientId === p.id" class="flex items-center gap-2 group/edit">
              <input 
                v-if="isEditingName"
                v-model="newName"
                @blur="saveName"
                @keyup.enter="saveName"
                ref="nameInput"
                class="bg-slate-950 border border-indigo-500/50 rounded-lg px-2 py-0.5 text-sm font-bold text-white w-28 focus:outline-none focus:ring-2 ring-indigo-500/20"
              />
              <span v-else class="text-xl font-black tracking-tight text-indigo-400 cursor-pointer truncate" @click="startEditing">{{ p.name }}</span>
              <button v-if="!isEditingName" @click="startEditing" class="opacity-0 group-hover/edit:opacity-100 transition text-slate-500 hover:text-indigo-400 flex-shrink-0">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
            <span v-else class="text-xl font-black tracking-tight text-slate-200 truncate">{{ p.name }}</span>
            <span class="text-[10px] font-black uppercase tracking-widest text-slate-500">
              {{ gameStore.creatorId === p.id ? 'Hôte du salon' : 'Joueur' }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="p-6 bg-slate-950/30 border-t border-white/5 mt-auto space-y-4">
        <div class="flex items-center gap-3 text-slate-500">
          <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span class="text-[10px] font-black uppercase tracking-widest">Salon actif • {{ roomId }}</span>
        </div>
        <button 
          @click="copyRoomLink"
          class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-black uppercase tracking-widest transition-all flex items-center justify-center gap-2 group shadow-lg active:scale-95"
        >
          <svg class="w-4 h-4 group-hover:rotate-12 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Copier l'ID du salon
        </button>
      </div>
    </div>

      <!-- Main Game Area -->
      <main class="flex-1 h-full overflow-hidden no-scrollbar relative flex flex-col">
      
      <!-- Waiting Screen (Lobby) -->
      <div v-if="gameStore.status === 'waiting'" class="flex-1 w-full overflow-y-auto md:overflow-hidden no-scrollbar bg-slate-900/20">
        <div class="text-center animate-fade-in w-full h-full flex flex-col overflow-hidden">
          <div class="flex-1 p-6 md:p-12 md:px-16 lg:px-24 bg-transparent border-white/5 border-l flex flex-col overflow-hidden min-h-0">
          
          <div v-if="gameStore.creatorId === gameStore.clientId" class="pt-4 flex-1 flex flex-col overflow-hidden min-h-0">

            <div v-if="loading" class="py-12 flex flex-col items-center gap-4">
                <div class="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                <p class="text-slate-500 font-medium">Récupération des thèmes...</p>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 text-left flex-1 min-h-0 overflow-hidden">
              <!-- Column 2 & 3: Themes (Order 2, Span 2) -->
              <div class="space-y-6 md:col-span-2 md:order-2 md:h-full flex flex-col overflow-hidden">
                <div class="flex flex-col h-full overflow-hidden">
                  <label class="block text-[10px] font-black text-slate-500 mb-4 uppercase tracking-[0.2em] text-center md:text-left">Thématiques</label>
                  
                  <div class="flex flex-wrap gap-2 justify-center md:justify-start mb-6 px-1">
                      <button 
                        @click="selectedTags = []"
                        class="px-5 py-2.5 rounded-full text-sm font-bold transition-all duration-300 border"
                        :class="selectedTags.length === 0 ? 'bg-white text-slate-950 border-white shadow-lg scale-105' : 'bg-slate-800/50 text-slate-400 border-white/10 hover:border-white/30'"
                      >
                        Mélange (Tous)
                      </button>
                      <button 
                        v-if="selectedTags.length > 0"
                        @click="selectedTags = []"
                        class="px-5 py-2.5 rounded-full text-sm font-bold transition-all duration-300 border bg-rose-500/20 text-rose-400 border-rose-500/30 hover:bg-rose-500/30 shadow-lg"
                      >
                        Reset ({{ selectedTags.length }})
                      </button>
                  </div>

                  <div class="flex-1 overflow-y-auto px-4 no-scrollbar border-y border-white/5 py-8 min-h-0">
                    <div class="flex flex-col gap-8">
                      <!-- Major Themes -->
                      <div v-if="majorThemes.length > 0">
                        <p class="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4 text-center md:text-left">Grands Thèmes (>40 cartes)</p>
                        <div class="grid grid-cols-1 sm:grid-cols-2 2xl:grid-cols-3 gap-3">
                          <template v-for="tag in majorThemes" :key="tag">
                              <button 
                                v-if="isTagCompatible(tag) || selectedTags.includes(tag)"
                                @click="toggleTag(tag)"
                                class="px-3 py-2 rounded-xl text-[11px] md:text-xs font-bold transition-all duration-300 border flex items-center justify-between gap-2"
                                :class="[
                                  selectedTags.includes(tag) ? 'bg-indigo-600 text-white border-indigo-400 shadow-[0_0_15px_rgba(79,70,229,0.4)] scale-102' : 
                                  'bg-slate-800/50 text-slate-400 border-white/10 hover:border-indigo-500/50'
                                ]"
                              >
                                <span class="uppercase tracking-tight truncate">{{ tag }}</span>
                                <span class="text-[9px] opacity-40 font-black flex-shrink-0">{{ tagCounts[tag] }}</span>
                              </button>
                          </template>
                        </div>
                      </div>

                      <!-- Other Themes -->
                      <div v-if="otherThemes.length > 0">
                        <p class="text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4 text-center md:text-left">Autres Thématiques</p>
                        <div class="grid grid-cols-1 sm:grid-cols-2 2xl:grid-cols-3 gap-2">
                          <template v-for="tag in otherThemes" :key="tag">
                              <button 
                                v-if="isTagCompatible(tag) || selectedTags.includes(tag)"
                                @click="toggleTag(tag)"
                                class="px-3 py-1.5 rounded-lg text-[10px] md:text-[11px] font-bold transition-all duration-300 border flex items-center justify-between gap-2"
                                :class="[
                                  selectedTags.includes(tag) ? 'bg-indigo-600 text-white border-indigo-400 shadow-[0_0_15px_rgba(79,70,229,0.4)]' : 
                                  'bg-slate-800/50 text-slate-400 border-white/10 hover:border-indigo-500/50'
                                ]"
                              >
                                <span class="uppercase tracking-tight truncate">{{ tag }}</span>
                                <span class="text-[8px] opacity-40 font-black flex-shrink-0">{{ tagCounts[tag] }}</span>
                              </button>
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Column 1: Mode & Attribute (Order 1, Span 1) -->
              <div class="space-y-10 md:order-1 md:col-span-1 md:border-r border-white/5 md:pr-10">
                <!-- 1. Attribute Selection (Moved to Top) -->
                <div class="bg-indigo-500/5 p-8 rounded-[2.5rem] border border-indigo-500/10 shadow-2xl">
                  <label class="block text-[10px] font-black text-indigo-400 mb-6 uppercase tracking-[0.2em] text-center md:text-left">Type de donnée</label>
                  <div class="relative group">
                    <select v-model="selectedAttribute" class="w-full appearance-none bg-slate-900 border border-white/10 rounded-2xl px-8 py-5 text-white font-black tracking-widest uppercase text-xs focus:outline-none focus:border-indigo-500 transition shadow-2xl cursor-pointer group-hover:bg-slate-800">
                      <option v-for="attr in dynamicAttributes" :key="attr" :value="attr">
                        {{ attr.replace('_', ' ') }}
                      </option>
                    </select>
                    <div class="pointer-events-none absolute inset-y-0 right-6 flex items-center text-slate-400">
                      <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                  </div>
                  <p class="mt-4 text-[10px] text-slate-500 text-center md:text-left font-medium opacity-60 italic">Attribut de comparaison pour la partie.</p>
                </div>

                <!-- 2. Mode Selection -->
                <div class="bg-slate-800/30 p-8 rounded-[2.5rem] border border-white/5 ring-1 ring-white/5">
                  <label class="block text-[10px] font-black text-slate-500 mb-6 uppercase tracking-[0.2em] text-center md:text-left">Mode de Jeu</label>
                  <div class="grid grid-cols-1 gap-4">
                    <button 
                      @click="selectedMode = 'classique'"
                      class="px-8 py-5 rounded-2xl border-2 transition-all flex flex-col gap-1 relative overflow-hidden group/btn"
                      :class="selectedMode === 'classique' ? 'bg-indigo-600 border-indigo-400 shadow-[0_0_30px_rgba(79,70,229,0.3)]' : 'bg-slate-900/50 border-white/5 hover:border-white/20'"
                    >
                      <div class="flex items-center justify-between w-full mb-1">
                        <span class="font-black uppercase tracking-widest text-sm md:text-base truncate">Classique</span>
                        <div v-if="selectedMode === 'classique'" class="w-2 h-2 rounded-full bg-white shadow-[0_0_10px_#fff] flex-shrink-0"></div>
                      </div>
                      <span class="text-[10px] md:text-xs opacity-60 leading-tight">Timeline traditionnelle</span>
                    </button>
                    <button 
                      @click="selectedMode = 'complet'"
                      class="px-8 py-5 rounded-2xl border-2 transition-all flex flex-col gap-1 relative overflow-hidden group/btn"
                      :class="selectedMode === 'complet' ? 'bg-teal-600 border-teal-400 shadow-[0_0_30px_rgba(20,184,166,0.3)]' : 'bg-slate-900/50 border-white/5 hover:border-white/20'"
                    >
                      <div class="flex items-center justify-between w-full mb-1">
                        <span class="font-black uppercase tracking-widest text-sm md:text-base truncate">Marathon</span>
                        <div v-if="selectedMode === 'complet'" class="w-2 h-2 rounded-full bg-white shadow-[0_0_10px_#fff] flex-shrink-0"></div>
                      </div>
                      <span class="text-[10px] md:text-xs opacity-60 leading-tight">Score cumulé (Précision)</span>
                    </button>
                  </div>
                </div>

                <!-- Deck Size Selection (Marathon only) -->
                <Transition name="fade">
                  <div v-if="selectedMode === 'complet'" class="bg-teal-500/5 p-8 rounded-[2.5rem] border border-teal-500/10 shadow-2xl">
                    <label class="block text-[10px] font-black text-teal-400 mb-6 uppercase tracking-[0.2em] text-center md:text-left">Nombre de Cartes (Deck)</label>
                    <div class="flex flex-wrap gap-2 justify-center md:justify-start">
                      <button 
                        v-for="opt in deckLimitOptions" 
                        :key="opt.value"
                        @click="selectedDeckLimit = opt.value"
                        class="px-4 py-2 rounded-xl border text-[10px] font-black uppercase tracking-widest transition-all"
                        :class="selectedDeckLimit === opt.value ? 'bg-teal-600 border-teal-400 text-white shadow-lg scale-110' : 'bg-slate-900/50 border-white/5 text-slate-500 hover:border-white/20'"
                      >
                        {{ opt.label }}
                      </button>
                    </div>
                    <p class="text-[10px] text-teal-500/40 mt-4 italic text-center md:text-left">*Le jeu s'arrêtera après avoir épuisé ce nombre de cartes.</p>
                  </div>
                </Transition>

                <!-- Hand Size Selection (Classique only) -->
                <Transition name="fade">
                  <div v-if="selectedMode === 'classique'" class="bg-indigo-500/5 p-8 rounded-[2.5rem] border border-indigo-500/10 shadow-2xl">
                    <label class="block text-[10px] font-black text-indigo-400 mb-6 uppercase tracking-[0.2em] text-center md:text-left">Taille de la Main Initiale</label>
                    <div class="flex items-center gap-4 justify-center md:justify-start">
                      <button 
                        @click="changeHandSize(-1)"
                        :disabled="selectedHandSize <= 3"
                        class="w-10 h-10 rounded-xl border flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed bg-slate-900/50 border-white/5 text-indigo-400 hover:border-indigo-500/50 active:scale-95"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M20 12H4" stroke-width="3" stroke-linecap="round"/></svg>
                      </button>
                      
                      <div class="w-16 py-2 bg-slate-900 rounded-xl border border-indigo-500/30 text-center font-black text-white shadow-inner">
                        {{ selectedHandSize }}
                      </div>

                      <button 
                        @click="changeHandSize(1)"
                        :disabled="selectedHandSize >= maxHandSize"
                        class="w-10 h-10 rounded-xl border flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed bg-slate-900/50 border-white/5 text-indigo-400 hover:border-indigo-500/50 active:scale-95"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-width="3" stroke-linecap="round"/></svg>
                      </button>
                    </div>
                    <p class="mt-4 text-[10px] text-indigo-500/60 font-medium italic text-center md:text-left">
                      Max: {{ maxHandSize }} ({{ finalCount }} cartes / {{ Math.max(1, gameStore.players.length) + 2 }})
                    </p>
                  </div>
                </Transition>

              </div>
            </div>

              <button 
                @click="startGame" 
                :disabled="!canStart" 
                class="w-full bg-gradient-to-r from-indigo-500 to-teal-500 px-12 py-5 rounded-2xl text-xl font-bold shadow-xl transform hover:scale-[1.02] transition active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed disabled:grayscale disabled:scale-100"
                :title="!canStart ? `Il faut au moins ${gameStore.players.length * selectedHandSize} cartes (${gameStore.players.length} joueurs x ${selectedHandSize})` : ''"
              >
                {{ !canStart ? `Manque de cartes (${finalCount}/${gameStore.players.length * selectedHandSize})` : `Démarrer la partie (${finalCount} cartes)` }}
              </button>
            </div>
          <div v-else class="flex flex-col items-center gap-4">
            <div class="w-12 h-12 border-4 border-teal-500/30 border-t-teal-500 rounded-full animate-spin"></div>
            <p class="text-teal-400 font-bold animate-pulse text-lg tracking-widest uppercase text-center">
              En attente de <span class="bg-teal-500/20 px-3 py-1 rounded-lg text-white font-black">{{ creatorName }}</span>
              <br/>
              <span class="text-xs text-slate-500 mt-2 block tracking-normal italic opacity-60">Le créateur configure la partie...</span>
            </p>
          </div>
      </div>
    </div>
  </div>

      <!-- Won Screen -->
      <div v-else-if="gameStore.status === 'won'" class="text-center z-30 animate-scale-up">
        <div class="p-16 bg-slate-900/90 rounded-[4rem] border-2 border-teal-500/30 shadow-[0_0_100px_rgba(20,184,166,0.2)]">
          <h2 class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-emerald-300 mb-4 animate-bounce">
            VICTOIRE !
          </h2>
          <p v-if="mode === 'complet'" class="text-2xl text-slate-300 mb-8">
            Score final : <span class="text-teal-400 font-bold">{{ accuracy }}%</span> de précision.
          </p>
          <p v-else class="text-2xl text-slate-300 mb-8">Toutes les cartes ont été placées !</p>
          
          <div class="flex flex-col md:flex-row gap-4 justify-center">
            <button 
              v-if="gameStore.creatorId === gameStore.clientId"
              @click="resetGame" 
              class="px-8 py-4 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-black uppercase tracking-widest shadow-lg transform transition hover:scale-105 active:scale-95 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Rejouer (Lobby)
            </button>
            <button @click="router.push('/')" class="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold transition flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Quitter
            </button>
          </div>
        </div>
      </div>

      <div v-else class="w-full flex flex-col items-center overflow-hidden">
        <!-- Placement Status Indicator -->
        <div v-if="gameStore.lastPlacement" class="flex items-center gap-3 px-4 py-2 bg-slate-900/50 backdrop-blur-md rounded-full border border-white/10 mb-4 animate-scale-up shadow-xl z-20">
          <span class="text-[10px] text-slate-500 uppercase font-black tracking-[0.2em]">Dernier placement :</span>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full shadow-[0_0_10px]" :class="gameStore.lastPlacement.success ? 'bg-emerald-500 shadow-emerald-500/50' : 'bg-rose-500 shadow-rose-500/50'"></div>
            <span class="text-xs font-bold" :class="gameStore.lastPlacement.success ? 'text-emerald-400' : 'text-rose-400'">
              {{ gameStore.lastPlacement.success ? 'Correct' : 'Incorrect' }}
            </span>
          </div>
        </div>

        <div 
          ref="gameContainer"
          @wheel="handleWheel"
          class="w-full overflow-x-auto overflow-y-visible flex items-center gap-8 px-12 py-24 no-scrollbar scroll-smooth justify-start snap-x snap-mandatory"
        >
          <!-- Center-aligned spacers -->
          <div class="flex-shrink-0 w-[45vw] h-1"></div>
          <template v-for="(card, i) in gameStore.board" :key="card.id">
            <!-- Slot Before -->
            <button 
              @click="placeCard(i)"
              class="group flex-shrink-0 w-8 md:w-12 h-48 md:h-64 rounded-2xl border-2 border-dashed border-white/5 hover:border-teal-500/50 hover:bg-teal-500/5 transition flex items-center justify-center opacity-30 hover:opacity-100 disabled:cursor-not-allowed snap-center"
              :class="{'opacity-100 border-teal-500/50 bg-teal-500/10 scale-110 shadow-[0_0_20px_rgba(20,184,166,0.2)]': selectedHandCard}"
              :disabled="gameStore.currentTurnId !== gameStore.clientId"
            >
              <svg class="w-6 h-6 text-teal-500 group-hover:scale-125 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"/></svg>
            </button>

            <!-- Placed Card -->
            <!-- Placed Card Wrapper -->
            <div 
              class="flex-shrink-0 relative transition-all duration-500 ease-out"
              :class="[
                gameStore.lastPlacement && gameStore.lastPlacement.card_id == card.id ? 'scale-125 z-[50] ring-4 ring-white/20 last-placed' : 'z-0',
                i === 0 ? 'first-card' : ''
              ]"
            >
              <!-- Halo Background -->
              <div 
                v-if="gameStore.lastPlacement && gameStore.lastPlacement.card_id == card.id"
                class="absolute -inset-4 rounded-3xl blur-3xl opacity-60 animate-pulse transition-all duration-500"
                :class="gameStore.lastPlacement.success ? 'bg-emerald-400' : 'bg-rose-500'"
              ></div>

              <!-- Status Icon -->
              <div 
                v-if="gameStore.lastPlacement && gameStore.lastPlacement.card_id == card.id"
                class="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center shadow-xl border-2 z-20 scale-110"
                :class="gameStore.lastPlacement.success ? 'bg-emerald-500 border-emerald-300' : 'bg-rose-500 border-rose-300'"
              >
                  <svg v-if="gameStore.lastPlacement.success" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  <svg v-else class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"/></svg>
              </div>

              <!-- Main Card -->
              <div 
                class="w-32 h-44 md:w-48 md:h-64 bg-slate-800 rounded-2xl border shadow-2xl overflow-hidden relative group transition-colors duration-500 snap-center"
                :class="[
                  gameStore.lastPlacement && gameStore.lastPlacement.card_id == card.id ? (
                    gameStore.lastPlacement.success ? 'border-emerald-500/50' : 'border-rose-500/50'
                  ) : 'border-white/10'
                ]"
              >
                <div v-if="!card.image_url || imageErrors.has(card.id)" 
                    class="absolute inset-0 flex items-center justify-center p-4 text-center"
                    :style="{ backgroundColor: getProceduralColor(card.name) }">
                  <span class="text-4xl font-black opacity-20 uppercase select-none">{{ card.name[0] }}</span>
                </div>
                <img v-else :src="card.image_url" 
                    @error="handleImageError(card.id)"
                    class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-80 transition" />
                <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent flex flex-col justify-end p-4">
                  <p class="text-xs text-slate-400 border-l-2 border-teal-500 pl-2 mb-1 uppercase tracking-tighter">{{ gameStore.attribute }}</p>
                  <p class="text-2xl font-black text-white leading-none">{{ card.value }}</p>
                  <p 
                    class="text-xs font-medium text-slate-300 line-clamp-3 overflow-hidden" 
                    :title="card.name"
                  >
                    {{ card.name }}
                  </p>
                </div>
                
                <!-- Card Overlay Buttons -->
                <div class="absolute top-2 right-2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <!-- Wiki Button -->
                  <button 
                      @mouseenter="handleWikiHover(card)" 
                      @mouseleave="closeWiki" 
                      @click="openWiki(card)"
                      class="p-2 bg-black/50 backdrop-blur-md rounded-lg hover:bg-white/20 text-white"
                      title="Wiki"
                  >
                    <span class="text-xs font-bold font-serif italic">W</span>
                  </button>
                  <!-- Info Button -->
                  <button 
                      @mouseenter="hoveredInfoCard = card" 
                      @mouseleave="hoveredInfoCard = null"
                      class="p-2 bg-indigo-500/50 backdrop-blur-md rounded-lg hover:bg-indigo-400 text-white"
                      title="Détails"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </button>
                </div>
              </div>
            </div>
          </template>

          <!-- Final Slot -->
          <button 
            @click="placeCard(gameStore.board.length)"
            class="group flex-shrink-0 w-8 md:w-12 h-48 md:h-64 rounded-2xl border-2 border-dashed border-white/5 hover:border-teal-500/50 hover:bg-teal-500/5 transition flex items-center justify-center opacity-30 hover:opacity-100 disabled:cursor-not-allowed snap-center"
            :class="{'opacity-100 border-teal-500/50 bg-teal-500/10 scale-110 shadow-[0_0_20px_rgba(20,184,166,0.2)]': selectedHandCard}"
            :disabled="gameStore.currentTurnId !== gameStore.clientId"
          >
            <svg class="w-6 h-6 text-teal-500 group-hover:scale-125 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"/></svg>
          </button>

          <div class="flex-shrink-0 w-[45vw] h-1"></div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex gap-4 mb-2">
            <button @click="scroll(-1)" class="p-3 bg-slate-800 hover:bg-slate-700 rounded-full transition shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
            </button>
            <button @click="scroll(1)" class="p-3 bg-slate-800 hover:bg-slate-700 rounded-full transition shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
            </button>
        </div>
      </div>



      </main>
      </div> <!-- End inner flex-1 -->

    <!-- Footer area (Hand + Controls) -->
    <footer v-if="gameStore.status !== 'waiting'" class="w-full bg-slate-900/80 backdrop-blur-xl border-t border-white/5 p-6 flex flex-col items-center gap-6 z-20 shadow-[0_-20px_50px_rgba(0,0,0,0.5)] transition-all duration-500">
      
      <!-- User Hand -->
      <div v-if="gameStore.status === 'playing'" class="flex gap-4 overflow-x-auto max-w-full no-scrollbar px-4 pt-6 pb-2">
        <div 
          v-for="card in gameStore.hand" :key="card.id"
          @click="selectCard(card)"
          class="flex-shrink-0 w-24 h-36 md:w-36 md:h-52 bg-slate-800 rounded-xl border border-white/10 overflow-hidden cursor-pointer relative group transition-all duration-300"
          :class="selectedHandCard?.id === card.id ? 'ring-4 ring-indigo-500 scale-105 -translate-y-2 md:-translate-y-4 shadow-[0_20px_40px_rgba(99,102,241,0.3)]' : 'hover:scale-105 hover:-translate-y-2'"
        >
          <div v-if="!card.image_url || imageErrors.has(card.id)" 
               class="absolute inset-0 flex items-center justify-center p-4 text-center"
               :style="{ backgroundColor: getProceduralColor(card.name) }">
            <span class="text-4xl font-black opacity-20 uppercase select-none">{{ card.name[0] }}</span>
          </div>
          <img v-else :src="card.image_url" 
               @error="handleImageError(card.id)"
               class="absolute inset-0 w-full h-full object-cover opacity-80" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent flex flex-col justify-end p-4">
            <p class="text-[10px] text-slate-400 uppercase tracking-tighter mb-1">? {{ gameStore.attribute }}</p>
            <p class="text-xs font-bold text-white line-clamp-2 leading-tight">{{ card.name }}</p>
          </div>

          <!-- Hand Card Info Button -->
          <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <button 
                @mouseenter="hoveredInfoCard = card" 
                @mouseleave="hoveredInfoCard = null"
                class="p-1.5 bg-indigo-500/50 backdrop-blur-md rounded-lg hover:bg-indigo-400 text-white"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Actions & Chat Toggle (Removed old left button, kept status) -->
      <div class="w-full flex items-center justify-between px-6">
        <div class="flex items-center gap-4">
          <div class="flex flex-col">
            <p v-if="gameStore.status === 'playing' && gameStore.currentTurnId !== gameStore.clientId" class="text-slate-500 font-medium italic animate-pulse">
              Attente du tour de l'autre joueur...
            </p>
            <p v-else-if="gameStore.status === 'playing' && gameStore.currentTurnId === gameStore.clientId" class="text-teal-400 font-black tracking-widest uppercase text-sm">
              Placez <span class="underline decoration-2 underline-offset-4 text-white">{{ selectedHandCard?.name }}</span> sur un emplacement (+)
            </p>
            <p v-else-if="gameStore.status === 'playing'" class="text-slate-500 font-black tracking-widest uppercase text-sm">
               Prêt pour votre tour...
            </p>
            <p v-else-if="gameStore.status === 'won'" class="text-emerald-400 font-black uppercase tracking-widest">Partie Terminée</p>
          </div>
        </div>

        <!-- Status / Logs panel -->

    <!-- Card Info Tooltip (Floating overlay in corner, anchored from bottom) -->
    <Transition name="fade">
      <div v-if="hoveredInfoCard" class="fixed bottom-48 left-8 pointer-events-none z-[100]">
        <div class="w-80 bg-slate-900/95 backdrop-blur-2xl rounded-[2rem] border border-indigo-500/20 shadow-[0_30px_60px_rgba(0,0,0,0.6)] overflow-hidden scale-in">
          <!-- Header -->
          <div class="p-6 pb-0">
            <h3 class="text-xl font-black text-white leading-tight mb-2">{{ hoveredInfoCard.name }}</h3>
            <div class="flex flex-wrap gap-2 mb-4">
              <span v-for="tag in hoveredInfoCard.tags" :key="tag.name" class="px-2 py-1 bg-indigo-500/20 text-indigo-300 text-[10px] font-black uppercase rounded-lg border border-indigo-500/30 tracking-widest">
                #{{ tag.name }}
              </span>
            </div>
          </div>
          
          <!-- Criteria Grid -->
          <div class="p-6 pt-0 space-y-3">
            <div class="h-px bg-white/5 w-full"></div>
            <p class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-4">Détails techniques</p>
            
            <div class="grid grid-cols-1 gap-2">
              <div v-for="(value, key) in hoveredInfoCard.attributes" :key="key" class="flex items-center gap-3 group/item bg-white/5 px-4 py-2 rounded-xl">
                <div class="w-1.5 h-1.5 rounded-full bg-indigo-500/50"></div>
                <span class="text-xs font-bold text-slate-300 uppercase tracking-widest">{{ key }}</span>
              </div>
            </div>
          </div>
          
          <!-- Card Image Preview (optional overlay style) -->
          <div v-if="hoveredInfoCard.image_url && !imageErrors.has(hoveredInfoCard.id)" class="w-full h-32 bg-slate-950/50 relative">
            <img :src="hoveredInfoCard.image_url" class="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-overlay" />
          </div>
        </div>
      </div>
    </Transition>
        <!-- Mode / Turn info -->
        <div class="hidden md:flex items-center gap-6">
           <div class="text-right">
             <p class="text-[10px] text-slate-600 font-black uppercase tracking-tighter">Deck Restant</p>
             <p class="text-xl font-black text-slate-300">{{ gameStore.deckCount }}</p>
           </div>
        </div>
      </div>
    </footer>

    <!-- Chat Drawer (Overlays Game And Footer) -->
    <div 
      class="absolute right-0 top-0 bottom-0 z-[60] flex-shrink-0 transition-transform duration-500 ease-in-out"
      :class="chatOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="w-[100vw] sm:w-96 h-full shadow-[-20px_0_50px_rgba(0,0,0,0.5)] bg-slate-900/80 backdrop-blur-3xl border-l border-white/10 flex flex-col relative pointer-events-auto">
        <!-- Chat Tab Toggle (Always visible, attached to the left of the drawer) -->
        <button 
          v-if="gameStore.status !== 'waiting' || chatOpen"
          @click="chatOpen = !chatOpen"
          class="absolute left-0 -translate-x-full top-1/2 -translate-y-1/2 px-2 py-4 md:px-3 md:py-6 bg-slate-900/40 backdrop-blur-3xl border border-white/10 border-r-0 rounded-l-[1.5rem] md:rounded-l-[2rem] text-slate-400 hover:text-teal-400 transition-all group z-[60]"
        >
          <div class="flex flex-col items-center gap-2 md:gap-4 font-black text-[10px] md:text-xs uppercase tracking-[0.2em] [writing-mode:vertical-lr] rotate-180">
            <span>Chat</span>
            <div class="w-1 h-1 md:w-1.5 md:h-1.5 rounded-full" :class="!chatOpen ? 'bg-teal-400 animate-pulse' : 'bg-slate-700'"></div>
          </div>
        </button>

        <div class="p-6 border-b border-white/5 flex items-center justify-between">
          <div class="flex flex-col">
            <h3 class="font-black uppercase tracking-widest text-xs text-slate-500">Discussion Room</h3>
            <button 
              @click="showLogs = !showLogs"
              class="flex items-center gap-1.5 mt-1 transition-colors group"
              :class="showLogs ? 'text-teal-500' : 'text-slate-600 hover:text-slate-400'"
            >
              <div class="w-2.5 h-2.5 rounded-full border border-current flex items-center justify-center">
                <div v-if="showLogs" class="w-1.5 h-1.5 bg-current rounded-full"></div>
              </div>
              <span class="text-[9px] font-black uppercase tracking-tighter">Journalisation {{ showLogs ? 'ON' : 'OFF' }}</span>
            </button>
          </div>
          <button 
            v-if="gameStore.status !== 'waiting'"
            @click="chatOpen = false" 
            class="text-slate-500 hover:text-white transition"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2" stroke-linecap="round"/></svg>
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-4 no-scrollbar">
          <div v-for="msg in visibleMessages" :key="msg.id" 
               class="flex flex-col" 
               :class="msg.clientId === gameStore.clientId ? 'items-end' : 'items-start'">
            
            <template v-if="msg.type === 'chat'">
              <span class="text-[9px] text-slate-600 mb-1 font-black uppercase tracking-tighter px-2">{{ msg.sender }}</span>
              <div 
                class="max-w-[90%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed"
                :class="msg.clientId === gameStore.clientId ? 'bg-indigo-600 text-white rounded-tr-none shadow-lg' : 'bg-slate-800 text-slate-200 rounded-tl-none border border-white/5'"
              >
                {{ msg.text }}
              </div>
            </template>
            
            <template v-else>
              <div 
                class="w-full py-2 px-3 border rounded-xl text-center transition-colors duration-300"
                :class="msg.type === 'error' ? 'bg-rose-500/20 border-rose-500/30 text-rose-200' : 'bg-white/5 border-white/5 text-slate-500'"
              >
                <span class="text-[10px] text-slate-500 italic font-medium">{{ msg.text }}</span>
              </div>
            </template>
          </div>
        </div>

        <div class="p-4 bg-slate-900 border-t border-white/10">
          <form @submit.prevent="sendChat" class="relative">
            <input 
              v-model="chatMessage"
              placeholder="Votre message..."
              class="w-full bg-slate-800 border border-white/10 rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-indigo-500 transition placeholder:text-slate-600 font-medium"
            />
            <button type="submit" class="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-indigo-500 text-white rounded-xl hover:bg-indigo-400 transition shadow-lg active:scale-90">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </form>
        </div>
      </div>
    </div>

    </div> <!-- End new wrapper -->

    <!-- System Toasts (Floating) -->
    <div class="fixed top-24 left-1/2 -translate-x-1/2 flex flex-col gap-3 z-40 pointer-events-none w-full max-w-lg items-center px-4">
        <TransitionGroup name="list">
            <div 
                v-for="msg in toasts" :key="msg.id"
                class="px-6 py-4 rounded-3xl font-bold shadow-2xl border backdrop-blur-2xl flex items-center gap-4 transition-all duration-500"
                :class="msg.type === 'error' ? 'bg-rose-500/10 border-rose-500/30 text-rose-300' : 'bg-teal-500/10 border-teal-500/30 text-teal-300'"
            >
                <div class="w-2.5 h-2.5 rounded-full shadow-lg" :class="msg.type === 'error' ? 'bg-rose-500 animate-pulse' : 'bg-teal-500 shadow-teal-500/50'"></div>
                <span class="text-sm tracking-wide">{{ msg.text }}</span>
            </div>
        </TransitionGroup>
    </div>

    <!-- Wiki Overlay -->
    <Transition name="fade">
      <div v-if="wikiSummary" class="fixed inset-0 z-[60] flex items-center justify-center p-6 bg-slate-950/40 backdrop-blur-sm pointer-events-none">
        <div class="w-full max-w-sm p-8 bg-slate-900 border border-white/10 rounded-[3rem] shadow-[0_0_100px_rgba(0,0,0,0.5)] relative animate-scale-up">
           <button @click="closeWiki" class="absolute top-6 right-6 p-2 text-slate-500 hover:text-white transition">
             <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2"/></svg>
           </button>
           <div class="w-12 h-12 bg-teal-500/20 rounded-2xl flex items-center justify-center mb-6">
             <span class="text-2xl font-serif italic text-teal-400">W</span>
           </div>
           <h4 class="text-xs font-black uppercase tracking-widest text-teal-500 mb-2">Wikipedia Insight</h4>
           <div class="h-max max-h-60 overflow-y-auto no-scrollbar">
             <p v-if="wikiLoading" class="animate-pulse text-slate-500 font-medium">Récupération des données...</p>
             <p v-else class="text-slate-300 leading-relaxed italic text-sm font-medium">"{{ wikiSummary }}"</p>
           </div>
           <p class="mt-6 text-[10px] text-slate-600 font-bold uppercase tracking-widest">Cliquez n'importe où sur la carte pour l'article complet</p>
        </div>
      </div>
    </Transition>
    
    <!-- Connection Status Overlay -->
    <Transition name="fade">
      <div v-if="!gameStore.connected" class="fixed inset-0 z-[100] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-6 text-center">
        <div class="max-w-xs animate-scale-up">
          <div class="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mx-auto mb-6"></div>
          <h2 class="text-2xl font-black mb-2 text-white">Connexion perdue</h2>
          <p class="text-slate-400 text-sm leading-relaxed mb-6">Tentative de reconnexion au salon en cours...</p>
          <button @click="router.push('/')" class="text-indigo-400 font-bold hover:text-indigo-300 transition text-sm flex items-center gap-2 mx-auto justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 19l-7-7m0 0l7-7m-7 7h18" stroke-width="2"/></svg>
            Retour à l'accueil
          </button>
        </div>
      </div>
    </Transition>

  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: translateY(-30px); }
.list-leave-to { opacity: 0; transform: translateY(-30px); }

@keyframes slide-in {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}
.animate-fade-in { animation: fade-in 0.5s ease-out; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes scale-up {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

.animate-scale-up { animation: scale-up 0.5s cubic-bezier(0.16, 1, 0.3, 1); }

.mask-fade-edges {
  mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}.scale-in {
  animation: tooltipScaleIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes tooltipScaleIn {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
