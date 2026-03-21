import requests
import json

BASE_URL = "http://localhost:8000"

def import_cards(cards):
    url = f"{BASE_URL}/cards/bulk"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(cards), headers=headers)
    if response.status_code == 200:
        print(f"Bilan : {response.json()['message']}")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def format_card(name, year, rating, box_office=None, tags=[]):
    attrs = {"année": year, "note_imdb": rating}
    if box_office:
        attrs["box_office_mondial"] = box_office
    
    return {
        "name": name,
        "image_url": f"https://source.unsplash.com/featured/?scifi,movie,{name.replace(' ', '+')}",
        "wiki_link": f"https://fr.wikipedia.org/wiki/{name.replace(' ', '_')}",
        "attributes": attrs,
        "tag_names": list(set(tags + ["Science-Fiction", "Cinéma"]))
    }

scifi_movies = [
    ("Metropolis", 1927, 8.3, 1, ["Classique", "Noir et Blanc"]),
    ("Le Jour où la Terre s'arrêta", 1951, 7.7, 1, ["Classique", "Extraterrestre"]),
    ("La Guerre des mondes", 1953, 7.1, 2, ["Classique", "Invasion"]),
    ("Planète interdite", 1956, 7.5, 3, ["Classique", "Espace"]),
    ("2001, l'Odyssée de l'espace", 1968, 8.3, 190, ["Espace", "Chef-d'œuvre"]),
    ("La Planète des singes", 1968, 8.0, 33, ["Dystopie", "Classique"]),
    ("Orange mécanique", 1971, 8.3, 26, ["Dystopie", "Culte"]),
    ("Soleil vert", 1973, 7.0, 1, ["Dystopie", "Écologie"]),
    ("Star Wars : Un nouvel espoir", 1977, 8.6, 775, ["Espace", "Saga"]),
    ("Rencontres du troisième type", 1977, 7.6, 303, ["Extraterrestre"]),
    ("Alien, le huitième passager", 1979, 8.5, 106, ["Horreur", "Espace"]),
    ("Stalker", 1979, 8.1, 1, ["Philosophique", "URSS"]),
    ("Star Wars : L'Empire contre-attaque", 1980, 8.7, 538, ["Espace", "Saga"]),
    ("New York 1997", 1981, 7.1, 25, ["Action", "Dystopie"]),
    ("Blade Runner", 1982, 8.1, 41, ["Cyberpunk", "Culte"]),
    ("E.T., l'extra-terrestre", 1982, 7.9, 792, ["Famille", "Extraterrestre"]),
    ("The Thing", 1982, 8.2, 19, ["Horreur", "Extraterrestre"]),
    ("Tron", 1982, 6.7, 33, ["Informatique", "Culte"]),
    ("Star Wars : Le Retour du Jedi", 1983, 8.3, 475, ["Espace", "Saga"]),
    ("Dune (Lynch)", 1984, 6.3, 30, ["Espace", "Saga"]),
    ("Terminator", 1984, 8.1, 78, ["Action", "IA"]),
    ("Brazil", 1985, 7.9, 16, ["Dystopie", "Surréaliste"]),
    ("Retour vers le futur", 1985, 8.5, 381, ["Voyage temporel", "Culte"]),
    ("Aliens, le retour", 1886, 8.4, 131, ["Action", "Espace"]),
    ("Robocop", 1987, 7.6, 53, ["Action", "Cyberpunk"]),
    ("Predator", 1987, 7.8, 98, ["Action", "Extraterrestre"]),
    ("Akira", 1988, 8.0, 49, ["Animation", "Cyberpunk"]),
    ("Abyss", 1989, 7.5, 90, ["Aventure", "Sous-marin"]),
    ("Total Recall", 1990, 7.5, 261, ["Action", "Mars"]),
    ("Terminator 2 : Le Jugement dernier", 1991, 8.6, 520, ["Action", "IA"]),
    ("Jurassic Park", 1993, 8.2, 1033, ["Aventure", "Dinosaures"]),
    ("Ghost in the Shell", 1995, 7.9, 2, ["Animation", "Cyberpunk"]),
    ("L'Armée des douze singes", 1995, 8.0, 168, ["Voyage temporel"]),
    ("Mars Attacks!", 1996, 6.4, 101, ["Comédie", "Invasion"]),
    ("Bienvenue à Gattaca", 1997, 7.8, 12, ["Dystopie", "Biologie"]),
    ("Le Cinquième Élément", 1997, 7.6, 263, ["Aventure", "Espace"]),
    ("Men in Black", 1997, 7.3, 589, ["Comédie", "Extraterrestre"]),
    ("Starship Troopers", 1997, 7.3, 121, ["Action", "Guerre"]),
    ("Dark City", 1998, 7.6, 27, ["Culte", "Mystère"]),
    ("The Truman Show", 1998, 8.2, 264, ["Drama", "Dystopie"]),
    ("Matrix", 1999, 8.7, 463, ["Action", "Cyberpunk"]),
    ("Minority Report", 2002, 7.7, 358, ["Action", "IA"]),
    ("Eternal Sunshine of the Spotless Mind", 2004, 8.3, 74, ["Romance", "Mémoire"]),
    ("Serenity", 2005, 7.8, 40, ["Espace", "Western"]),
    ("Children of Men", 2006, 7.9, 70, ["Dystopie", "Drame"]),
    ("Sunshine", 2007, 7.2, 34, ["Espace", "Soleil"]),
    ("WALL-E", 2008, 8.4, 533, ["Animation", "Robot"]),
    ("District 9", 2009, 7.9, 210, ["Social", "Extraterrestre"]),
    ("Avatar", 2009, 7.9, 2923, ["Espace", "Épopée"]),
    ("Moon", 2009, 7.8, 9, ["Espace", "Psychologique"]),
    ("Inception", 2010, 8.8, 836, ["Action", "Rêve"]),
    ("Looper", 2012, 7.4, 176, ["Action", "Voyage temporel"]),
    ("Gravity", 2013, 7.7, 723, ["Espace", "Survie"]),
    ("Her", 2013, 8.0, 48, ["IA", "Romance"]),
    ("Interstellar", 2014, 8.7, 701, ["Espace", "Physique"]),
    ("Ex Machina", 2014, 7.7, 36, ["IA", "Thriller"]),
    ("Mad Max: Fury Road", 2015, 8.1, 380, ["Dystopie", "Action"]),
    ("Seul sur Mars", 2015, 8.0, 630, ["Espace", "Survie"]),
    ("Premier Contact", 2016, 7.9, 203, ["Extraterrestre", "Langage"]),
    ("Blade Runner 2049", 2017, 8.0, 259, ["Cyberpunk", "Saga"]),
    ("Everything Everywhere All at Once", 2022, 7.8, 143, ["Multivers", "Action"]),
    ("Dune : Deuxième partie", 2024, 8.6, 711, ["Espace", "Saga"])
]

formatted_cards = [format_card(*m) for m in scifi_movies]
import_cards(formatted_cards)
