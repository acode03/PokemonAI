import json
from pprint import pprint


class PokemonData:
    def __init__(self) -> None:
        self.data = self._load_data()

    def _load_data(self):
        """
        Loads the JSON file as a Python object that the other methods in this class can interact with.
        Should not be called outside this module
        """
        file = "data/gen9ou-0.json"

        with open(file, "r") as j:
            data = json.loads(j.read())

        return data["data"]

    def get_all_pokemon(self) -> list:
        """
        Returns a list of all legal Pokemon in the format
        """
        return list(self.data.keys())

    def get_pokemon_info(self, pokemon: str) -> dict:
        """
        Returns all the aggregated battle information of the requested Pokemon
        """
        return self.data[pokemon]
    
    def get_most_common_moves(self, pokemon: str, k: int = 4):
        """
        Returns a list of the k most common moves that the specified Pokémon uses
        """
        poke_data = self.get_pokemon_info(pokemon)

        poke_moves = poke_data["Moves"]

        most_common_moves = sorted(poke_moves, key=poke_moves.get, reverse=True)[:k]

        return most_common_moves
    
    def get_most_common_ability(self, pokemon: str):
        """
        Returns the most common ability 
        """
        poke_data = self.get_pokemon_info(pokemon)

        poke_ability = poke_data["Abilities"]

        most_common_ability = max(poke_ability, key=poke_ability.get)

        return most_common_ability
    
    def get_most_common_items(self, pokemon: str):
        """
        Returns a list of the 4 most common items that the specified Pokémon uses
        """
        poke_data = self.get_pokemon_info(pokemon)

        poke_items = poke_data["Items"]

        most_common_items = sorted(poke_items, key=poke_items.get, reverse=True)[:4]

        return most_common_items

    def get_matchup_info(self, pokemon: str, opponent: str) -> list:
        """
        Returns a list encoding common opponent Pokemon that force switches/KOs vs the current Pokemon
        list[1]
        """
        poke_data = self.get_pokemon_info(pokemon)

        return poke_data["Checks and Counters"][opponent]

    def get_most_common_build(self, pokemon: str):
        """
        Returns the most common EV spread and
        """
        poke_data = self.get_pokemon_info(pokemon)

        poke_builds = poke_data["Spreads"]

        most_common_build = max(poke_builds, key=poke_builds.get)

        return most_common_build

    def get_most_common_tera(self, pokemon: str):
        poke_data = self.get_pokemon_info(pokemon)

        poke_tera = poke_data["Tera Types"]

        most_common_tera = max(poke_tera, key=poke_tera.get)

        return most_common_tera


if __name__ == "__main__":
    d = PokemonData()
    pokemon = "Iron Valiant"

    pprint(d.get_most_common_ability(pokemon))
