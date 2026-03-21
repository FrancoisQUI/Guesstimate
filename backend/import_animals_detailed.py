import models
from database import SessionLocal, engine

def import_animals():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    print("Nettoyage des anciens animaux...")
    animal_tag = db.query(models.Tag).filter(models.Tag.name == "animaux").first()
    if animal_tag:
        # Get all cards with this tag
        cards = db.query(models.Card).all()
        for c in cards:
            if animal_tag in c.tags:
                db.delete(c)
        db.commit()
    else:
        animal_tag = models.Tag(name="animaux")
        db.add(animal_tag)
        db.commit()
        db.refresh(animal_tag)

    # 250 ANIMALS DATA (Compact format)
    # n: name, h: height_cm, w: weight_kg, e: expectancy, t: custom_tags
    data = [
        # FELINS (15)
        {"n":"Lion","h":120,"w":190,"e":14,"t":["mamifère","félidé","afrique","savane"]},
        {"n":"Tigre du Bengale","h":110,"w":220,"e":15,"t":["mamifère","félidé","asie","forêt"]},
        {"n":"Tigre de Sibérie","h":110,"w":300,"e":15,"t":["mamifère","félidé","asie","froid"]},
        {"n":"Jaguar","h":75,"w":95,"e":12,"t":["mamifère","félidé","amérique du sud","forêt","pays:brésil"]},
        {"n":"Léopard des neiges","h":60,"w":45,"e":15,"t":["mamifère","félidé","asie","montagne"]},
        {"n":"Léopard d'Afrique","h":70,"w":60,"e":12,"t":["mamifère","félidé","afrique","savane"]},
        {"n":"Guépard","h":85,"w":50,"e":12,"t":["mamifère","félidé","afrique","savane"]},
        {"n":"Puma","h":75,"w":70,"e":13,"t":["mamifère","félidé","amérique du nord","montagne"]},
        {"n":"Lynx boréal","h":65,"w":25,"e":15,"t":["mamifère","félidé","europe","forêt"]},
        {"n":"Lynx roux (Bobcat)","h":50,"w":12,"e":12,"t":["mamifère","félidé","amérique du nord","forêt"]},
        {"n":"Serval","h":60,"w":15,"e":11,"t":["mamifère","félidé","afrique","savane"]},
        {"n":"Caracal","h":45,"w":18,"e":12,"t":["mamifère","félidé","afrique","désert"]},
        {"n":"Ocelot","h":45,"w":11,"e":10,"t":["mamifère","félidé","amérique centrale","forêt"]},
        {"n":"Margay","h":40,"w":4,"e":12,"t":["mamifère","félidé","amérique du sud","forêt"]},
        {"n":"Chat de Pallas","h":30,"w":4.5,"e":10,"t":["mamifère","félidé","asie","montagne"]},

        # CANIDES (10)
        {"n":"Loup gris","h":85,"w":40,"e":10,"t":["mamifère","canidé","europe","forêt"]},
        {"n":"Loup arctique","h":80,"w":45,"e":10,"t":["mamifère","canidé","arctique","froid"]},
        {"n":"Renard roux","h":40,"w":7,"e":4,"t":["mamifère","canidé","europe","forêt"]},
        {"n":"Renard polaire","h":30,"w":4,"e":6,"t":["mamifère","canidé","arctique","froid"]},
        {"n":"Coyote","h":60,"w":15,"e":12,"t":["mamifère","canidé","amérique du nord","prairie"]},
        {"n":"Chacal doré","h":45,"w":12,"e":10,"t":["mamifère","canidé","asie","savane"]},
        {"n":"Lycaon","h":75,"w":25,"e":10,"t":["mamifère","canidé","afrique","savane"]},
        {"n":"Dingo","h":55,"w":18,"e":13,"t":["mamifère","canidé","océanie","pays:australie"]},
        {"n":"Fennec","h":20,"w":1.5,"e":12,"t":["mamifère","canidé","afrique","désert","pays:algérie"]},
        {"n":"Dhole","h":50,"w":15,"e":10,"t":["mamifère","canidé","asie","forêt"]},

        # PRIMATES (15)
        {"n":"Gorille des montagnes","h":170,"w":180,"e":40,"t":["mamifère","primate","afrique","montagne"]},
        {"n":"Gorille de plaine","h":160,"w":160,"e":45,"t":["mamifère","primate","afrique","forêt"]},
        {"n":"Chimpanzé","h":130,"w":50,"e":45,"t":["mamifère","primate","afrique","forêt"]},
        {"n":"Bonobo","h":110,"w":40,"e":40,"t":["mamifère","primate","afrique","forêt"]},
        {"n":"Orang-outan de Bornéo","h":140,"w":80,"e":45,"t":["mamifère","primate","asie","forêt","pays:indonésie"]},
        {"n":"Orang-outan de Sumatra","h":130,"w":70,"e":50,"t":["mamifère","primate","asie","forêt","pays:indonésie"]},
        {"n":"Gibbon","h":60,"w":7,"e":25,"t":["mamifère","primate","asie","forêt"]},
        {"n":"Babouin Anubis","h":75,"w":30,"e":30,"t":["mamifère","primate","afrique","savane"]},
        {"n":"Mandrill","h":80,"w":35,"e":20,"t":["mamifère","primate","afrique","forêt"]},
        {"n":"Ouistiti","h":20,"w":0.4,"e":12,"t":["mamifère","primate","amérique du sud","forêt"]},
        {"n":"Capucin","h":45,"w":4,"e":20,"t":["mamifère","primate","amérique du sud","forêt"]},
        {"n":"Atèle (Singe-araignée)","h":55,"w":9,"e":25,"t":["mamifère","primate","amérique du sud","forêt"]},
        {"n":"Aye-aye","h":40,"w":2.5,"e":20,"t":["mamifère","primate","afrique","pays:madagascar"]},
        {"n":"Lémur catta","h":45,"w":3,"e":18,"t":["mamifère","primate","afrique","pays:madagascar"]},
        {"n":"Macaque japonais","h":60,"w":11,"e":25,"t":["mamifère","primate","asie","pays:japon","froid"]},

        # ONGULES (30)
        {"n":"Éléphant d'Afrique","h":350,"w":6000,"e":70,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Éléphant d'Asie","h":270,"w":4000,"e":60,"t":["mamifère","onglet","asie","forêt"]},
        {"n":"Girafe réticulée","h":530,"w":1200,"e":25,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Zèbre de montagne","h":130,"w":300,"e":20,"t":["mamifère","onglet","afrique","montagne"]},
        {"n":"Zèbre des plaines","h":140,"w":350,"e":25,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Rhinocéros noir","h":160,"w":1400,"e":40,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Rhinocéros blanc","h":180,"w":2300,"e":45,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Hippopotame","h":150,"w":1500,"e":40,"t":["mamifère","onglet","afrique","aquatique"]},
        {"n":"Gnou bleu","h":135,"w":250,"e":20,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Buffle d'Afrique","h":160,"w":800,"e":20,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Élan (Orignal)","h":200,"w":600,"e":15,"t":["mamifère","onglet","europe","forêt","froid"]},
        {"n":"Cerf élaphe","h":130,"w":220,"e":15,"t":["mamifère","onglet","europe","forêt"]},
        {"n":"Daim","h":100,"w":80,"e":16,"t":["mamifère","onglet","europe","forêt"]},
        {"n":"Renne (Caribou)","h":120,"w":180,"e":15,"t":["mamifère","onglet","arctique","froid"]},
        {"n":"Chevreuil","h":75,"w":30,"e":12,"t":["mamifère","onglet","europe","forêt"]},
        {"n":"Sanglier","h":90,"w":150,"e":10,"t":["mamifère","onglet","europe","forêt"]},
        {"n":"Phacochère","h":75,"w":100,"e":15,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Chameau de Bactriane","h":210,"w":600,"e":40,"t":["mamifère","onglet","asie","désert"]},
        {"n":"Dromadaire","h":200,"w":500,"e":40,"t":["mamifère","onglet","afrique","désert"]},
        {"n":"Lama","h":180,"w":150,"e":20,"t":["mamifère","onglet","amérique du sud","montagne"]},
        {"n":"Alpaga","h":100,"w":70,"e":20,"t":["mamifère","onglet","amérique du sud","montagne"]},
        {"n":"Guanaco","h":115,"w":120,"e":25,"t":["mamifère","onglet","amérique du sud","prairie"]},
        {"n":"Vigogne","h":90,"w":50,"e":20,"t":["mamifère","onglet","amérique du sud","montagne"]},
        {"n":"Tapir du Brésil","h":100,"w":250,"e":30,"t":["mamifère","onglet","amérique du sud","forêt"]},
        {"n":"Okapi","h":160,"w":250,"e":30,"t":["mamifère","onglet","afrique","forêt"]},
        {"n":"Oryx","h":120,"w":200,"e":20,"t":["mamifère","onglet","afrique","désert"]},
        {"n":"Gazelle de Thomson","h":65,"w":25,"e":10,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Impala","h":90,"w":60,"e":15,"t":["mamifère","onglet","afrique","savane"]},
        {"n":"Bouquetin des Alpes","h":100,"w":100,"e":18,"t":["mamifère","onglet","europe","montagne"]},
        {"n":"Mouflon","h":90,"w":50,"e":12,"t":["mamifère","onglet","europe","montagne"]},

        # MARINS (15)
        {"n":"Baleine bleue","h":450,"w":150000,"e":90,"t":["mamifère","marin","océan"]},
        {"n":"Baleine à bosse","h":400,"w":35000,"e":50,"t":["mamifère","marin","océan"]},
        {"n":"Orque","h":700,"w":5000,"e":60,"t":["mamifère","marin","océan"]},
        {"n":"Grand dauphin","h":250,"w":250,"e":45,"t":["mamifère","marin","océan"]},
        {"n":"Marsouin commun","h":160,"w":60,"e":20,"t":["mamifère","marin","océan"]},
        {"n":"Cachalot","h":1800,"w":45000,"e":70,"t":["mamifère","marin","océan"]},
        {"n":"Beluga","h":450,"w":1500,"e":40,"t":["mamifère","marin","arctique"]},
        {"n":"Narval","h":500,"w":1200,"e":50,"t":["mamifère","marin","arctique"]},
        {"n":"Morse","h":320,"w":1000,"e":35,"t":["mamifère","marin","arctique"]},
        {"n":"Phoque moine","h":240,"w":280,"e":25,"t":["mamifère","marin","océan"]},
        {"n":"Otarie de Californie","h":220,"w":300,"e":20,"t":["mamifère","marin","océan"]},
        {"n":"Éléphant de mer","h":500,"w":3000,"e":20,"t":["mamifère","marin","océan"]},
        {"n":"Lamantin","h":350,"w":500,"e":50,"t":["mamifère","marin","aquatique"]},
        {"n":"Dugong","h":300,"w":400,"e":70,"t":["mamifère","marin","aquatique"]},
        {"n":"Loutre de mer","h":140,"w":35,"e":18,"t":["mamifère","marin","océan"]},

        # RONGEURS / PETITS (15)
        {"n":"Castor d'Europe","h":35,"w":25,"e":15,"t":["mamifère","rongeur","europe","aquatique"]},
        {"n":"Écureuil roux","h":25,"w":0.3,"e":7,"t":["mamifère","rongeur","europe","forêt"]},
        {"n":"Marmotte des Alpes","h":55,"w":6,"e":15,"t":["mamifère","rongeur","europe","montagne"]},
        {"n":"Porc-épic","h":75,"w":15,"e":20,"t":["mamifère","rongeur","afrique","savane"]},
        {"n":"Hérisson européen","h":25,"w":1,"e":5,"t":["mamifère","insectivore","europe","jardin"]},
        {"n":"Taupe d'Europe","h":15,"w":0.1,"e":4,"t":["mamifère","insectivore","europe","jardin"]},
        {"n":"Musaraigne carrelée","h":8,"w":0.01,"e":2,"t":["mamifère","insectivore","europe","jardin"]},
        {"n":"Raton laveur","h":50,"w":8,"e":5,"t":["mamifère","omnivore","amérique du nord","forêt"]},
        {"n":"Blaireau européen","h":80,"w":12,"e":12,"t":["mamifère","mustélidé","europe","forêt"]},
        {"n":"Putois","h":40,"w":1,"e":8,"t":["mamifère","mustélidé","europe","forêt"]},
        {"n":"Belette","h":20,"w":0.1,"e":4,"t":["mamifère","mustélidé","europe","forêt"]},
        {"n":"Hermine","h":25,"w":0.3,"e":7,"t":["mamifère","mustélidé","europe","forêt"]},
        {"n":"Martre des pins","h":50,"w":1.5,"e":10,"t":["mamifère","mustélidé","europe","forêt"]},
        {"n":"Loir gris","h":18,"w":0.15,"e":6,"t":["mamifère","rongeur","europe","forêt"]},
        {"n":"Hamster d'Europe","h":25,"w":0.4,"e":3,"t":["mamifère","rongeur","europe","prairie"]},

        # MARSUPIAUX (10)
        {"n":"Kangourou roux","h":160,"w":85,"e":20,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Kangourou géant","h":180,"w":60,"e":20,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Koala","h":75,"w":10,"e":15,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Wombat","h":100,"w":30,"e":15,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Diable de Tasmanie","h":60,"w":10,"e":6,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Wallaby","h":90,"w":20,"e":15,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Opossum de Virginie","h":50,"w":4,"e":3,"t":["mamifère","marsupial","amérique du nord"]},
        {"n":"Planeur de sucre","h":20,"w":0.15,"e":12,"t":["mamifère","marsupial","océanie"]},
        {"n":"Quokka","h":50,"w":3.5,"e":10,"t":["mamifère","marsupial","océanie","pays:australie"]},
        {"n":"Numbat","h":25,"w":0.5,"e":5,"t":["mamifère","marsupial","océanie","pays:australie"]},

        # AUTRES MAMMIFERES (15)
        {"n":"Ours polaire","h":140,"w":500,"e":25,"t":["mamifère","ours","arctique","froid"]},
        {"n":"Ours brun","h":130,"w":400,"e":25,"t":["mamifère","ours","europe","forêt"]},
        {"n":"Ours noir d'Amérique","h":110,"w":250,"e":20,"t":["mamifère","ours","amérique du nord","forêt"]},
        {"n":"Grizzly","h":130,"w":350,"e":25,"t":["mamifère","ours","amérique du nord","forêt"]},
        {"n":"Panda géant","h":85,"w":120,"e":20,"t":["mamifère","ours","asie","pays:chine"]},
        {"n":"Petit panda (Roux)","h":60,"w":5,"e":12,"t":["mamifère","asie","forêt","pays:chine"]},
        {"n":"Paresseux à trois doigts","h":60,"w":5,"e":20,"t":["mamifère","amérique du sud","forêt"]},
        {"n":"Tatou à neuf bandes","h":45,"w":5,"e":15,"t":["mamifère","amérique","prairie"]},
        {"n":"Grand fourmilier","h":120,"w":40,"e":15,"t":["mamifère","amérique du sud","savane"]},
        {"n":"Ornithorynque","h":45,"w":2,"e":12,"t":["mamifère","monotrème","océanie","pays:australie"]},
        {"n":"Échidné","h":40,"w":4,"e":40,"t":["mamifère","monotrème","océanie","pays:australie"]},
        {"n":"Chauve-souris (Grand murin)","h":12,"w":0.03,"e":15,"t":["mamifère","volant","europe"]},
        {"n":"Renard volant (Roussette)","h":30,"w":1.2,"e":20,"t":["mamifère","volant","océanie"]},
        {"n":"Lynx d'Espagne","h":70,"w":13,"e":13,"t":["mamifère","félidé","europe","pays:espagne"]},
        {"n":"Bison d'Europe","h":180,"w":800,"e":20,"t":["mamifère","onglet","europe","forêt"]},

        # OISEAUX - RAPACES (12)
        {"n":"Aigle royal","h":85,"w":5,"e":30,"t":["oiseau","rapace","europe","montagne"]},
        {"n":"Pygargue à tête blanche","h":90,"w":6,"e":25,"t":["oiseau","rapace","amérique du nord"]},
        {"n":"Faucon pèlerin","h":45,"w":1,"e":15,"t":["oiseau","rapace","mondial","vitesse"]},
        {"n":"Faucon crécerelle","h":35,"w":0.2,"e":12,"t":["oiseau","rapace","europe"]},
        {"n":"Autour des palombes","h":55,"w":1.2,"e":15,"t":["oiseau","rapace","europe","forêt"]},
        {"n":"Chouette effraie","h":35,"w":0.3,"e":15,"t":["oiseau","rapace","europe","nuit"]},
        {"n":"Hibou grand-duc","h":70,"w":3,"e":20,"t":["oiseau","rapace","europe","nuit"]},
        {"n":"Hibou petit-duc","h":20,"w":0.1,"e":10,"t":["oiseau","rapace","europe","nuit"]},
        {"n":"Vautour fauve","h":110,"w":10,"e":35,"t":["oiseau","rapace","europe","nécrophage"]},
        {"n":"Gypaète barbu","h":120,"w":7,"e":40,"t":["oiseau","rapace","europe","montagne"]},
        {"n":"Condor des Andes","h":130,"w":12,"e":50,"t":["oiseau","rapace","amérique du sud","montagne"]},
        {"n":"Messager sagittaire","h":140,"w":4,"e":15,"t":["oiseau","rapace","afrique","savane"]},

        # OISEAUX - AQUATIQUES (15)
        {"n":"Manchot empereur","h":115,"w":35,"e":20,"t":["oiseau","aquatique","antarctique","froid"]},
        {"n":"Manchot de Magellan","h":70,"w":5,"e":20,"t":["oiseau","aquatique","amérique du sud"]},
        {"n":"Gorfou sauteur","h":55,"w":3,"e":15,"t":["oiseau","aquatique","antarctique"]},
        {"n":"Albatros hurleur","h":120,"w":10,"e":50,"t":["oiseau","marin","océan"]},
        {"n":"Pétrel géant","h":90,"w":5,"e":25,"t":["oiseau","marin","antarctique"]},
        {"n":"Macareux moine","h":30,"w":0.5,"e":20,"t":["oiseau","marin","europe","atlantique"]},
        {"n":"Fou de Bassan","h":90,"w":3,"e":20,"t":["oiseau","marin","europe"]},
        {"n":"Grand Cormoran","h":90,"w":3,"e":15,"t":["oiseau","marin","europe"]},
        {"n":"Héron cendré","h":100,"w":1.5,"e":20,"t":["oiseau","aquatique","europe","étang"]},
        {"n":"Grande aigrette","h":90,"w":1,"e":15,"t":["oiseau","aquatique","mondial"]},
        {"n":"Cigogne blanche","h":110,"w":3.5,"e":20,"t":["oiseau","aquatique","europe","migration"]},
        {"n":"Grue cendrée","h":120,"w":5,"e":25,"t":["oiseau","aquatique","europe","migration"]},
        {"n":"Flamant rose","h":130,"w":3,"e":30,"t":["oiseau","aquatique","afrique","étang"]},
        {"n":"Cygne tuberculé","h":150,"w":12,"e":20,"t":["oiseau","aquatique","europe","étang"]},
        {"n":"Canard colvert","h":60,"w":1.2,"e":10,"t":["oiseau","aquatique","europe","étang"]},

        # OISEAUX - EXOTIQUES (15)
        {"n":"Ara bleu et jaune","h":90,"w":1,"e":50,"t":["oiseau","exotique","amérique du sud","forêt"]},
        {"n":"Cacatoès à huppe jaune","h":50,"w":0.8,"e":40,"t":["oiseau","exotique","océanie","pays:australie"]},
        {"n":"Inséparable","h":15,"w":0.05,"e":12,"t":["oiseau","exotique","afrique"]},
        {"n":"Toucan toco","h":60,"w":0.6,"e":20,"t":["oiseau","exotique","amérique du sud","forêt"]},
        {"n":"Colibri d'Elena","h":6,"w":0.002,"e":5,"t":["oiseau","exotique","amérique","fleur"]},
        {"n":"Oiseau-lyre","h":90,"w":1,"e":20,"t":["oiseau","exotique","océanie","pays:australie"]},
        {"n":"Paradisier grand-émeraude","h":40,"w":0.2,"e":15,"t":["oiseau","exotique","océanie"]},
        {"n":"Perruche callopsitte","h":30,"w":0.1,"e":15,"t":["oiseau","exotique","océanie","pays:australie"]},
        {"n":"Martin-pêcheur d'Europe","h":17,"w":0.04,"e":7,"t":["oiseau","exotique","europe","rivière"]},
        {"n":"Guêpier d'Europe","h":28,"w":0.06,"e":6,"t":["oiseau","exotique","europe"]},
        {"n":"Rollier d'Europe","h":30,"w":0.15,"e":10,"t":["oiseau","exotique","europe"]},
        {"n":"Calao bicorne","h":120,"w":3,"e":40,"t":["oiseau","exotique","asie","forêt"]},
        {"n":"Quetzal resplendissant","h":40,"w":0.2,"e":10,"t":["oiseau","exotique","amérique centrale"]},
        {"n":"Hoazin","h":65,"w":0.8,"e":15,"t":["oiseau","exotique","amérique du sud","forêt"]},
        {"n":"Ibis rouge","h":60,"w":0.7,"e":20,"t":["oiseau","exotique","amérique du sud","marais"]},

        # OISEAUX - TERRESTRES / AUTRES (18)
        {"n":"Autruche d'Afrique","h":250,"w":130,"e":40,"t":["oiseau","terrestre","afrique","savane"]},
        {"n":"Émeu d'Australie","h":170,"w":45,"e":15,"t":["oiseau","terrestre","océanie","pays:australie"]},
        {"n":"Casoar à casque","h":160,"w":60,"e":40,"t":["oiseau","terrestre","océanie","forêt"]},
        {"n":"Kiwi austral","h":40,"w":3,"e":30,"t":["oiseau","terrestre","océanie","pays:nouvelle-zélande"]},
        {"n":"Coq de roche péruvien","h":30,"w":0.2,"e":10,"t":["oiseau","exotique","amérique du sud"]},
        {"n":"Faisan de Colchide","h":85,"w":1.2,"e":10,"t":["oiseau","terrestre","europe"]},
        {"n":"Perdrix rouge","h":35,"w":0.5,"e":6,"t":["oiseau","terrestre","europe"]},
        {"n":"Caille des blés","h":18,"w":0.1,"e":3,"t":["oiseau","terrestre","europe"]},
        {"n":"Paon bleu","h":200,"w":5,"e":20,"t":["oiseau","terrestre","asie","pays:inde"]},
        {"n":"Dindon sauvage","h":110,"w":8,"e":12,"t":["oiseau","terrestre","amérique du nord"]},
        {"n":"Corbeau freux","h":45,"w":0.5,"e":20,"t":["oiseau","commun","europe"]},
        {"n":"Pie bavarde","h":45,"w":0.2,"e":15,"t":["oiseau","commun","europe"]},
        {"n":"Geai des chênes","h":35,"w":0.15,"e":15,"t":["oiseau","commun","europe"]},
        {"n":"Rossignol philomèle","h":16,"w":0.02,"e":8,"t":["oiseau","commun","europe"]},
        {"n":"Rouge-gorge familier","h":14,"w":0.018,"e":13,"t":["oiseau","commun","europe"]},
        {"n":"Mésange bleue","h":12,"w":0.01,"e":12,"t":["oiseau","commun","europe"]},
        {"n":"Hirondelle de cheminée","h":18,"w":0.02,"e":15,"t":["oiseau","commun","europe","migration"]},
        {"n":"Moineau domestique","h":15,"w":0.03,"e":13,"t":["oiseau","commun","europe"]},

        # REPTILES - CROCS ET TORTUES (13)
        {"n":"Crocodile du Nil","h":500,"w":500,"e":70,"t":["reptile","crocodilien","afrique","rivière"]},
        {"n":"Alligator d'Amérique","h":400,"w":360,"e":50,"t":["reptile","crocodilien","amérique du nord"]},
        {"n":"Caïman noir","h":450,"w":400,"e":60,"t":["reptile","crocodilien","amérique du sud"]},
        {"n":"Gavial du Gange","h":500,"w":250,"e":50,"t":["reptile","crocodilien","asie","pays:inde"]},
        {"n":"Crocodile marin","h":600,"w":1000,"e":70,"t":["reptile","crocodilien","océanie","pays:australie"]},
        {"n":"Tortue luth","h":200,"w":600,"e":50,"t":["reptile","tortue","océan","marin"]},
        {"n":"Tortue verte","h":120,"w":150,"e":80,"t":["reptile","tortue","océan","marin"]},
        {"n":"Tortue imbriquée","h":90,"w":80,"e":50,"t":["reptile","tortue","océan","marin"]},
        {"n":"Tortue alligator","h":75,"w":80,"e":50,"t":["reptile","tortue","amérique du nord","rivière"]},
        {"n":"Tortue géante des Galápagos","h":150,"w":250,"e":150,"t":["reptile","tortue","amérique du sud","pays:équateur"]},
        {"n":"Tortue d'Hermann","h":20,"w":1,"e":80,"t":["reptile","tortue","europe","forêt"]},
        {"n":"Cistude d'Europe","h":15,"w":0.8,"e":60,"t":["reptile","tortue","europe","marais"]},
        {"n":"Tortue boîte","h":15,"w":0.5,"e":50,"t":["reptile","tortue","amérique du nord"]},

        # REPTILES - SERPENTS (15)
        {"n":"Cobra royal","h":550,"w":6,"e":20,"t":["reptile","serpent","asie","venimeux"]},
        {"n":"Mamba noir","h":300,"w":1.5,"e":12,"t":["reptile","serpent","afrique","savane","venimeux"]},
        {"n":"Taïpan du désert","h":200,"w":2,"e":15,"t":["reptile","serpent","océanie","pays:australie","venimeux"]},
        {"n":"Serpent à sonnette","h":150,"w":2,"e":15,"t":["reptile","serpent","amérique","désert","venimeux"]},
        {"n":"Vipère aspic","h":70,"w":0.4,"e":15,"t":["reptile","serpent","europe","venimeux"]},
        {"n":"Couleuvre à collier","h":100,"w":0.3,"e":15,"t":["reptile","serpent","europe","étang"]},
        {"n":"Anaconda vert","h":600,"w":100,"e":10,"t":["reptile","serpent","amérique du sud","marais"]},
        {"n":"Python réticulé","h":700,"w":120,"e":25,"t":["reptile","serpent","asie","forêt"]},
        {"n":"Boa constrictor","h":350,"w":30,"e":25,"t":["reptile","serpent","amérique","forêt"]},
        {"n":"Serpent corail","h":80,"w":0.2,"e":10,"t":["reptile","serpent","amérique","venimeux"]},
        {"n":"Bongare rayé","h":150,"w":1,"e":15,"t":["reptile","serpent","asie","venimeux"]},
        {"n":"Serpent tigre","h":150,"w":1.5,"e":15,"t":["reptile","serpent","océanie","pays:australie","venimeux"]},
        {"n":"Python royal","h":120,"w":2,"e":20,"t":["reptile","serpent","afrique","savane"]},
        {"n":"Boomslang","h":150,"w":0.5,"e":15,"t":["reptile","serpent","afrique","forêt","venimeux"]},
        {"n":"Serpent marin annelé","h":120,"w":1,"e":15,"t":["reptile","serpent","océan","venimeux"]},

        # LEZARDS ET AMPHIBIENS (12)
        {"n":"Dragon de Komodo","h":300,"w":70,"e":30,"t":["reptile","lézard","asie","pays:indonésie"]},
        {"n":"Varan du Nil","h":200,"w":15,"e":15,"t":["reptile","lézard","afrique","rivière"]},
        {"n":"Iguane marin des Galápagos","h":120,"w":10,"e":12,"t":["reptile","lézard","amérique du sud","marin"]},
        {"n":"Iguane vert","h":150,"w":4,"e":20,"t":["reptile","lézard","amérique centrale","forêt"]},
        {"n":"Caméléon de Jackson","h":30,"w":0.2,"e":8,"t":["reptile","lézard","afrique","forêt"]},
        {"n":"Gecko léopard","h":25,"w":0.06,"e":15,"t":["reptile","lézard","asie","désert"]},
        {"n":"Scinque à langue bleue","h":45,"w":0.5,"e":20,"t":["reptile","lézard","océanie","pays:australie"]},
        {"n":"Grenouille rousse","h":8,"w":0.03,"e":8,"t":["amphibien","grenouille","europe","étang"]},
        {"n":"Crapaud commun","h":10,"w":0.08,"e":10,"t":["amphibien","crapaud","europe","jardin"]},
        {"n":"Salamandre tachetée","h":20,"w":0.04,"e":20,"t":["amphibien","salamandre","europe","forêt"]},
        {"n":"Triton palmé","h":8,"w":0.01,"e":10,"t":["amphibien","triton","europe","étang"]},
        {"n":"Axolotl","h":25,"w":0.1,"e":12,"t":["amphibien","asie","aquatique","pays:mexique"]},

        # POISSONS (20)
        {"n":"Grand requin blanc","h":450,"w":1100,"e":70,"t":["poisson","requin","océan","carnivore"]},
        {"n":"Requin baleine","h":1200,"w":19000,"e":70,"t":["poisson","requin","océan","herbivore"]},
        {"n":"Requin marteau","h":400,"w":250,"e":30,"t":["poisson","requin","océan"]},
        {"n":"Requin bouledogue","h":250,"w":130,"e":15,"t":["poisson","requin","océan","rivière"]},
        {"n":"Raie manta","h":700,"w":1300,"e":20,"t":["poisson","raie","océan"]},
        {"n":"Raie pastenague","h":100,"w":35,"e":15,"t":["poisson","raie","océan"]},
        {"n":"Requin scie","h":500,"w":300,"e":30,"t":["poisson","requin","océan"]},
        {"n":"Thon rouge","h":250,"w":400,"e":40,"t":["poisson","marin","océan"]},
        {"n":"Espadon","h":300,"w":400,"e":15,"t":["poisson","marin","océan"]},
        {"n":"Marlin bleu","h":400,"w":600,"e":20,"t":["poisson","marin","océan"]},
        {"n":"Saumon de l'Atlantique","h":100,"w":15,"e":10,"t":["poisson","rivière","océan","migration"]},
        {"n":"Truite fario","h":50,"w":2,"e":10,"t":["poisson","rivière","europe"]},
        {"n":"Brochet","h":100,"w":10,"e":15,"t":["poisson","rivière","europe"]},
        {"n":"Carpe commune","h":80,"w":15,"e":20,"t":["poisson","rivière","europe"]},
        {"n":"Poisson-clown","h":10,"w":0.1,"e":10,"t":["poisson","marin","récif"]},
        {"n":"Chirurgien bleu","h":25,"w":0.3,"e":15,"t":["poisson","marin","récif"]},
        {"n":"Murène commune","h":150,"w":10,"e":15,"t":["poisson","marin","récif"]},
        {"n":"Hippocampe (Cheval de mer)","h":15,"w":0.05,"e":5,"t":["poisson","marin","océan"]},
        {"n":"Poisson-lune (Mola mola)","h":300,"w":1000,"e":20,"t":["poisson","marin","océan"]},
        {"n":"Piranha rouge","h":30,"w":1,"e":10,"t":["poisson","rivière","amérique du sud"]},

        # INVERTEBRES (15)
        {"n":"Poulpe commun","h":90,"w":10,"e":3,"t":["invertébré","mollusque","marin","océan"]},
        {"n":"Calmar géant","h":1300,"w":275,"e":5,"t":["invertébré","mollusque","marin","océan"]},
        {"n":"Méduse boîte","h":30,"w":2,"e":1,"t":["invertébré","cnidaire","marin","venimeux"]},
        {"n":"Homard européen","h":50,"w":5,"e":50,"t":["invertébré","crustacé","marin"]},
        {"n":"Abeille domestique","h":1.2,"w":0.0001,"e":0.5,"t":["invertébré","insecte","mondial"]},
        {"n":"Fourmi coupeuse de feuilles","h":1,"w":0.0001,"e":2,"t":["invertébré","insecte","amérique"]},
        {"n":"Papillon Monarque","h":10,"w":0.0005,"e":0.5,"t":["invertébré","insecte","amérique","migration"]},
        {"n":"Mante religieuse","h":8,"w":0.01,"e":1,"t":["invertébré","insecte","europe"]},
        {"n":"Mygale à genoux rouges","h":15,"w":0.1,"e":30,"t":["invertébré","arachnide","amérique centrale"]},
        {"n":"Scorpion empereur","h":20,"w":0.05,"e":8,"t":["invertébré","arachnide","afrique"]},
        {"n":"Étoile de mer","h":20,"w":1,"e":10,"t":["invertébré","échinoderme","marin"]},
        {"n":"Crabe dormeur","h":25,"w":3,"e":10,"t":["invertébré","crustacé","marin"]},
        {"n":"Limace léopard","h":15,"w":0.03,"e":3,"t":["invertébré","mollusque","europe"]},
        {"n":"Coccinelle à sept points","h":0.8,"w":0.0001,"e":1,"t":["invertébré","insecte","europe"]},
        {"n":"Libellule déprimée","h":8,"w":0.001,"e":2,"t":["invertébré","insecte","europe"]}
    ]

    count = 0
    for d in data:
        # Create or Get tags
        db_tags = [animal_tag]
        for t_name in d["t"]:
            tag = db.query(models.Tag).filter(models.Tag.name == t_name).first()
            if not tag:
                tag = models.Tag(name=t_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            db_tags.append(tag)
            
        card = models.Card(
            name=d["n"],
            image_url=None,
            wiki_link=f"https://fr.wikipedia.org/wiki/{d['n'].replace(' ', '_')}",
            attributes={
                "taille_cm": d["h"],
                "poids_kg": d["w"],
                "esperance_vie": d["e"]
            },
            tags=db_tags
        )
        db.add(card)
        count += 1
        if count % 50 == 0:
            db.commit()
            print(f"Importation: {count} animaux...")

    db.commit()
    db.close()
    print(f"Bdd mise à jour avec {count} nouveaux animaux!")

if __name__ == "__main__":
    import_animals()
