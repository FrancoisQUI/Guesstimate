from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Timeline CardGame API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

def validate_admin(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return True

@app.get("/verify-admin")
def verify_admin(is_admin: bool = Depends(validate_admin)):
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Timeline CardGame API"}

@app.post("/cards/", response_model=schemas.Card)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db), admin: bool = Depends(validate_admin)):
    db_tags = []
    for t_name in card.tag_names:
        tag = db.query(models.Tag).filter(models.Tag.name == t_name).first()
        if not tag:
            tag = models.Tag(name=t_name)
            db.add(tag)
        db_tags.append(tag)
        
    db_card = models.Card(
        name=card.name,
        image_url=card.image_url,
        wiki_link=card.wiki_link,
        attributes=card.attributes,
        tags=db_tags
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@app.get("/cards/", response_model=List[schemas.Card])
def read_cards(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    cards = db.query(models.Card).offset(skip).limit(limit).all()
    return cards

@app.post("/cards/bulk")
async def import_cards(cards: List[schemas.CardCreate], db: Session = Depends(get_db), admin: bool = Depends(validate_admin)):
    created_count = 0
    updated_count = 0
    for card in cards:
        db_tags = []
        for t_name in card.tag_names:
            tag = db.query(models.Tag).filter(models.Tag.name == t_name).first()
            if not tag:
                tag = models.Tag(name=t_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            db_tags.append(tag)
            
        db_card = db.query(models.Card).filter(models.Card.name == card.name).first()
        if not db_card:
            db_card = models.Card(
                name=card.name,
                image_url=card.image_url,
                wiki_link=card.wiki_link,
                attributes=card.attributes,
                tags=db_tags
            )
            db.add(db_card)
            created_count += 1
        else:
            # Update existing card
            if card.attributes:
                current_attrs = dict(db_card.attributes) if db_card.attributes else {}
                current_attrs.update(card.attributes)
                db_card.attributes = current_attrs
            
            # Merge tags
            current_tag_names = {t.name for t in db_card.tags}
            for tag in db_tags:
                if tag.name not in current_tag_names:
                    db_card.tags.append(tag)
            
            if card.image_url:
                db_card.image_url = card.image_url
            if card.wiki_link:
                db_card.wiki_link = card.wiki_link
            
            updated_count += 1
            
        db.commit()
    return {"message": f"{created_count} nouvelles cartes, {updated_count} mises à jour !"}

@app.get("/metadata/")
def get_metadata(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    tag_names = [t.name for t in tags]
    
    cards = db.query(models.Card).all()
    attr_keys = set()
    for card in cards:
        if card.attributes:
            attr_keys.update(card.attributes.keys())
            
    return {
        "tags": sorted(tag_names),
        "attributes": sorted(list(attr_keys))
    }

@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card: schemas.CardCreate, db: Session = Depends(get_db), admin: bool = Depends(validate_admin)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if not db_card:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Card not found")
        
    db_tags = []
    for t_name in card.tag_names:
        tag = db.query(models.Tag).filter(models.Tag.name == t_name).first()
        if not tag:
            tag = models.Tag(name=t_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        db_tags.append(tag)
        
    db_card.name = card.name
    db_card.image_url = card.image_url
    db_card.wiki_link = card.wiki_link
    db_card.attributes = card.attributes
    db_card.tags = db_tags
    
    db.commit()
    db.refresh(db_card)
    return db_card

@app.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), admin: bool = Depends(validate_admin)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card:
        db.delete(db_card)
        db.commit()
    return {"message": "Card deleted"}

from database import SessionLocal
import random

class ConnectionManager:
    def __init__(self):
        self.rooms = {}

    async def connect(self, websocket: WebSocket, room_id: str, client_id: str, name: str = None):
        await websocket.accept()
        await websocket.send_json({"action": "WELCOME", "client_id": client_id})
        if room_id not in self.rooms:
            self.rooms[room_id] = {
                "players": {}, # client_id -> {ws, hand, name}
                "player_order": [],
                "status": "waiting",
                "deck": [],
                "board": [],
                "current_turn_idx": 0,
                "attribute": "",
                "mode": "classique",
                "score_correct": 0,
                "score_total": 0,
                "creator_id": client_id,
                "last_placement": None
            }
        
        room = self.rooms[room_id]
        
        # S'assurer que le joueur n'existe pas déjà ou mettre à jour son WS
        if client_id in room["players"]:
            room["players"][client_id]["ws"] = websocket
            if name: # Mettre à jour le nom si fourni
                room["players"][client_id]["name"] = name
        else:
            # Nouveau joueur
            display_name = name if name else f"Joueur {len(room['player_order']) + 1}"
            room["players"][client_id] = {
                "ws": websocket,
                "hand": [],
                "name": display_name
            }
            room["player_order"].append(client_id)
            
        await self.send_game_state(room_id)

    async def disconnect(self, websocket: WebSocket, room_id: str, client_id: str):
        if room_id in self.rooms:
            room = self.rooms[room_id]
            if client_id in room["players"]:
                del room["players"][client_id]
            if client_id in room["player_order"]:
                room["player_order"].remove(client_id)
                # Migration d'hôte : si le créateur quitte, le plus ancien restant devient hôte
                if room["creator_id"] == client_id and room["player_order"]:
                    room["creator_id"] = room["player_order"][0]
            
            if not room["players"]:
                del self.rooms[room_id]
            else:
                await self.send_game_state(room_id)

    async def broadcast(self, message: dict, room_id: str):
        if room_id in self.rooms:
            for pid in self.rooms[room_id]["player_order"]:
                try:
                    ws = self.rooms[room_id]["players"][pid]["ws"]
                    await ws.send_json(message)
                except:
                    pass

    async def send_game_state(self, room_id: str):
        room = self.rooms.get(room_id)
        if not room: return
        
        # Self-healing host: si l'hôte n'est plus là, migrer
        if room["creator_id"] not in room["players"] and room["player_order"]:
            room["creator_id"] = room["player_order"][0]
        
        player_list = []
        for pid in room["player_order"]:
            p = room["players"][pid]
            player_list.append({
                "id": pid,
                "name": p["name"],
                "hand_count": len(p["hand"])
            })

        for pid in room["player_order"]:
            p = room["players"][pid]
            # Hide values of cards in hand to others, but current player sees their own values? 
            # Actually, per rules of Timeline, you don't see the values even in your own hand until you play them.
            safe_hand = []
            for c in p["hand"]:
                safe_hand.append({
                    "id": c["id"],
                    "name": c["name"],
                    "image_url": c["image_url"],
                    "wiki_link": c.get("wiki_link"),
                    "tags": c.get("tags", []),
                    "attributes": {k: "???" for k in c.get("attributes", {}).keys()},
                    "value": "?" # Hidden
                })
            
            state = {
                "action": "GAME_STATE",
                "status": room.get("status", "waiting"),
                "board": room.get("board", []),
                "hand": safe_hand,
                "players": player_list,
                "current_turn_id": room["player_order"][room["current_turn_idx"]] if room["player_order"] else None,
                "deck_count": len(room.get("deck", [])),
                "attribute": room.get("attribute", ""),
                "mode": room.get("mode", "classique"),
                "score_correct": room.get("score_correct", 0),
                "score_total": room.get("score_total", 0),
                "creator_id": room.get("creator_id"),
                "last_placement": room.get("last_placement")
            }
            try:
                await p["ws"].send_json(state)
            except:
                pass

    async def process_message(self, room_id: str, client_id: str, data: dict):
        room = self.rooms.get(room_id)
        if not room: return
        
        action = data.get("action")
        
        if action == "START_GAME":
            if room["creator_id"] != client_id:
                ws = room["players"][client_id]["ws"]
                await ws.send_json({"action": "ERROR", "message": "Seul le créateur peut lancer la partie"})
                return

            attr = data.get("attribute", "année")
            tags_str = data.get("tags", "tous")
            mode = data.get("mode", "classique")
            deck_limit = data.get("deck_limit", 0)
            hand_size = data.get("hand_size", 5)
            
            with SessionLocal() as db:
                cards = db.query(models.Card).all()
                valid_cards = []
                target_tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]
                
                for c in cards:
                    if not c.attributes or attr not in c.attributes:
                        continue
                    if "tous" not in target_tags and target_tags:
                        c_tags = [t.name.lower() for t in c.tags]
                        if not any(tt in c_tags for tt in target_tags):
                            continue
                    valid_cards.append({
                        "id": c.id, 
                        "name": c.name, 
                        "image_url": c.image_url,
                        "wiki_link": c.wiki_link, 
                        "tags": [{"name": t.name} for t in c.tags],
                        "attributes": c.attributes,
                        "value": c.attributes.get(attr)
                    })
            
            random.shuffle(valid_cards)
            
            if deck_limit > 0 and len(valid_cards) > deck_limit:
                valid_cards = valid_cards[:deck_limit]
            min_required = len(room["player_order"]) * hand_size + 1
            if len(valid_cards) < min_required:
                await self.broadcast({"action": "ERROR", "message": f"Pas assez de cartes ({len(valid_cards)} < {min_required}) !"}, room_id)
                return
                
            room["deck"] = valid_cards
            room["board"] = [room["deck"].pop()]
            
            # Distribute hands
            for pid in room["player_order"]:
                room["players"][pid]["hand"] = [room["deck"].pop() for _ in range(hand_size)]
            
            room["status"] = "playing"
            room["current_turn_idx"] = 0
            room["attribute"] = attr
            room["mode"] = mode
            room["score_correct"] = 0
            room["score_total"] = 0
            room["last_placement"] = None
            
            await self.send_game_state(room_id)
            
        elif action == "PLACE_CARD":
            if room["status"] != "playing": return
            
            # Check turn
            current_pid = room["player_order"][room["current_turn_idx"]]
            if client_id != current_pid:
                return # Not your turn
            
            player = room["players"][client_id]
            card_id = data.get("card_id")
            index = data.get("index")
            
            card = next((c for c in player["hand"] if c["id"] == card_id), None)
            if not card: return
            
            try: val = float(card["value"])
            except: val = 0.0
                
            is_valid = True
            if index > 0:
                try: prev_val = float(room["board"][index-1]["value"])
                except: prev_val = 0.0
                if val < prev_val: is_valid = False
            
            if index < len(room["board"]):
                try: next_val = float(room["board"][index]["value"])
                except: next_val = 0.0
                if val > next_val: is_valid = False
            
            player["hand"] = [c for c in player["hand"] if c["id"] != card_id]
            mode = room.get("mode", "classique")
            msg_type = "info"
            
            # Find correct index for auto-placement on failure
            correct_idx = len(room["board"])
            for i, c in enumerate(room["board"]):
                try: c_val = float(c["value"])
                except: c_val = 0.0
                if val <= c_val:
                    correct_idx = i
                    break

            if is_valid:
                room["board"].insert(index, card)
                room["last_placement"] = {"card_id": card["id"], "success": True}
                msg = f"{player['name']} a placé {card['name']}."
                if mode == "complet":
                    room["score_correct"] += 1
            else:
                room["board"].insert(correct_idx, card)
                room["last_placement"] = {"card_id": card["id"], "success": False}
                msg_type = "error"
                msg = f"Faux pour {player['name']} ! {card['name']} placé automatiquement."

            if mode == "complet":
                room["score_total"] += 1

            if room["deck"]:
                if mode == "complet" or (mode == "classique" and not is_valid):
                    player["hand"].append(room["deck"].pop())

            # Win condition
            if mode == "classique":
                if not player["hand"]:
                    room["status"] = "won"
                    msg = f"🏆 {player['name']} a gagné la partie !"
            else: # complet
                all_empty = all(len(room["players"][p]["hand"]) == 0 for p in room["player_order"])
                if all_empty and not room["deck"]:
                    room["status"] = "won"
                    msg = "Partie terminée !"

            # Next turn
            room["current_turn_idx"] = (room["current_turn_idx"] + 1) % len(room["player_order"])
            
            await self.broadcast({"action": "INFO", "message": msg, "type": msg_type}, room_id)
            await self.send_game_state(room_id)
            
        elif action == "RESET_GAME":
            # Only creator can reset
            if client_id != room.get("creator_id"):
                return
            
            room["status"] = "waiting"
            room["deck"] = []
            room["board"] = []
            room["score_correct"] = 0
            room["score_total"] = 0
            room["last_placement"] = None
            
            for pid in room["player_order"]:
                if pid in room["players"]:
                    room["players"][pid]["hand"] = []
            
            await self.broadcast({"action": "INFO", "message": "Le salon a été réinitialisé.", "type": "info"}, room_id)
            await self.send_game_state(room_id)
            
        elif action == "CHAT":
            msg_text = data.get("text", "")
            if msg_text:
                player_name = room["players"][client_id]["name"]
                await self.broadcast({
                    "action": "CHAT",
                    "sender": player_name,
                    "text": msg_text,
                    "client_id": client_id
                }, room_id)
        
        elif action == "UPDATE_NICKNAME":
            new_name = data.get("name")
            if new_name and client_id in room["players"]:
                old_name = room["players"][client_id]["name"]
                room["players"][client_id]["name"] = new_name
                await self.broadcast({
                    "action": "INFO", 
                    "message": f"{old_name} s'appelle désormais {new_name}", 
                    "type": "info"
                }, room_id)
                await self.send_game_state(room_id)

manager = ConnectionManager()

@app.get("/rooms/{room_id}/exists")
def check_room(room_id: str):
    return {"exists": room_id in manager.rooms}

@app.websocket("/ws/{client_id}/{room_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, room_id: str):
    name = websocket.query_params.get("name")
    await manager.connect(websocket, room_id, client_id, name)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.process_message(room_id, client_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id, client_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
