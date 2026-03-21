import json
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def import_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    with open("demo_cards.json", "rt", encoding="utf-8") as f:
        cards_data = json.load(f)
        
    for data in cards_data:
        db_tags = []
        for t_name in data.get("tag_names", []):
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
                image_url=data.get("image_url"),
                wiki_link=data.get("wiki_link"),
                attributes=data.get("attributes"),
                tags=db_tags
            )
            db.add(card)
            db.commit()
            
    db.close()
    print("Demo cards imported successfully into the database!")

if __name__ == "__main__":
    import_data()
