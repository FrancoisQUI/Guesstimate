import requests
import json

BASE_URL = "http://localhost:8000"

def import_cards(cards):
    url = f"{BASE_URL}/cards/bulk"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(cards), headers=headers)
    if response.status_code == 200:
        print(f"Succès: {response.json()['message']}")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

mcu_movies = [
    {"name": "Iron Man", "year": 2008, "box_office": 585, "budget": 140, "note": 7.9},
    {"name": "L'Incroyable Hulk", "year": 2008, "box_office": 264, "budget": 150, "note": 6.6},
    {"name": "Iron Man 2", "year": 2010, "box_office": 623, "budget": 200, "note": 6.9},
    {"name": "Thor", "year": 2011, "box_office": 449, "budget": 150, "note": 7.0},
    {"name": "Captain America: First Avenger", "year": 2011, "box_office": 370, "budget": 140, "note": 6.9},
    {"name": "The Avengers", "year": 2012, "box_office": 1518, "budget": 220, "note": 8.0},
    {"name": "Iron Man 3", "year": 2013, "box_office": 1214, "budget": 200, "note": 7.1},
    {"name": "Thor: Le Monde des ténèbres", "year": 2013, "box_office": 644, "budget": 170, "note": 6.8},
    {"name": "Captain America: Le Soldat de l'hiver", "year": 2014, "box_office": 714, "budget": 170, "note": 7.7},
    {"name": "Les Gardiens de la Galaxie", "year": 2014, "box_office": 773, "budget": 170, "note": 8.0},
    {"name": "Avengers: L'Ère d'Ultron", "year": 2015, "box_office": 1405, "budget": 250, "note": 7.3},
    {"name": "Ant-Man", "year": 2015, "box_office": 519, "budget": 130, "note": 7.3},
    {"name": "Captain America: Civil War", "year": 2016, "box_office": 1153, "budget": 250, "note": 7.8},
    {"name": "Doctor Strange", "year": 2016, "box_office": 677, "budget": 165, "note": 7.5},
    {"name": "Les Gardiens de la Galaxie Vol. 2", "year": 2017, "box_office": 863, "budget": 200, "note": 7.6},
    {"name": "Spider-Man: Homecoming", "year": 2017, "box_office": 880, "budget": 175, "note": 7.4},
    {"name": "Thor: Ragnarok", "year": 2017, "box_office": 854, "budget": 180, "note": 7.9},
    {"name": "Black Panther", "year": 2018, "box_office": 1347, "budget": 200, "note": 7.3},
    {"name": "Avengers: Infinity War", "year": 2018, "box_office": 2048, "budget": 316, "note": 8.4},
    {"name": "Ant-Man et la Guêpe", "year": 2018, "box_office": 622, "budget": 162, "note": 7.0},
    {"name": "Captain Marvel", "year": 2019, "box_office": 1128, "budget": 152, "note": 6.8},
    {"name": "Avengers: Endgame", "year": 2019, "box_office": 2797, "budget": 356, "note": 8.4},
    {"name": "Spider-Man: Far From Home", "year": 2019, "box_office": 1131, "budget": 160, "note": 7.4},
    {"name": "Black Widow", "year": 2021, "box_office": 379, "budget": 200, "note": 6.7},
    {"name": "Shang-Chi et la Légende des Dix Anneaux", "year": 2021, "box_office": 432, "budget": 150, "note": 7.4},
    {"name": "Les Éternels", "year": 2021, "box_office": 402, "budget": 200, "note": 6.3},
    {"name": "Spider-Man: No Way Home", "year": 2021, "box_office": 1912, "budget": 200, "note": 8.2},
    {"name": "Doctor Strange in the Multiverse of Madness", "year": 2022, "box_office": 955, "budget": 200, "note": 6.9},
    {"name": "Thor: Love and Thunder", "year": 2022, "box_office": 760, "budget": 250, "note": 6.2},
    {"name": "Black Panther: Wakanda Forever", "year": 2022, "box_office": 859, "budget": 250, "note": 6.7},
    {"name": "Ant-Man et la Guêpe: Quantumania", "year": 2023, "box_office": 476, "budget": 200, "note": 6.1},
    {"name": "Les Gardiens de la Galaxie Vol. 3", "year": 2023, "box_office": 845, "budget": 250, "note": 7.9},
    {"name": "The Marvels", "year": 2023, "box_office": 206, "budget": 274, "note": 5.6}
]

pixar_movies = [
    {"name": "Toy Story", "year": 1995, "box_office": 373, "budget": 30, "note": 8.3},
    {"name": "1001 Pattes", "year": 1998, "box_office": 363, "budget": 60, "note": 7.2},
    {"name": "Toy Story 2", "year": 1999, "box_office": 497, "budget": 90, "note": 7.9},
    {"name": "Monstres & Cie", "year": 2001, "box_office": 577, "budget": 115, "note": 8.1},
    {"name": "Le Monde de Nemo", "year": 2003, "box_office": 940, "budget": 94, "note": 8.2},
    {"name": "Les Indestructibles", "year": 2004, "box_office": 633, "budget": 92, "note": 8.0},
    {"name": "Cars", "year": 2006, "box_office": 462, "budget": 120, "note": 7.2},
    {"name": "Ratatouille", "year": 2007, "box_office": 623, "budget": 150, "note": 8.1},
    {"name": "WALL-E", "year": 2008, "box_office": 533, "budget": 180, "note": 8.4},
    {"name": "Là-haut", "year": 2009, "box_office": 735, "budget": 175, "note": 8.3},
    {"name": "Toy Story 3", "year": 2010, "box_office": 1067, "budget": 200, "note": 8.3},
    {"name": "Rebelle", "year": 2012, "box_office": 540, "budget": 185, "note": 7.1},
    {"name": "Monstres Academy", "year": 2013, "box_office": 744, "budget": 200, "note": 7.2},
    {"name": "Vice-versa", "year": 2015, "box_office": 858, "budget": 175, "note": 8.1},
    {"name": "Le Voyage d'Arlo", "year": 2015, "box_office": 332, "budget": 175, "note": 6.7},
    {"name": "Le Monde de Dory", "year": 2016, "box_office": 1028, "budget": 200, "note": 7.3},
    {"name": "Cars 3", "year": 2017, "box_office": 383, "budget": 175, "note": 6.7},
    {"name": "Coco", "year": 2017, "box_office": 807, "budget": 175, "note": 8.4},
    {"name": "Les Indestructibles 2", "year": 2018, "box_office": 1242, "budget": 200, "note": 7.6},
    {"name": "Toy Story 4", "year": 2019, "box_office": 1073, "budget": 200, "note": 7.7},
    {"name": "En avant", "year": 2020, "box_office": 141, "budget": 175, "note": 7.4},
    {"name": "Soul", "year": 2020, "box_office": 121, "budget": 150, "note": 8.0},
    {"name": "Luca", "year": 2021, "box_office": 49, "budget": 150, "note": 7.4},
    {"name": "Alerte rouge", "year": 2022, "box_office": 20, "budget": 175, "note": 7.0},
    {"name": "Buzz l'Éclair", "year": 2022, "box_office": 226, "budget": 200, "note": 6.1},
    {"name": "Élémentaire", "year": 2023, "box_office": 496, "budget": 200, "note": 7.0}
]

ghibli_movies = [
    {"name": "Le Château dans le ciel", "year": 1986, "box_office": 16, "note": 8.0},
    {"name": "Le Tombeau des lucioles", "year": 1988, "box_office": 15, "note": 8.5},
    {"name": "Mon voisin Totoro", "year": 1988, "box_office": 30, "note": 8.1},
    {"name": "Kiki la petite sorcière", "year": 1989, "box_office": 18, "note": 7.8},
    {"name": "Souvenirs goutte à goutte", "year": 1991, "box_office": 15, "note": 7.6},
    {"name": "Porco Rosso", "year": 1992, "box_office": 34, "note": 7.7},
    {"name": "Pompoko", "year": 1994, "box_office": 27, "note": 7.3},
    {"name": "Si tu tends l'oreille", "year": 1995, "box_office": 23, "note": 7.9},
    {"name": "Princesse Mononoké", "year": 1997, "box_office": 169, "note": 8.4},
    {"name": "Le Voyage de Chihiro", "year": 2001, "box_office": 355, "note": 8.6},
    {"name": "Le Royaume des chats", "year": 2002, "box_office": 65, "note": 7.1},
    {"name": "Le Château ambulant", "year": 2004, "box_office": 236, "note": 8.2},
    {"name": "Les Contes de Terremer", "year": 2006, "box_office": 68, "note": 6.3},
    {"name": "Ponyo sur la falaise", "year": 2008, "box_office": 204, "note": 7.6},
    {"name": "Arrietty : Le Petit Monde des Chapardeurs", "year": 2010, "box_office": 145, "note": 7.6},
    {"name": "La Colline aux coquelicots", "year": 2011, "box_office": 61, "note": 7.4},
    {"name": "Le Vent se lève", "year": 2013, "box_office": 136, "note": 7.7},
    {"name": "Le Conte de la princesse Kaguya", "year": 2013, "box_office": 27, "note": 8.0},
    {"name": "Souvenirs de Marnie", "year": 2014, "box_office": 35, "note": 7.7},
    {"name": "Le Garçon et le Héron", "year": 2023, "box_office": 167, "note": 7.6}
]

disney_movies = [
    {"name": "Blanche-Neige et les Sept Nains", "year": 1937, "box_office": 418, "note": 7.6},
    {"name": "Pinocchio", "year": 1940, "box_office": 164, "note": 7.5},
    {"name": "Fantasia", "year": 1940, "box_office": 83, "note": 7.7},
    {"name": "Dumbo", "year": 1941, "box_office": 1, "note": 7.2},
    {"name": "Bambi", "year": 1942, "box_office": 267, "note": 7.3},
    {"name": "Cendrillon", "year": 1950, "box_office": 263, "note": 7.3},
    {"name": "Alice au pays des merveilles", "year": 1951, "box_office": 2, "note": 7.3},
    {"name": "Peter Pan", "year": 1953, "box_office": 87, "note": 7.3},
    {"name": "La Belle et le Clochard", "year": 1955, "box_office": 93, "note": 7.3},
    {"name": "La Belle au bois dormant", "year": 1959, "box_office": 51, "note": 7.2},
    {"name": "Les 101 Dalmatiens", "year": 1961, "box_office": 215, "note": 7.3},
    {"name": "Merlin l'Enchanteur", "year": 1963, "box_office": 22, "note": 7.1},
    {"name": "Le Livre de la jungle", "year": 1967, "box_office": 205, "note": 7.6},
    {"name": "Les Aristochats", "year": 1970, "box_office": 191, "note": 7.1},
    {"name": "Robin des Bois", "year": 1973, "box_office": 32, "note": 7.5},
    {"name": "Les Aventures de Bernard et Bianca", "year": 1977, "box_office": 169, "note": 6.9},
    {"name": "Rox et Rouky", "year": 1981, "box_office": 63, "note": 7.2},
    {"name": "La Petite Sirène", "year": 1989, "box_office": 211, "note": 7.5},
    {"name": "La Belle et la Bête", "year": 1991, "box_office": 424, "note": 8.0},
    {"name": "Aladdin", "year": 1992, "box_office": 504, "note": 8.0},
    {"name": "Le Roi Lion", "year": 1994, "box_office": 968, "note": 8.5},
    {"name": "Pocahontas", "year": 1995, "box_office": 346, "note": 6.7},
    {"name": "Le Bossu de Notre-Dame", "year": 1996, "box_office": 325, "note": 7.0},
    {"name": "Mulan", "year": 1998, "box_office": 304, "note": 7.6},
    {"name": "Tarzan", "year": 1999, "box_office": 448, "note": 7.3},
    {"name": "Lilo & Stitch", "year": 2002, "box_office": 273, "note": 7.3},
    {"name": "Raiponce", "year": 2010, "box_office": 592, "note": 7.7},
    {"name": "La Reine des neiges", "year": 2013, "box_office": 1281, "note": 7.4},
    {"name": "Vaiana", "year": 2016, "box_office": 643, "note": 7.6},
    {"name": "Encanto", "year": 2021, "box_office": 256, "note": 7.2}
]

def format_cards(movie_list, theme):
    formatted = []
    for m in movie_list:
        card = {
            "name": m["name"],
            "image_url": f"https://source.unsplash.com/featured/?{m['name'].replace(' ', '+')},animation",
            "wiki_link": f"https://fr.wikipedia.org/wiki/{m['name'].replace(' ', '_')}",
            "attributes": {
                "année": m["year"],
                "box_office_mondial": m.get("box_office", 0),
                "note_imdb": m.get("note", 0)
            },
            "tag_names": [theme, "Cinéma", "Animation"]
        }
        if "budget" in m:
            card["attributes"]["budget"] = m["budget"]
        formatted.append(card)
    return formatted

all_cards = []
all_cards.extend(format_cards(mcu_movies, "MCU"))
all_cards.extend(format_cards(pixar_movies, "Pixar"))
all_cards.extend(format_cards(ghibli_movies, "Ghibli"))
all_cards.extend(format_cards(disney_movies, "Disney"))

import_cards(all_cards)
