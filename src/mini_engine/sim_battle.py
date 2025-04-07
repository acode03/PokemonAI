import poke_battle_sim as pb


class BattleSim:
    def __init__(self, battle: pb.Battle) -> None:
        self.battle = battle
        self.pokemon1 = {
            "name": "",
            "stats": [],
            "cur_hp": 0,
            "type": set(),
            "moves": {},
            "level": 10,
            "has_fainted": False,
        }
 
        self.pokemon2 = {
            "name": "",
            "stats": [],
            "cur_hp": 0,
            "type": set(),
            "moves": {},
            "level": 10,
            "has_fainted": False,
        }

    def get_battle_info(self):
        # Get both pokemon info
        # For each pokemon, get their stats, cur hp, and moves

        # Trainer 1's Pokémon (pokemon1)
        trainer1_pokemon = self.battle.t1.current_poke
        self.pokemon1["name"] = trainer1_pokemon.name
        self.pokemon1["stats"] = trainer1_pokemon.stats_actual
        self.pokemon1["cur_hp"] = trainer1_pokemon.cur_hp
        self.pokemon1["type"] = set(
            trainer1_pokemon.types
        )  # set because Pokémon can have one or two types
        self.pokemon1["moves"] = [
            {
                "name": move.name,
                "power": move.power,
                "type": move.type,
                "pp": move.cur_pp,
            }
            for move in trainer1_pokemon.moves
        ]

        # self.pokemon1["moves"] = [{"name": growl,...}, {"name": thunderbolt, ...}, ...]
        # self.pokemon1["moves"][0]["name"]

        # self.pokemon1["moves"] = {"thunderbolt": {"power":100, "pp":12, "type": "Special"},
        #                           "growl": {"power":100, "pp":12, "type": "Special"} }
        # self.pokemon1["moves"]["thunderbolt"]["power"]

        # Trainer 2's Pokémon (pokemon2)
        trainer2_pokemon = self.battle.t2.current_poke
        self.pokemon2["name"] = trainer2_pokemon.name
        self.pokemon2["stats"] = trainer2_pokemon.stats_actual
        self.pokemon2["cur_hp"] = trainer2_pokemon.cur_hp
        self.pokemon2["type"] = set(
            trainer2_pokemon.types
        )  # set because Pokémon can have one or two types
        self.pokemon2["moves"] = [
            {
                "name": move.name,
                "power": move.power,
                "type": move.type,
                "pp": move.cur_pp,
            }
            for move in trainer2_pokemon.moves
        ]
        pass

    def damage_calculator(self, move, atk_pokemon, def_pokemon):
        lvl = atk_pokemon["level"]
        power = move["power"]

        if move["type"] == "Physical":
            atk = atk_pokemon["stats"][1]
            defense = def_pokemon["stats"][2]
        else:
            atk = atk_pokemon["stats"][3]
            defense = def_pokemon["stats"][4]

        damage = (((((2 * lvl) / 5) + 2) * power * atk) / (50 * defense)) + 2

        return damage

    def deal_damage(self, move, atk_pokemon, def_pokemon):
        damage = self.damage_calculator(move, atk_pokemon, def_pokemon)

        def_pokemon["cur_hp"] -= damage
        self.faint_check(def_pokemon)

    def faint_check(self, pokemon):
        if pokemon["cur_hp"] < 0:
            pokemon["has_fainted"] = True

    def can_make_move(self, pokemon):
        if pokemon["has_fainted"] == False:
            return True
        else:
            return False

    def simulate_turn(self, move1, move2):
        self.get_battle_info()

        speed1 = self.pokemon1["stats"][5]
        speed2 = self.pokemon2["stats"][5]

        if speed1 > speed2:
            if self.can_make_move(self.pokemon1):
                self.deal_damage(move1, self.pokemon1, self.pokemon2)

            if self.can_make_move(self.pokemon2):
                self.deal_damage(move2, self.pokemon2, self.pokemon1)
        else:
            if self.can_make_move(self.pokemon2):
                self.deal_damage(move1, self.pokemon2, self.pokemon1)

            if self.can_make_move(self.pokemon1):
                self.deal_damage(move2, self.pokemon1, self.pokemon2)


articuno = pb.Pokemon(
    "Articuno",
    10,
    ["tackle", "tailwind"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 55],
)

pikachu = pb.Pokemon(
    "Pikachu",
    13,
    ["thunder-shock", "growl"],
    "male",
    stats_actual=[100, 50, 50, 50, 50, 50],
)
ash = pb.Trainer("Ash", [articuno], selection=None)


misty = pb.Trainer("Misty", [pikachu])
battle = pb.Battle(ash, misty)
sim = BattleSim(battle)

battle.turn(t1_turn=["move", "tackle"], t2_turn=["move", "thunder-shock"])
print("turn")

battle.get_all_text()
