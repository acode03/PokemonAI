import poke_battle_sim as pb
import copy
import random
from poke_battle_sim.conf import global_settings as gs
from poke_battle_sim.core.pokemon import Pokemon
from team import *
import sys

class MinimaxTrainer(pb.Trainer):
    def __init__(self, name: str, poke_list: list[Pokemon], selection):
        super().__init__(name, poke_list, selection)
        self.name = name
        self.poke_id = 0
        self.selection = selection
        self.t2_poke_id = 0

    
    def simulate_turn(self, battle: pb.Battle, move1, move2):     
        new_battle = copy.deepcopy(battle)
        new_battle.turn(
            t1_turn=self.get_translated_move_name(move1),
            t2_turn=self.get_translated_move_name(move2),
        )

        return new_battle

    def evaluate_state(self, battle: pb.Battle) -> int:
        point_modifier: int = 0
        
        # Get current Pokemon for each trainer
        our_pokemon = battle.t1.current_poke
        opponent_pokemon = battle.t2.current_poke

        # Calculate HP fractions
        our_hp_fraction = our_pokemon.cur_hp / our_pokemon.max_hp
        opp_hp_fraction = opponent_pokemon.cur_hp / opponent_pokemon.max_hp

        #new attempt at hp
        health_points = 50

        ourPokemonList = battle.t1.poke_list
        oppPokemonList = battle.t2.poke_list

        ourPokemonTotal = 0
        ourPokemonActual = 0

        oppPokemonTotal = 0
        oppPokemonActual = 0

        for poke in ourPokemonList:
            ourPokemonActual += poke.cur_hp
            ourPokemonTotal += poke.max_hp

        for poke in oppPokemonList:
            oppPokemonActual += poke.cur_hp
            oppPokemonTotal += poke.max_hp 

        ourTotalFraction = ourPokemonActual / ourPokemonTotal
        oppTotalFraction = oppPokemonActual / oppPokemonTotal

        difference = ourTotalFraction - oppTotalFraction

        point_modifier += difference * health_points
        
        return point_modifier

    # doesn't do anything
    def get_opponent_stats(self, opponent):
        return opponent.copy()

    
    def get_translated_move_name(self, move):
        if type(move) == int:
            return ['other', 'switch']
        else:
            return ["move", move.name]

    # what is the point of this? it seems like we loop through this stuff anyways in minimax?
    def choose_move(self, battle: pb.Battle):
        new_battle = copy.deepcopy(battle)
        bestMove = None
        max_score = float("-inf")
        bestSwitch = None
        max_switch_score = float('-inf')

        # consider the switch
        #trainer selector function

        for move in self.current_poke.moves + list(range(len(battle.t1.poke_list))):


            """This might break things when the pokemon faints and has to choose what to switch to
            so maybe we could put it in a different place? discuss with team"""
            if type(move) == int:
                battle.t1.poke_id = move

            """we are only going to run the minimax call if:
            its a valid switch and move is an int
            its a normal move and we've checked if it's valid"""
            if type(move) == int and self.validSwitch(move, True):
                score = self.minimax(new_battle, move, 3, False, float('-inf'), float('inf'))
                if score > max_switch_score:
                    max_switch_score = score
                    battle.t1.poke_id = move
            elif type(move) != int and battle.t1.can_use_move(self.get_translated_move_name(move)):
                score = self.minimax(new_battle, move, 3, False, float('-inf'), float('inf'))
            else:
                continue
        
        
            if score > max_score:
                max_score = score
                bestMove = move

        return self.get_translated_move_name(bestMove)
    
    def validSwitch(self, pokeID, isMaxPlayer):
        #check if player can switch out and check if its a valid pokemon to switch to
        if isMaxPlayer: #I think these flags maybe fix the issue of need two minimax trainers??
            if battle.t1.can_switch_out() and  battle.t1.poke_list[pokeID].cur_hp > 0 and battle.t1.poke_list[pokeID] != battle.t1.current_poke:
                return True
            else:
                return False
        else:
            if battle.t2.can_switch_out() and battle.t2.poke_list[pokeID].cur_hp > 0 and battle.t2.poke_list[pokeID] != battle.t2.current_poke:
                return True
            else:
                return False


    def minimax(
        self, battle: pb.Battle, move, depth, isMaxPlayer, alpha, beta
    ):

        if depth == 0 or battle.is_finished():
            score = self.evaluate_state(battle)

            return score

        if isMaxPlayer:
            max_score = -float("Inf")

            for cur_move in self.current_poke.moves + list(range(len(battle.t1.poke_list))):


                if type(cur_move) == int:
                    self.poke_id = cur_move

                # if cur_move is an int(if we are switching, we need to check if it's valid othwesie we shouldn't consider it)
                # if it isn't valid switch we pass and don't even consider it.
                if type(cur_move) == int and self.validSwitch(cur_move, True):
                    score = self.minimax(battle, cur_move, 1, False, alpha, beta)
                elif type(cur_move) != int and battle.t1.can_use_move(self.get_translated_move_name(cur_move)):
                    score = self.minimax(battle, cur_move, 1, False, alpha, beta)
                else:
                    continue

                max_score = max(score, max_score)
                alpha = max(alpha, max_score)

                if alpha >= beta:
                    break

            return max_score

        else:
            min_score = float("Inf")

            for opp_move in battle.t2.current_poke.moves + list(range(len(battle.t1.poke_list))):
                
                if type(opp_move) == int:
                    self.t2_poke_id = opp_move

                #check if its a valid swap
                if type(opp_move) == int and self.validSwitch(opp_move, isMaxPlayer):
                    new_battle = self.simulate_turn(battle, move, opp_move)
                elif type(opp_move) != int and battle.t2.can_use_move(self.get_translated_move_name(opp_move)):
                    new_battle = self.simulate_turn(battle, move, opp_move)
                else:
                    continue

                score = self.minimax(new_battle, None, depth - 1, True, alpha, beta)

                min_score = min(score, min_score)
                beta = min(beta, min_score)

                if alpha >= beta:
                    break

            # print("min score", min_score)
            # print("Misty move associated with min score:",self.get_translated_move_name(min_move))
            # print("Ash move associated with min score:",self.get_translated_move_name(min_moveAsh))
            
            return min_score




#this is for minimaxTrainer or t1
def selection_function(battle):
    battle.t1.current_poke = battle.t1.poke_list[battle.t1.poke_id]

#this will be non minimax or t2
def selection_function2(battle):
    battle.t2.current_poke = battle.t2.poke_list[battle.t1.t2_poke_id]

# #doesn't consider switches, should maybe add that?
def t2RandomTurn(battle):
    
    currentPokeMoves = battle.t2.current_poke.moves
    randomMove = random.choice(currentPokeMoves)

    while not battle.t2.can_use_move(["move", randomMove.name]):
        randomMove = random.choice(currentPokeMoves)

    return ["move", randomMove.name]


teamList = [team1, team2, team3, team4, team5]


ash = MinimaxTrainer("ash", team3, selection_function)

misty = pb.Trainer("misty", team4, selection_function2)

battle = pb.Battle(ash, misty)

battle.start()

while not battle.is_finished():

    battle.turn(t1_turn=ash.choose_move(battle), t2_turn=t2RandomTurn(battle))


print(battle.all_text)
            


#automation

# results = {}

# for sim1 in [team3, team4, team5]:
#     for sim2 in [team3, team4, team5]:

#         if sim1 == sim2:
#             sim2 = copy.deepcopy(sim1)
        
#         matchUp = str(sim1[0].name) + " vs " + str(sim2[0].name)
        
#         print(matchUp)
        
#         ashWinCounter = 0
        
        
        
        # ash = MinimaxTrainer("ash", copy.deepcopy(sim1), selection_function)

        # misty = pb.Trainer("misty", copy.deepcopy(sim2), selection_function2)
            
            
            
            
#         for i in range(50):
            
#             print("Battle: " + str(i))
            
#             ash = MinimaxTrainer("ash", copy.deepcopy(sim1), selection_function)

#             misty = pb.Trainer("misty", copy.deepcopy(sim2), selection_function2)

#             battle = pb.Battle(ash, misty)

#             battle.start()

#             while not battle.is_finished():

#                 battle.turn(t1_turn=ash.choose_move(battle), t2_turn=t2RandomTurn(battle))
                
#             if battle.get_winner().name == "ash":
#                 ashWinCounter += 1
                
#         results[matchUp] = ashWinCounter
        
#         with open('results.txt', 'a') as file:
#             file.write(matchUp + ": " + str(ashWinCounter) + "\n")
