import poke_battle_sim.core
import poke_battle_sim.core.battle
from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.player.random_player import RandomPlayer
from teambuilder.custom_teambuilder import custom_builder

# from data.type_chart import TYPE_CHART
# from data.vigor_chart import VIGOR_CHART
import numpy as np
from typing import List, Tuple, Optional, Union, Dict
import random
import poke_battle_sim
from poke_battle_sim import PokeSim
from poke_battle_sim.conf import global_settings as gs
from poke_battle_sim import PokeSim
from poke_battle_sim.conf import global_settings as gs
from MinimaxNode import MiniMaxNode


class MinMaxAgent(Player):
    def __init__(self, battle_format: str, teambuilder=None, max_depth: int = 2):
        if teambuilder is not None:
            team = teambuilder.yield_team()
        else:
            team = None
        super().__init__(battle_format=battle_format, team=team)
        self.max_depth = max_depth
        self.sim_battle = None

    def simulate_state(
        self, battle: poke_battle_sim.Battle, move1: str, move2: str
    ) -> poke_battle_sim.Battle:
        if move1 == "switch":
            action1 = ["other", "switch"]
        else:
            action1 = ["move", move1]

        if move2 == "switch":
            action2 = ["other", "switch"]
        else:
            action2 = ["move", move2]

        battle.turn(t1_turn=action1, t2_turn=action2)

        return battle

    # def battle_engine(self, battle: poke_battle_sim.Battle) -> float:
    #     """
    #     As of now so I dont forget this is what our engine is doing:

    #     Args:
    #         battle: A poke_battle_sim Battle object containing the current battle state

    #     Returns:
    #         Float point modifier representing the evaluated battle state
    #     """
    #     # the original variable definitions
    #     poke = poke_battle_sim.Pokemon("Pikachu", 50, ["tackle"], "male")
    #     p1 = poke_battle_sim.Trainer("a", [poke])
    #     p2 = poke_battle_sim.Trainer("b", [poke])

    #     # Create a new battle instance
    #     sim_battle = poke_battle_sim.Battle(p1, p2)

    #     point_modifier = 0.0

    #     # Get the current Pokemon for each trainer
    #     our_pokemon = sim_battle.t1.current_poke
    #     opponent_pokemon = sim_battle.t2.current_poke

    #     # Game State 1: Team HP States
    #     our_hp_fraction = our_pokemon.cur_hp / our_pokemon.max_hp
    #     opp_hp_fraction = opponent_pokemon.cur_hp / opponent_pokemon.max_hp

    #     # Penalize for low HP
    #     if our_hp_fraction < 1.0:  # Any damage
    #         point_modifier -= 15
    #     if our_hp_fraction < 0.5:  # Below half health
    #         point_modifier -= 25
    #     if our_hp_fraction < 0.25:  # Critical health
    #         point_modifier -= 40

    #     # Reward for opponent's low HP
    #     if opp_hp_fraction < 1.0:  # Any damage
    #         point_modifier += 10
    #     if opp_hp_fraction < 0.5:  # Below half health
    #         point_modifier += 20
    #     if opp_hp_fraction < 0.25:  # Critical health
    #         point_modifier += 35

    #     # Game State 2: Type Advantage/Disadvantage
    #     if our_pokemon and opponent_pokemon:
    #         for our_type in our_pokemon.types:
    #             if our_type:  # Check if type exists (not None)
    #                 for opp_type in opponent_pokemon.types:
    #                     if opp_type:  # Check if type exists (not None)
    #                         effectiveness = PokeSim.get_type_ef(our_type, opp_type)
    #                         if effectiveness > 1:  # Super effective
    #                             point_modifier += 45
    #                         elif effectiveness < 1:  # Not very effective
    #                             point_modifier -= 30
    #                         elif effectiveness == 0:  # Immune
    #                             point_modifier -= 60

    #     # Game State 3: Status Conditions
    #     if our_pokemon.nv_status:
    #         if our_pokemon.nv_status == gs.BURNED:
    #             point_modifier -= 30  # Significant penalty for burn (reduces attack)
    #         elif our_pokemon.nv_status == gs.PARALYZED:
    #             point_modifier -= 40  # Major penalty for paralysis (reduces speed)
    #         elif our_pokemon.nv_status == gs.POISONED:
    #             point_modifier -= 25  # Moderate penalty for poison
    #         elif our_pokemon.nv_status == gs.BADLY_POISONED:
    #             point_modifier -= 35  # Higher penalty for toxic
    #         elif our_pokemon.nv_status == gs.ASLEEP:
    #             point_modifier -= 45  # Major penalty for sleep

    #     if opponent_pokemon.nv_status:
    #         if opponent_pokemon.nv_status == gs.BURNED:
    #             point_modifier += 25  # Reward for opponent's burn
    #         elif opponent_pokemon.nv_status == gs.PARALYZED:
    #             point_modifier += 35  # Good reward for opponent's paralysis
    #         elif opponent_pokemon.nv_status == gs.POISONED:
    #             point_modifier += 20  # Moderate reward for poison
    #         elif opponent_pokemon.nv_status == gs.BADLY_POISONED:
    #             point_modifier += 30  # Higher reward for toxic
    #         elif opponent_pokemon.nv_status == gs.ASLEEP:
    #             point_modifier += 40  # Major reward for sleep

    #     # Game State 4: Field Effects
    #     if sim_battle.battlefield:
    #         if sim_battle.battlefield.weather == gs.RAIN:
    #             # Evaluate rain effects based on typing
    #             if 'water' in our_pokemon.types:
    #                 point_modifier += 20
    #             if 'fire' in our_pokemon.types:
    #                 point_modifier -= 20
    #         elif sim_battle.battlefield.weather == gs.HARSH_SUNLIGHT:
    #             # Evaluate sun effects based on typing
    #             if 'fire' in our_pokemon.types:
    #                 point_modifier += 20
    #             if 'water' in our_pokemon.types:
    #                 point_modifier -= 20

    #     # Game State 5: Ability Evaluation
    #     if our_pokemon.ability:
    #         # Add points for particularly valuable abilities
    #         valuable_abilities = ['intimidate', 'levitate', 'speed-boost', 'drought', 'drizzle']
    #         if our_pokemon.ability in valuable_abilities:
    #             point_modifier += 25

    #     return point_modifier

    # def action_engine(self, battle: Battle) -> float:
    # """
    # Analyzes move-related states and returns point modifiers for the total score
    # """
    # point_move_modifier = 0.0

    # # Case 1: Strong moves available
    # for move in battle.available_moves:
    #     if getattr(move, 'base_power', 0) > 90:  # Strong move threshold
    #         point_move_modifier += 25  # Bonus for having powerful moves available

    # # Case 2: Move type variety (rewards having moves of different types)
    # move_types = set(getattr(move, 'type', None) for move in battle.available_moves)
    # if len(move_types) >= 3:  # If we have moves of 3 or more different types
    #     point_move_modifier += 30

    # return point_move_modifier

    def choose_move(self, battle: Battle) -> BattleOrder:  # type: ignore
        """Main method to choose moves using MinMax algorithm"""
        # try:
        """
            # Get all possible actions (moves and switches unified)
            our_moves = self.get_possible_moves(battle)
            opponent_moves = self.get_possible_opponent_moves(battle)

            # Create payoff matrix
            payoff_matrix = self.create_payoff_matrix(battle, our_moves, opponent_moves)

            # Get best move using minimax
            best_move = self.minimax(self.sim_battle, self.max_depth, 10000, 100000, True)  # type: ignore

            if best_move is None or best_move[1] is None:
                return self.choose_random_move(battle)

            return self.create_order(best_move[1])
        """
        return self.choose_default_move()

    def evaluate_state(self, battle: poke_battle_sim.Battle) -> float:
        """Evaluate the current battle state"""
        try:
            # Get HP percentages (0-100)
            our_hp = battle.t1.current_poke.cur_hp
            opponent_hp = battle.t1.current_poke.cur_hp

            # Get Pokemon counts (0-6)

            # our_pokemon_left = len([mon for mon in battle.team.values() if not mon.fainted])
            # opponent_pokemon_left = len([mon for mon in battle.opponent_team.values() if not mon.fainted])

            # Calculate scores for different factors
            hp_score = our_hp - opponent_hp
            # pokemon_score = (our_pokemon_left - opponent_pokemon_left) * 50
            status_score = 0

            # Status conditions

            """
            battle.t1.current_poke
            
            if battle.active_pokemon.status is not None:
                status_score -= 20
            if battle.opponent_active_pokemon.status is not None:
                status_score += 20

            # Type advantage scoring
            type_score = 0
            #our_types = battle.active_pokemon.types
            opponent_types = battle.opponent_active_pokemon.types

            # Calculate type advantage for our Pokemon against opponent
            for our_type in our_types:
                for opp_type in opponent_types:
                    if opp_type in TYPE_CHART and our_type in TYPE_CHART[opp_type]["damageTaken"]:
                        damage_taken = TYPE_CHART[opp_type]["damageTaken"][our_type]
                        if damage_taken == 1:  # Super effective
                            type_score += 30
                        elif damage_taken == 2:  # Not very effective
                            type_score -= 15
                        elif damage_taken == 3:  # Immune
                            type_score -= 30

            # Calculate opponent's type advantage against us
            for opp_type in opponent_types:
                for our_type in our_types:
                    if our_type in TYPE_CHART and opp_type in TYPE_CHART[our_type]["damageTaken"]:
                        damage_taken = TYPE_CHART[our_type]["damageTaken"][opp_type]
                        if damage_taken == 1:  # Super effective against us
                            type_score -= 30
                        elif damage_taken == 2:  # Not very effective against us
                            type_score += 15
                        elif damage_taken == 3:  # We're immune
                            type_score += 30

            # Vigor scoring
            vigor_score = 0

            # Calculate our Pokemon's vigor penalty
            if battle.active_pokemon.status:
                status = battle.active_pokemon.status.value
                if status in VIGOR_CHART:
                    vigor_info = VIGOR_CHART[status]
                    # Base penalty based on severity
                    base_penalty = vigor_info["severity"] * -10

                    # Additional penalties based on status effects
                    if "damage" in vigor_info:  # For burn, poison
                        vigor_score += base_penalty - 15
                    if "attack_modifier" in vigor_info:  # For burn
                        if any(move.category == "PHYSICAL" for move in battle.available_moves):
                            vigor_score -= 20
                    if "speed_modifier" in vigor_info:  # For paralysis
                        vigor_score -= 25
                    if "move_chance" in vigor_info:  # For sleep, freeze
                        if vigor_info["move_chance"] == 0:
                            vigor_score -= 40
                        else:
                            vigor_score -= 20

            # Calculate opponent's vigor penalty (reverse the scores)
            if battle.opponent_active_pokemon.status:
                status = battle.opponent_active_pokemon.status.value
                if status in VIGOR_CHART:
                    vigor_info = VIGOR_CHART[status]
                    base_bonus = vigor_info["severity"] * 10

                    if "damage" in vigor_info:
                        vigor_score += base_bonus + 15
                    if "attack_modifier" in vigor_info:
                        vigor_score += 20
                    if "speed_modifier" in vigor_info:
                        vigor_score += 25
                    if "move_chance" in vigor_info:
                        if vigor_info["move_chance"] == 0:
                            vigor_score += 40
                        else:
                            vigor_score += 20

            # Combine all scores
            total_score = hp_score + pokemon_score + status_score + type_score + vigor_score

            # Add battle engine point modifiers
            total_score += self.battle_engine(battle)

            # Add action engine point modifiers
            # total_score += self.action_engine(battle)

            return total_score
            
        """

        except Exception as e:
            print(f"Error in evaluate_state: {str(e)}")
            return 0.0

        return 5

    def minimax(
        self,
        battle: poke_battle_sim.Battle,
        depth: int,
        alpha: int,
        beta: int,
        isPlayerTurn: bool,
    ) -> float:
        """Minimax algorithm"""

        if depth == 0 or battle.is_finished:
            return self.evaluate_state(battle)

        if isPlayerTurn:
            maxValue = -float("Inf")

        return 1

    """
    def choose_random_move(self, battle: Battle) -> BattleOrder:
        moves = self.get_possible_moves(battle)
        if moves:
            return self.create_order(random.choice(moves))
        return self.create_order("struggle")
        
    """

    def get_possible_moves(self, battle: Battle) -> List[Union[Pokemon, BattleOrder]]:
        """Get all possible moves and switches as one unified moveset"""
        possible_actions = []
        if battle.available_moves:
            possible_actions.extend(battle.available_moves)
        if battle.available_switches:
            possible_actions.extend(battle.available_switches)
        return possible_actions

    def get_possible_opponent_moves(
        self, battle: Battle
    ) -> List[Union[Pokemon, BattleOrder]]:
        """Estimate opponent's possible moves"""
        return self.get_possible_moves(battle)


async def main():
    try:
        # Create players with custom teambuilder
        player1 = MinMaxAgent(
            battle_format="gen9ou", teambuilder=custom_builder, max_depth=2
        )
        player2 = RandomPlayer(
            battle_format="gen9ou", team=custom_builder.yield_team()
        )  # Note different format for RandomPlayer

        print("Starting battle...")
        print("Player 1: MinMax Agent")
        print("Player 2: Random Agent")

        # Run any number of battles
        await player1.battle_against(player2, n_battles=50)

        print("\nBattle Results:")
        print(f"MinMax Agent wins: {player1.n_won_battles}")
        print(f"Random Agent wins: {player2.n_won_battles}")

    except Exception as e:
        print(f"Error in main: {str(e)}")


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(main())
