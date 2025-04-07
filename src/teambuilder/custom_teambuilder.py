import asyncio

import numpy as np

from poke_env.player import RandomPlayer
from poke_env.teambuilder import Teambuilder


class SingleTeamTeambuilder(Teambuilder):
    def __init__(self, team):
        self.team = self.join_team(self.parse_showdown_team(team))

    def yield_team(self):
        return self.team


# class RandomTeamFromPool(Teambuilder):
#     def __init__(self, teams):
#         self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

#     def yield_team(self):
#         return np.random.choice(self.teams)
     

team = """

Porygon2 @ Eviolite 
Ability: Download  
Tera Type: Poison  
EVs: 244 HP / 12 Def / 252 SpD  
Bold Nature  
- Tri Attack  
- Shadow Ball  
- Thunder Wave  
- Recover

Dragonite @ Loaded Dice
Ability: Multiscale
Tera Type: Fire
EVs: 252 Atk / 252 Spe / 4 HP
Adamant  Nature
- Extreme Speed
- Scale Shot
- Fire Punch
- Dragon Dance

Gholdengo @ Covert Cloak
Ability: Good as Gold
Tera Type: Flying
EVs: 208 SpA / 212 HP / 84 Spe / 4 Def
Modest Nature
- Make It Rain
- Shadow Ball
- Psyshock
- Nasty Plot

Corviknight @ Sitrus Berry
Ability: Stamina
Tera Type: Fairy  
EVs: 252 HP / 60 Def / 196 SpD
Careful Nature
- Dragon Tail
- Body Press
- Foul Play
- Stealth Rock

Dondozo @ Leftovers
Ability: Unaware
Tera Type: Steel
EVs: 252 HP / 252 Def / 4 SpD
Lax Nature
- Wave Crash
- Curse
- Yawn
- Protect

Meowscarada @ Choice Band
Ability: Protean
Tera Type: Steel
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Flower Trick
- Knock Off
- Triple Axel
- U-Turn
"""
custom_builder = SingleTeamTeambuilder(team)
# custom_builder = RandomTeamFromPool([team_1, team_2])


async def main():

    # try:
    #     # Create players
    #     player1 = MinMaxAgent(battle_format="gen9randombattle", max_depth=2)
    #     player2 = RandomPlayer(battle_format="gen9randombattle")

    #     print("Starting battle...")
    #     print("Player 1: MinMax Agent")
    #     print("Player 2: Random Agent")

    #     # Run any number of battles
    #     await player1.battle_against(player2, n_battles=50)

    #     print("\nBattle Results:")
    #     print(f"MinMax Agent wins: {player1.n_won_battles}")
    #     print(f"Random Agent wins: {player2.n_won_battles}")

    # except Exception as e:
    #     print(f"Error in main: {str(e)}")

    # We create two players
    player_1 = RandomPlayer(
        battle_format="gen9ou", team=custom_builder, max_concurrent_battles=10
    )
    player_2 = RandomPlayer(
        battle_format="gen9ou", team=custom_builder, max_concurrent_battles=10
    )

    await player_1.battle_against(player_2, n_battles=5)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())