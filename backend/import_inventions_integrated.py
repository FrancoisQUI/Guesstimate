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

def format_card(name, year, tags):
    return {
        "name": name,
        "image_url": f"https://source.unsplash.com/featured/?{name.replace(' ', '+')},history",
        "wiki_link": f"https://fr.wikipedia.org/wiki/{name.replace(' ', '_')}",
        "attributes": {"année": year},
        "tag_names": tags
    }

# Theme 1: Sciences & Technologies (~50)
science_tech = [
    ("Boussole", 1100, ["Navigation"]), ("Imprimerie", 1440, ["Communication"]), ("Télescope", 1608, ["Astronomie"]),
    ("Calculatrice de Pascal", 1642, ["Informatique"]), ("Baromètre", 1643, ["Météo"]), ("Thermomètre", 1714, ["Santé"]),
    ("Paratonnerre", 1752, ["Physique"]), ("Machine à vapeur", 1769, ["Industrie"]), ("Pile électrique", 1800, ["Énergie"]),
    ("Télégraphe", 1837, ["Communication"]), ("Code Morse", 1838, ["Communication"]), ("Dynamite", 1867, ["Chimie"]),
    ("Téléphone", 1876, ["Communication"]), ("Phonographe", 1877, ["Musique"]), ("Ampoule électrique", 1879, ["Énergie"]),
    ("Microphone", 1877, ["Communication"]), ("Sismographe", 1880, ["Terre"]), ("Haut-parleur", 1880, ["Musique"]),
    ("Rayons X", 1895, ["Médecine"]), ("Radio", 1895, ["Communication"]), ("Cinéma", 1895, ["Arts"]),
    ("Moteur Diesel", 1897, ["Industrie"]), ("Aspirateur", 1901, ["Maison"]), ("Climatisation", 1902, ["Maison"]),
    ("Compteur Geiger", 1908, ["Nucléaire"]), ("Bakélite", 1907, ["Matériaux"]), ("Acier inoxydable", 1913, ["Matériaux"]),
    ("Radar", 1935, ["Navigation"]), ("Nylon", 1935, ["Matériaux"]), ("Hélicoptère", 1939, ["Aviation"]),
    ("Ordinateur ENIAC", 1945, ["Informatique"]), ("Micro-ondes", 1946, ["Cuisine"]), ("Transistor", 1947, ["Électronique"]),
    ("Holographie", 1947, ["Optique"]), ("Code-barres", 1952, ["Commerce"]), ("Puce électronique", 1958, ["Informatique"]),
    ("Laser", 1960, ["Physique"]), ("Cassette audio", 1962, ["Musique"]), ("Souris d'ordinateur", 1963, ["Informatique"]),
    ("Écran à cristaux liquides (LCD)", 1968, ["Électronique"]), ("Microprocesseur", 1971, ["Informatique"]),
    ("Email", 1971, ["Internet"]), ("Calculatrice de poche", 1971, ["Outils"]), ("Lancement d'Internet (TCP/IP)", 1983, ["Informatique"]),
    ("Windows 1.0", 1985, ["Logiciel"]), ("World Wide Web", 1989, ["Internet"]), ("Linux", 1991, ["Logiciel"]),
    ("Wi-Fi", 1997, ["Réseaux"]), ("Bluetooth", 1994, ["Réseaux"]), ("Google", 1998, ["Internet"]),
    ("Bitcoin", 2009, ["Finance"]), ("IA Générative", 2022, ["IA"])
]

# Theme 2: Transports (~45)
transports = [
    ("Roue", -3500, ["Préhistoire"]), ("Bateau à voiles", -3000, ["Navigation"]), ("Char de guerre", -2000, ["Militaire"]),
    ("Drakkar", 800, ["Navigation"]), ("Caravelle", 1450, ["Exploration"]), ("Sextant", 1730, ["Navigation"]),
    ("Montgolfière", 1783, ["Aviation"]), ("Bateau à vapeur", 1783, ["Navigation"]), ("Parachute", 1783, ["Aviation"]),
    ("Locomotive", 1804, ["Rail"]), ("Vélocipède", 1817, ["Loisirs"]), ("Hélice marine", 1836, ["Navigation"]),
    ("Métro de Londres", 1863, ["Urbain"]), ("Moteur thermique", 1876, ["Moteur"]), ("Vélo à pédales", 1885, ["Loisirs"]),
    ("Automobile (Benz)", 1886, ["Route"]), ("Pneumatique", 1888, ["Route"]), ("Zeppelin", 1900, ["Aviation"]),
    ("Avion (Frères Wright)", 1903, ["Aviation"]), ("Ford T", 1908, ["Route"]), ("Porte-avions", 1918, ["Militaire"]),
    ("Avion à réaction", 1939, ["Aviation"]), ("Hélicoptère (Sikorsky)", 1939, ["Aviation"]), ("Vespa", 1946, ["Urbain"]),
    ("Citroën DS", 1955, ["Route"]), ("Concorde", 1969, ["Aviation"]), ("Boeing 747", 1969, ["Aviation"]),
    ("TGV", 1981, ["Rail"]), ("Navette spatiale", 1981, ["Espace"]), ("Eurotunnel", 1994, ["Rail"]),
    ("Tesla Roadster", 2008, ["Électrique"]), ("SpaceX Falcon 9", 2010, ["Espace"]), ("Hyperloop (concept)", 2013, ["Futur"]),
    ("Drone civil", 2013, ["Aviation"]), ("Vélib (Paris)", 2007, ["Urbain"]), ("Skateboard électrique", 2012, ["Urbain"])
]

# Theme 3: Médecine & Santé (~45)
medecine = [
    ("Hippocrate (Médecine moderne)", -400, ["Histoire"]), ("Lunettes de vue", 1284, ["Optique"]), ("Microscope", 1590, ["Biologie"]),
    ("Circulation du sang (Harvey)", 1628, ["Anatomie"]), ("Vaccin contre la variole", 1796, ["Virus"]), ("Stéthoscope", 1816, ["Diagnostic"]),
    ("Anesthésie (Éther)", 1846, ["Chirurgie"]), ("Pasteurisation", 1862, ["Sciences"]), ("Loi de Mendel (Génétique)", 1865, ["Sciences"]),
    ("Lavage des mains (Semmelweis)", 1847, ["Hygiène"]), ("Thermomètre médical", 1714, ["Outils"]), ("Aspirine", 1899, ["Pharmacie"]),
    ("Groupes sanguins", 1901, ["Biologie"]), ("Premier ECG", 1903, ["Électronique"]), ("Insuline", 1922, ["Hormones"]),
    ("Pénicilline", 1928, ["Antibiotiques"]), ("Poumon d'acier", 1928, ["Urgence"]), ("Sulfamides", 1932, ["Antibiotiques"]),
    ("Cortisone", 1948, ["Hormones"]), ("Structure de l'ADN", 1953, ["Génétique"]), ("Stimulateur cardiaque", 1958, ["Technologie"]),
    ("Pilule contraceptive", 1960, ["Société"]), ("Échographie", 1956, ["Imagerie"]), ("Première greffe de cœur", 1967, ["Chirurgie"]),
    ("Greffe de rein (Premier succès)", 1954, ["Chirurgie"]), ("Laser en ophtalmologie", 1961, ["Optique"]), ("Scanner médical", 1971, ["Imagerie"]),
    ("IRM", 1973, ["Imagerie"]), ("Fécondation in vitro", 1978, ["Sciences"]), ("Virus du SIDA découvert", 1983, ["Virus"]),
    ("Prozac", 1987, ["Psy"]), ("Dolly (Clonage)", 1996, ["Génétique"]), ("Séquençage du génome humain", 2003, ["Génétique"]),
    ("Vaccin ARNm", 2020, ["Virus"]), ("Cœur artificiel total", 2013, ["Technologie"]), ("Chirurgie robotique (Da Vinci)", 2000, ["Technologie"]),
    ("Vaccin contre la rage", 1885, ["Virus"]), ("Hormone de croissance synthétique", 1985, ["Biologie"]), ("Défibrillateur automatique", 1969, ["Urgence"]),
    ("Lentilles de contact souples", 1971, ["Optique"]), ("Prothèse de hanche moderne", 1962, ["Orthopédie"])
]

# Theme 4: Communication & Médias (~45)
communication = [
    ("Papier (Chine)", 105, ["Support"]), ("Imprimerie", 1440, ["Culture"]), ("Alphabet Morse", 1838, ["Réseaux"]),
    ("Photographie", 1839, ["Arts"]), ("Télégraphe", 1837, ["Réseaux"]), ("Téléphone", 1876, ["Mobiles"]),
    ("Gramophone", 1888, ["Son"]), ("Radio", 1895, ["Médias"]), ("Cinématographe", 1895, ["Arts"]),
    ("Bande magnétique", 1928, ["Son"]), ("Télévision", 1927, ["Médias"]), ("Radar civil", 1946, ["Navigation"]),
    ("Disque vinyle LP", 1948, ["Son"]), ("Cassette audio", 1963, ["Son"]), ("Fax (Premier)", 1964, ["Bureau"]),
    ("Email (Premier)", 1971, ["Internet"]), ("Téléphone portable", 1973, ["Mobiles"]), ("VHS", 1976, ["Vidéo"]),
    ("Walkman", 1979, ["Son"]), ("Minitel", 1980, ["Réseaux"]), ("CD Audio", 1982, ["Son"]),
    ("World Wide Web", 1989, ["Internet"]), ("Navigateur Mosaic", 1993, ["Internet"]), ("SMS (Premier)", 1992, ["Mobiles"]),
    ("MP3", 1993, ["Son"]), ("Netflix (Streaming)", 2007, ["Médias"]), ("YouTube", 2005, ["Médias"]),
    ("Twitter", 2006, ["Social"]), ("Facebook", 2004, ["Social"]), ("WhatsApp", 2009, ["Social"]),
    ("Instagram", 2010, ["Social"]), ("TikTok", 2016, ["Social"]), ("Spotify", 2008, ["Musique"]),
    ("Zoom", 2011, ["Vidéo"]), ("Twitch", 2011, ["Médias"]), ("Snapchat", 2011, ["Social"]),
    ("Premier tweet", 2006, ["Internet"]), ("iPad", 2010, ["Mobile"]), ("Kindle (Liseuse)", 2007, ["Lecture"]),
    ("Podcast (Premier)", 2004, ["Audio"]), ("Disquette 3.5 pouces", 1982, ["Informatique"])
]

# Theme 5: Objets du Quotidien (~45)
quotidien = [
    ("Maîtrise du feu", -400000, ["Préhistoire"]), ("Aiguille à coudre", -20000, ["Vêtements"]), ("Miroir", -6000, ["Beauté"]),
    ("Fourchette", 1000, ["Cuisine"]), ("Ciseaux", 100, ["Outils"]), ("Lunettes", 1284, ["Optique"]),
    ("Crayon", 1565, ["Bureau"]), ("Thermomètre", 1714, ["Santé"]), ("Parapluie moderne", 1710, ["Accessoire"]),
    ("Brosse à dents", 1780, ["Hygiène"]), ("Allumettes", 1826, ["Maison"]), ("Seringue", 1853, ["Santé"]),
    ("Timbre-poste", 1840, ["Poste"]), ("Ascenseur", 1852, ["Urbain"]), ("Machine à écrire", 1867, ["Bureau"]),
    ("Jeans", 1873, ["Mode"]), ("Papier toilette en rouleau", 1891, ["Hygiène"]), ("Fermeture éclair", 1891, ["Vêtements"]),
    ("Lame de rasoir Gillette", 1901, ["Beauté"]), ("Réfrigérateur", 1913, ["Cuisine"]), ("Stylo à bille", 1938, ["Bureau"]),
    ("Ruban adhésif (Scotch)", 1930, ["Maison"]), ("Nylon", 1935, ["Textile"]), ("Velcro", 1941, ["Textile"]),
    ("Micro-ondes", 1946, ["Cuisine"]), ("Tupperware", 1946, ["Cuisine"]), ("Carte de crédit", 1950, ["Finance"]),
    ("Code-barres", 1952, ["Commerce"]), ("Post-it", 1968, ["Bureau"]), ("Rubik's Cube", 1974, ["Jeux"]),
    ("Walkman", 1979, ["Musique"]), ("Nespresso", 1986, ["Cuisine"]), ("Smartphone", 2007, ["Technologie"]),
    ("Format MP3", 1993, ["Musique"]), ("Airfryer", 2010, ["Cuisine"]), ("Ampoule LED domestique", 2008, ["Maison"]),
    ("Masque chirurgical (Grand public)", 2020, ["Santé"]), ("Drones civils", 2013, ["Loisirs"]), ("Friteuse sans huile", 2006, ["Cuisine"]),
    ("Vélib (Paris)", 2007, ["Urbain"]), ("Skateboard électrique", 2012, ["Urbain"])
]

# Theme 6: Espace (~45)
espace = [
    ("Gravitation (Newton)", 1687, ["Sciences"]), ("Fusée à propulsion liquide", 1926, ["Techno"]), ("V2 (Missile balistique)", 1942, ["Militaire"]),
    ("Sonde Spoutnik 1", 1957, ["Histoire"]), ("Laïka", 1957, ["Histoire"]), ("Youri Gagarine", 1961, ["Histoire"]),
    ("Valentina Terechkova", 1963, ["Histoire"]), ("Sortie extravéhiculaire (Leonov)", 1965, ["Histoire"]), ("Apollo 11", 1969, ["Histoire"]),
    ("Saliout 1 (Station)", 1971, ["Habitat"]), ("Sonde Viking sur Mars", 1976, ["Planètes"]), ("Pioneer 10", 1972, ["Sonde"]),
    ("Voyager 1", 1977, ["Sonde"]), ("Ariane 1", 1979, ["Fusée"]), ("Navette Columbia", 1981, ["Fusée"]),
    ("Station Mir", 1986, ["Habitat"]), ("Hubble", 1990, ["Optique"]), ("Sonde Galileo (Jupiter)", 1989, ["Planètes"]),
    ("ISS (Premier module)", 1998, ["Habitat"]), ("Touriste spatial (Dennis Tito)", 2001, ["Loisirs"]), ("Mars Express", 2003, ["Mars"]),
    ("Rosetta (Comète 67P)", 2004, ["Espace"]), ("New Horizons (Pluton)", 2006, ["Espace"]), ("Curiosity sur Mars", 2012, ["Mars"]),
    ("Découverte d'exoplanète habitable (Proxima b)", 2016, ["Astronomie"]), ("Photo Trou Noir", 2019, ["Sciences"]),
    ("James Webb Telescope", 2021, ["Optique"]), ("Starship (Premier vol)", 2023, ["Fusée"]), ("Artemis 1", 2022, ["Lune"]),
    ("Sonde Parker (Soleil)", 2018, ["Astronomie"]), ("Chandra (Télescope X)", 1999, ["Astronomie"]), ("Sonde Cassini (Saturne)", 1997, ["Planètes"]),
    ("Premier tour de la Lune (Apollo 8)", 1968, ["Histoire"]), ("Première femme commandant de l'ISS", 2007, ["Histoire"]), ("Sonde Juno (Jupiter)", 2011, ["Planètes"]),
    ("Découverte des anneaux d'Uranus", 1977, ["Astronomie"]), ("Sonde Magellan (Vénus)", 1989, ["Planètes"]), ("Télescope Kepler (Exoplanètes)", 2009, ["Astronomie"]),
    ("Sonde OSIRIS-REx (Bennu)", 2016, ["Espace"]), ("Sonde New Horizons (Arrokoth)", 2019, ["Espace"])
]

# Theme 7: Histoire (~45)
histoire = [
    ("Stonehenge", -2500, ["Archéologie"]), ("Grande Pyramide", -2560, ["Architecture"]), ("Code Hammurabi", -1750, ["Lois"]),
    ("Alphabet Phénicien", -1200, ["Langage"]), ("Rome fondée", -753, ["Politique"]), ("Carthage détruite", -146, ["Guerre"]),
    ("César assassiné", -44, ["Politique"]), ("Pompéi (Éruption)", 79, ["Catastrophe"]), ("Empire romain chute", 476, ["Histoire"]),
    ("Hégire", 622, ["Religion"]), ("Charlemagne couronné", 800, ["Politique"]), ("Guillaume le Conquérant (Hastings)", 1066, ["Guerre"]),
    ("Magna Carta", 1215, ["Lois"]), ("Jeanne d'Arc à Orléans", 1429, ["Guerre"]), ("Amérique découverte", 1492, ["Exploration"]),
    ("Thèses de Luther", 1517, ["Religion"]), ("Révolution française", 1789, ["Politique"]), ("Bataille de Waterloo", 1815, ["Guerre"]),
    ("Pierre de Rosette (Champollion)", 1822, ["Savoir"]), ("Guerre de Sécession", 1861, ["Guerre"]), ("Toutânkhamon (Carter)", 1922, ["Archéologie"]),
    ("Lascaux découverte", 1940, ["Préhistoire"]), ("Débarquement de Normandie", 1944, ["Guerre"]), ("Guerre du Vietnam (Début US)", 1965, ["Guerre"]),
    ("Mur de Berlin chute", 1989, ["Politique"]), ("Otzi (Momie)", 1991, ["Archéologie"]), ("Grotte Chauvet", 1994, ["Préhistoire"]),
    ("Attentats 11 Septembre", 2001, ["Drame"]), ("Tsunami Océan Indien", 2004, ["Catastrophe"]), ("Printemps Arabe", 2011, ["Révolte"]),
    ("Notre-Dame (Incendie)", 2019, ["Drame"]), ("Confinement COVID", 2020, ["Santé"]), ("Élection de Mandela", 1994, ["Politique"]),
    ("Explosion de Tchernobyl", 1986, ["Catastrophe"]), ("Premier pas sur la Lune", 1969, ["Espace"]), ("Indépendance de l'Inde", 1947, ["Politique"]),
    ("Procès de Nuremberg", 1945, ["Justice"]), ("Création de l'ONU", 1945, ["International"]),
    ("Bataille de Verdun", 1916, ["Guerre"]), ("Naufrage du Titanic", 1912, ["Drame"]), ("Première croisade", 1096, ["Histoire"]),
    ("Chute de Constantinople", 1453, ["Histoire"]), ("Ouverture du Canal de Suez", 1869, ["Histoire"])
]

all_raw = [
    (science_tech, ["Inventions", "Sciences", "Technologie"]),
    (transports, ["Transports", "Inventions"]),
    (medecine, ["Médecine", "Santé", "Sciences"]),
    (communication, ["Communication", "Médias", "Inventions"]),
    (quotidien, ["Quotidien", "Inventions"]),
    (espace, ["Espace", "Sciences", "Astronomie"]),
    (histoire, ["Histoire", "Archéologie"])
]

final_cards = []
for data_list, theme_tags in all_raw:
    theme_main = theme_tags[0]
    for name, year, tags in data_list:
        full_tags = list(set(tags + theme_tags))
        final_cards.append(format_card(name, year, full_tags))

import_cards(final_cards)
print(f"Total des cartes préparées : {len(final_cards)}")
