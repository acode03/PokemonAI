import poke_battle_sim as pb
import copy

# Team 4: Alakazam + Scizor + Rotom-Wash
alakazam = pb.Pokemon(
    "Alakazam",
    50,
    ["psychic", "focus-blast", "shadow-ball", "energy-ball"],
    "male",
    ability="synchronize",
    stats_actual=[145, 75, 80, 195, 120, 190],
)

scizor = pb.Pokemon(
    "Scizor",
    50,
    ["bullet-punch", "u-turn", "superpower", "pursuit"],
    "male",
    ability="technician",
    stats_actual=[175, 185, 160, 95, 140, 115],
)

jirachi = pb.Pokemon(
    "Jirachi",
    50,
    ["stealth-rock", "iron-head", "wish", "u-turn"],
    "genderless",
    ability="serene-grace",
    stats_actual=[185, 120, 140, 110, 165, 122],
)

team4 = [alakazam, scizor, jirachi]

# Team 3: Infernape + Gengar + Swampert
infernape = pb.Pokemon(
    "Infernape",
    50,
    ["close-combat", "flamethrower", "grass-knot", "u-turn"],
    "male",
    ability="blaze",
    stats_actual=[179, 164, 131, 164, 131, 166],
)

swampert = pb.Pokemon(
    "Swampert",
    50,
    ["earthquake", "surf", "ice-beam", "stealth-rock"],
    "male",
    ability="torrent",
    stats_actual=[205, 165, 150, 140, 150, 110],
)

gengar = pb.Pokemon(
    "Gengar",
    50,
    ["shadow-ball", "focus-blast", "thunderbolt", "substitute"],
    "male",
    ability="levitate",
    stats_actual=[155, 95, 100, 190, 120, 180],
)

team3 = [infernape, gengar, swampert]

# Team 2: Torterra + Gyarados + Heatran
torterra = pb.Pokemon(
    "Torterra",
    50,
    ["wood-hammer", "earthquake", "stone-edge", "synthesis"],
    "male",
    ability="overgrow",
    stats_actual=[215, 177, 157, 127, 147, 103],
)

gyarados = pb.Pokemon(
    "Gyarados",
    50,
    ["waterfall", "earthquake", "ice-fang", "dragon-dance"],
    "male",
    ability="intimidate",
    stats_actual=[170, 145, 99, 80, 120, 101],
)

heatran = pb.Pokemon(
    "Heatran",
    50,
    ["fire-blast", "earth-power", "stealth-rock", "explosion"],
    "male",
    ability="flash-fire",
    stats_actual=[185, 110, 166, 195, 176, 117],
)

team2 = [torterra, gyarados, heatran]

# Team 1: Charizard + Starmie + Snorlax
charizard = pb.Pokemon(
    "Charizard",
    50,
    ["dragon-dance", "flare-blitz", "earthquake", "roost"],
    "male",
    ability="blaze",
    stats_actual=[185, 149, 143, 177, 150, 167],
)

starmie = pb.Pokemon(
    "Starmie",
    50,
    ["surf", "thunderbolt", "ice-beam", "rapid-spin"],
    "genderless",
    ability="natural-cure",
    stats_actual=[155, 115, 140, 167, 140, 187],
)

snorlax = pb.Pokemon(
    "Snorlax",
    50,
    ["curse", "body-slam", "earthquake", "rest"],
    "male",
    ability="thick-fat",
    stats_actual=[245, 165, 125, 115, 165, 75],
)

team1 = [charizard, starmie, snorlax]

# Team 5: Venusaur + Blissey + Skarmory
venusaur = pb.Pokemon(
    "Venusaur",
    50,
    ["leech-seed", "sleep-powder", "sludge-bomb", "synthesis"],
    "male",
    ability="overgrow",
    stats_actual=[185, 122, 143, 155, 155, 120],
)

blissey = pb.Pokemon(
    "Blissey",
    50,
    ["soft-boiled", "toxic", "seismic-toss", "aromatherapy"],
    "female",
    ability="natural-cure",
    stats_actual=[255, 60, 115, 125, 185, 115],
)

skarmory = pb.Pokemon(
    "Skarmory",
    50,
    ["roost", "spikes", "whirlwind", "brave-bird"],
    "male",
    ability="keen-eye",
    stats_actual=[175, 140, 195, 80, 133, 120],
)

team5 = [venusaur, blissey, skarmory]

team1Copy = copy.deepcopy(team1)
team2Copy = copy.deepcopy(team2)
team3Copy = copy.deepcopy(team3)
team4Copy = copy.deepcopy(team4)
team5Copy = copy.deepcopy(team5)