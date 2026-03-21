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

def format_card(name, year, word_count, tags):
    return {
        "name": name,
        "image_url": f"https://source.unsplash.com/featured/?book,{name.replace(' ', '+')}",
        "wiki_link": f"https://fr.wikipedia.org/wiki/{name.replace(' ', '_')}",
        "attributes": {
            "année": year,
            "nombre_de_mots": word_count
        },
        "tag_names": tags + ["Littérature", "Classique"]
    }

books = [
    ("Don Quichotte", 1605, 345000, ["Roman", "Aventure"]),
    ("Les Misérables", 1862, 530000, ["Roman", "Drame", "France"]),
    ("Guerre et Paix", 1869, 587000, ["Roman", "Historique", "Russie"]),
    ("Ulysse", 1922, 265000, ["Roman", "Modernisme"]),
    ("Infinite Jest", 1996, 543000, ["Roman", "Postmodernisme"]),
    ("Gatsby le Magnifique", 1925, 47000, ["Roman", "Jazz Age"]),
    ("Le Vieil Homme et la Mer", 1952, 27000, ["Roman", "Aventure"]),
    ("La Ferme des animaux", 1945, 30000, ["Roman", "Allégorie"]),
    ("Le Petit Prince", 1943, 16000, ["Conte", "Philosophie", "France"]),
    ("Madame Bovary", 1857, 118000, ["Roman", "Réalisme", "France"]),
    ("Germinal", 1885, 150000, ["Roman", "Naturalisme", "France"]),
    ("Bel-Ami", 1885, 90000, ["Roman", "Réalisme", "France"]),
    ("L'Étranger", 1942, 36000, ["Roman", "Existentialisme", "France"]),
    ("Orgueil et Préjugés", 1813, 120000, ["Roman", "Social", "Angleterre"]),
    ("Raison et Sentiments", 1811, 126000, ["Roman", "Social", "Angleterre"]),
    ("Jane Eyre", 1847, 183000, ["Roman", "Gothique", "Angleterre"]),
    ("Les Hauts de Hurlevent", 1847, 107000, ["Roman", "Gothique", "Angleterre"]),
    ("Moby-Dick", 1851, 206000, ["Roman", "Aventure", "Mer"]),
    ("Dracula", 1897, 160000, ["Roman", "Horreur", "Gothique"]),
    ("Frankenstein", 1818, 75000, ["Roman", "Horreur", "Science-fiction"]),
    ("Le Portrait de Dorian Gray", 1890, 78000, ["Roman", "Philosophie"]),
    ("Anna Karénine", 1877, 350000, ["Roman", "Drame", "Russie"]),
    ("Crime et Châtiment", 1866, 211000, ["Roman", "Psychologique", "Russie"]),
    ("Les Frères Karamazov", 1880, 364000, ["Roman", "Philosophie", "Russie"]),
    ("Le Comte de Monte-Cristo", 1844, 463000, ["Roman", "Aventure", "France"]),
    ("Les Trois Mousquetaires", 1844, 227000, ["Roman", "Aventure", "France"]),
    ("Notre-Dame de Paris", 1831, 185000, ["Roman", "Historique", "France"]),
    ("Gargantua", 1534, 50000, ["Roman", "Satire", "France"]),
    ("Candide", 1759, 30000, ["Conte", "Satire", "France"]),
    ("1984", 1949, 88000, ["Roman", "Dystopie"]),
    ("Le Meilleur des mondes", 1932, 64000, ["Roman", "Dystopie"]),
    ("Fahrenheit 451", 1953, 46000, ["Roman", "Dystopie"]),
    ("L'Attrape-cœurs", 1951, 73000, ["Roman", "Jeunesse"]),
    ("Ne tirez pas sur l'oiseau moqueur", 1960, 100000, ["Roman", "Social"]),
    ("Le Hobbit", 1937, 95000, ["Roman", "Fantasy"]),
    ("Le Seigneur des Anneaux", 1954, 481000, ["Roman", "Fantasy"]),
    ("Harry Potter à l'école des sorciers", 1997, 77000, ["Roman", "Jeunesse", "Fantasy"]),
    ("Harry Potter et les Reliques de la Mort", 2007, 198000, ["Roman", "Jeunesse", "Fantasy"]),
    ("De grandes espérances", 1861, 183000, ["Roman", "Social", "Angleterre"]),
    ("Oliver Twist", 1837, 155000, ["Roman", "Social", "Angleterre"]),
    ("Un conte de deux villes", 1859, 135000, ["Roman", "Historique"]),
    ("David Copperfield", 1850, 358000, ["Roman", "Social"]),
    ("La Maison d'Aspre-Vent", 1853, 355000, ["Roman", "Incomplet"]),
    ("Les Temps difficiles", 1854, 104000, ["Roman", "Social"]),
    ("Tess d'Urberville", 1891, 150000, ["Roman", "Drame"]),
    ("Les Raisins de la colère", 1939, 169000, ["Roman", "Social"]),
    ("Des souris et des hommes", 1937, 30000, ["Roman", "Drame"]),
    ("À l'est d'Éden", 1952, 225000, ["Roman", "Saga"]),
    ("Sur la route", 1957, 115000, ["Roman", "Beat Generation"]),
    ("Catch 22", 1961, 174000, ["Roman", "Satire"]),
    ("Abattoir 5", 1969, 49000, ["Roman", "Science-fiction"]),
    ("Lolita", 1955, 112000, ["Roman", "Drame"]),
    ("Feu pâle", 1962, 70000, ["Roman", "Postmodernisme"]),
    ("Méridien de sang", 1985, 100000, ["Roman", "Western"]),
    ("La Route", 2006, 58000, ["Roman", "Post-apocalyptique"]),
    ("Beloved", 1987, 80000, ["Roman", "Historique"]),
    ("Cent ans de solitude", 1967, 144000, ["Roman", "Réalisme magique"]),
    ("L'Amour aux temps du choléra", 1985, 120000, ["Roman", "Romance"]),
    ("À la recherche du temps perdu", 1913, 1267000, ["Roman", "Saga", "France"]),
    ("Du côté de chez Swann", 1913, 215000, ["Roman", "France"]),
    ("Middlemarch", 1871, 316000, ["Roman", "Saga"]),
    ("L'Odyssée", -800, 110000, ["Épopée", "Mythologie", "Grèce"]),
    ("L'Iliade", -800, 135000, ["Épopée", "Mythologie", "Grèce"]),
    ("Le Paradis perdu", 1667, 80000, ["Poésie", "Religion"]),
    ("La Divine Comédie", 1320, 100000, ["Poésie", "Religion", "Italie"]),
    ("Les Contes de Cantorbéry", 1387, 165000, ["Nouvelles", "Moyen-Âge"]),
    ("Les Voyages de Gulliver", 1726, 107000, ["Roman", "Satire"]),
    ("Robinson Crusoé", 1719, 120000, ["Roman", "Aventure"]),
    ("Le Soleil se lève aussi", 1926, 67000, ["Roman", "Lost Generation"]),
    ("Pour qui sonne le glas", 1940, 175000, ["Roman", "Guerre"]),
    ("L'Adieu aux armes", 1929, 90000, ["Roman", "Guerre"]),
    ("Gens de Dublin", 1914, 67000, ["Nouvelles", "Irlande"]),
    ("Portrait de l'artiste en jeune homme", 1916, 85000, ["Roman", "Semi-autobiographique"]),
    ("La Promenade au phare", 1927, 70000, ["Roman", "Modernisme"]),
    ("Mrs Dalloway", 1925, 45000, ["Roman", "Modernisme"]),
    ("Voyage au centre de la Terre", 1864, 85000, ["Roman", "Aventure", "France"]),
    ("Vingt mille lieues sous les mers", 1870, 130000, ["Roman", "Aventure", "France"]),
    ("Le Tour du monde en quatre-vingts jours", 1873, 65000, ["Roman", "Aventure", "France"]),
    ("Manon Lescaut", 1731, 55000, ["Roman", "France"]),
    ("Le Père Goriot", 1835, 95000, ["Roman", "Réalisme", "France"]),
    ("Illusions perdues", 1837, 230000, ["Roman", "Réalisme", "France"]),
    ("La Princesse de Clèves", 1678, 45000, ["Roman", "Psychologique", "France"])
]

formatted_cards = [format_card(b[0], b[1], b[2], b[3]) for b in books]
import_cards(formatted_cards)
print(f"Total des livres importés : {len(formatted_cards)}")
