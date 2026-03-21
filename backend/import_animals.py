import json
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def import_animals():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    animals_data = [
        {"name": "Éléphant d'Afrique", "taille_cm": 350, "poids_kg": 6000, "esperance_vie": 70},
        {"name": "Lion", "taille_cm": 120, "poids_kg": 190, "esperance_vie": 14},
        {"name": "Tigre de Sibérie", "taille_cm": 110, "poids_kg": 300, "esperance_vie": 15},
        {"name": "Girafe", "taille_cm": 530, "poids_kg": 1200, "esperance_vie": 25},
        {"name": "Hippopotame", "taille_cm": 150, "poids_kg": 1500, "esperance_vie": 40},
        {"name": "Rhinocéros blanc", "taille_cm": 180, "poids_kg": 2300, "esperance_vie": 50},
        {"name": "Gorille à dos argenté", "taille_cm": 170, "poids_kg": 160, "esperance_vie": 40},
        {"name": "Panthère noire", "taille_cm": 70, "poids_kg": 60, "esperance_vie": 12},
        {"name": "Guépard", "taille_cm": 80, "poids_kg": 50, "esperance_vie": 12},
        {"name": "Zèbre", "taille_cm": 140, "poids_kg": 400, "esperance_vie": 25},
        {"name": "Kangourou roux", "taille_cm": 150, "poids_kg": 85, "esperance_vie": 20},
        {"name": "Ours polaire", "taille_cm": 140, "poids_kg": 450, "esperance_vie": 25},
        {"name": "Ours brun", "taille_cm": 110, "poids_kg": 350, "esperance_vie": 25},
        {"name": "Loup gris", "taille_cm": 80, "poids_kg": 40, "esperance_vie": 10},
        {"name": "Renard roux", "taille_cm": 40, "poids_kg": 7, "esperance_vie": 4},
        {"name": "Aigle royal", "taille_cm": 80, "poids_kg": 5, "esperance_vie": 30},
        {"name": "Autruche", "taille_cm": 250, "poids_kg": 130, "esperance_vie": 40},
        {"name": "Manchot empereur", "taille_cm": 115, "poids_kg": 30, "esperance_vie": 20},
        {"name": "Crocodile du Nil", "taille_cm": 500, "poids_kg": 500, "esperance_vie": 70},
        {"name": "Alligator d'Amérique", "taille_cm": 400, "poids_kg": 360, "esperance_vie": 50},
        {"name": "Grand requin blanc", "taille_cm": 450, "poids_kg": 1100, "esperance_vie": 70},
        {"name": "Orque", "taille_cm": 700, "poids_kg": 4000, "esperance_vie": 50},
        {"name": "Baleine bleue", "taille_cm": 2500, "poids_kg": 150000, "esperance_vie": 90},
        {"name": "Dauphin", "taille_cm": 250, "poids_kg": 150, "esperance_vie": 40},
        {"name": "Phoque commun", "taille_cm": 160, "poids_kg": 100, "esperance_vie": 25},
        {"name": "Morse", "taille_cm": 300, "poids_kg": 1000, "esperance_vie": 30},
        {"name": "Cheval de trait", "taille_cm": 170, "poids_kg": 800, "esperance_vie": 25},
        {"name": "Vache laitière", "taille_cm": 140, "poids_kg": 700, "esperance_vie": 15},
        {"name": "Cochon", "taille_cm": 80, "poids_kg": 150, "esperance_vie": 10},
        {"name": "Mouton", "taille_cm": 90, "poids_kg": 60, "esperance_vie": 12},
        {"name": "Chien", "taille_cm": 60, "poids_kg": 30, "esperance_vie": 12},
        {"name": "Chat domestique", "taille_cm": 25, "poids_kg": 4.5, "esperance_vie": 15},
        {"name": "Chimpanzé", "taille_cm": 120, "poids_kg": 50, "esperance_vie": 45},
        {"name": "Orang-outan", "taille_cm": 130, "poids_kg": 75, "esperance_vie": 45},
        {"name": "Panda géant", "taille_cm": 75, "poids_kg": 100, "esperance_vie": 20},
        {"name": "Koala", "taille_cm": 75, "poids_kg": 10, "esperance_vie": 15},
        {"name": "Paresseux", "taille_cm": 60, "poids_kg": 6, "esperance_vie": 20},
        {"name": "Élan", "taille_cm": 190, "poids_kg": 500, "esperance_vie": 15},
        {"name": "Cerf élaphe", "taille_cm": 130, "poids_kg": 200, "esperance_vie": 15},
        {"name": "Bison d'Amérique", "taille_cm": 180, "poids_kg": 900, "esperance_vie": 20},
        {"name": "Chameau", "taille_cm": 200, "poids_kg": 600, "esperance_vie": 40},
        {"name": "Lama", "taille_cm": 180, "poids_kg": 140, "esperance_vie": 20},
        {"name": "Marmotte", "taille_cm": 50, "poids_kg": 4, "esperance_vie": 15},
        {"name": "Souris domestique", "taille_cm": 8, "poids_kg": 0.02, "esperance_vie": 2},
        {"name": "Rat brun", "taille_cm": 25, "poids_kg": 0.3, "esperance_vie": 2},
        {"name": "Crapaud", "taille_cm": 10, "poids_kg": 0.05, "esperance_vie": 10},
        {"name": "Tortue des Galápagos", "taille_cm": 150, "poids_kg": 250, "esperance_vie": 100},
        {"name": "Anaconda géant", "taille_cm": 600, "poids_kg": 100, "esperance_vie": 10},
        {"name": "Caméléon", "taille_cm": 30, "poids_kg": 0.1, "esperance_vie": 5},
        {"name": "Mygale", "taille_cm": 12, "poids_kg": 0.08, "esperance_vie": 15}
    ]

    count = 0
    for data in animals_data:
        db_tags = []
        for t_name in ["animaux", "nature"]:
            tag = db.query(models.Tag).filter(models.Tag.name == t_name).first()
            if not tag:
                tag = models.Tag(name=t_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            db_tags.append(tag)
            
        card = db.query(models.Card).filter(models.Card.name == data["name"]).first()
        if not card:
            card = models.Card(
                name=data["name"],
                image_url=None,
                wiki_link=f"https://fr.wikipedia.org/wiki/{data['name'].replace(' ', '_')}",
                attributes={
                    "taille_cm": data["taille_cm"],
                    "poids_kg": data["poids_kg"],
                    "esperance_vie_annees": data["esperance_vie"]
                },
                tags=db_tags
            )
            db.add(card)
            db.commit()
            count += 1
            
    db.close()
    print(f"Bdd mise à jour avec {count} nouveaux animaux!")

if __name__ == "__main__":
    import_animals()
