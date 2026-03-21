import { defineStore } from 'pinia'

export const useGameStore = defineStore('game', {
  state: () => ({
    socket: null,
    connected: false,
    status: 'waiting',
    board: [],
    hand: [],
    deckCount: 0,
    attribute: '',
    mode: 'classique',
    scoreCorrect: 0,
    scoreTotal: 0,
    players: [],
    currentTurnId: null,
    messages: [],
    reconnectInterval: null,
    isConnecting: false,
    currentRoomId: null,
    clientId: null,
    nickname: sessionStorage.getItem('nickname') || '',
    lastPlacement: null,
  }),
  actions: {
    resetLocalState() {
      this.status = 'waiting';
      this.board = [];
      this.hand = [];
      this.deckCount = 0;
      this.attribute = '';
      this.mode = 'classique';
      this.scoreCorrect = 0;
      this.scoreTotal = 0;
      this.players = [];
      this.currentTurnId = null;
      this.messages = [];
      this.lastPlacement = null;
    },
    setNickname(name) {
      this.nickname = name;
      sessionStorage.setItem('nickname', name);
    },
    connect(roomId) {
      if (this.currentRoomId !== roomId) {
        this.disconnect();
        this.resetLocalState();
        this.currentRoomId = roomId;
      }
      
      if (!this.clientId) {
        this.clientId = sessionStorage.getItem('clientId') || `player-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        sessionStorage.setItem('clientId', this.clientId);
      }
      
      if (this.socket || this.isConnecting) return;
      this.isConnecting = true;
      
      const baseUrl = window.location.host.includes('localhost') ? 'ws://localhost:8000' : `ws://${window.location.host}`;
      let url = `${baseUrl}/ws/${this.clientId}/${roomId}`;
      if (this.nickname) {
        url += `?name=${encodeURIComponent(this.nickname)}`;
      }
      
      this.socket = new WebSocket(url);
      
      this.socket.onopen = () => {
        console.log("Connected to game room");
        this.connected = true;
        this.isConnecting = false;
        if (this.reconnectInterval) {
          clearInterval(this.reconnectInterval);
          this.reconnectInterval = null;
        }
      };
      
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.action === "GAME_STATE") {
          this.status = data.status;
          this.board = data.board;
          this.hand = data.hand;
          this.deckCount = data.deck_count;
          this.attribute = data.attribute;
          this.mode = data.mode || 'classique';
          this.scoreCorrect = data.score_correct || 0;
          this.scoreTotal = data.score_total || 0;
          this.players = data.players || [];
          this.currentTurnId = data.current_turn_id;
          this.creatorId = data.creator_id;
          this.lastPlacement = data.last_placement;
        } else if (data.action === "INFO" || data.action === "ERROR" || data.action === "CHAT") {
          const msg = {
            id: Date.now() + Math.random(),
            text: data.message || data.text,
            type: data.type || (data.action === "ERROR" ? "error" : "info"),
            sender: data.sender,
            clientId: data.client_id
          };
          if (data.action === "CHAT") msg.type = "chat";
          this.messages.push(msg);
        }
      };
      
      this.socket.onclose = () => {
        console.log("Disconnected from game room");
        this.connected = false;
        this.socket = null;
        this.isConnecting = false;
        
        // Auto-reconnect if not intentionally disconnected
        if (!this.reconnectInterval) {
          this.reconnectInterval = setInterval(() => {
            console.log("Attempting to reconnect...");
            this.connect(roomId);
          }, 3000);
        }
      };
    },
    disconnect() {
      if (this.reconnectInterval) {
        clearInterval(this.reconnectInterval);
        this.reconnectInterval = null;
      }
      if (this.socket) {
        this.socket.close();
        this.socket = null;
        this.connected = false;
      }
    },
    startGame(attribute, tags, mode, deckLimit = 0, handSize = 5) {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                action: "START_GAME",
                attribute: attribute,
                tags: tags,
                mode: mode,
                deck_limit: deckLimit,
                hand_size: handSize
            }))
        }
    },
    resetGame() {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                action: "RESET_GAME"
            }))
        }
    },
    placeCard(cardId, index) {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                action: "PLACE_CARD",
                card_id: cardId,
                index: index
            }))
        }
    },
    sendMessage(text) {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                action: "CHAT",
                text: text
            }))
        }
    },
    updateNickname(newName) {
        if (this.socket && this.connected) {
            this.socket.send(JSON.stringify({
                action: "UPDATE_NICKNAME",
                name: newName
            }));
            this.setNickname(newName); // Update local storage too
        }
    }
  }
})
