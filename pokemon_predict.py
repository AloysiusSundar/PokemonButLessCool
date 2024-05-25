import random
import pandas as pd
from sklearn.linear_model import LogisticRegression

class Pokemon:
    def __init__(self, name, type, level, hp, attack, defense, speed, moves=[]):
        self.name = name
        self.type = type
        self.level = level
        self.max_hp = hp
        self.hp = self.max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_opponent(self, opponent, move_idx):
        if move_idx < 0 or move_idx >= len(self.moves):
            print("Invalid move selection!")
            return 0
        
        move = self.moves[move_idx]
        damage = move['power'] - opponent.defense
        opponent.take_damage(damage)
        return damage

class Battle:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon

        # Train predictive model
        self.model = LogisticRegression()

    def train_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict_outcome(self, features):
        return self.model.predict(features)

    def calculate_win_probability(self):
        player_hp_ratio = self.player_pokemon.hp / self.player_pokemon.max_hp
        opponent_hp_ratio = self.opponent_pokemon.hp / self.opponent_pokemon.max_hp

        feature_names = ['player_level', 'opponent_level', 'player_hp_ratio', 'opponent_hp_ratio', 'player_speed', 'opponent_speed']
        predicted_outcome = self.model.predict([[self.player_pokemon.level, self.opponent_pokemon.level,
                                                 player_hp_ratio, opponent_hp_ratio,
                                                 self.player_pokemon.speed, self.opponent_pokemon.speed]])[0]

        if predicted_outcome == 1:
            player_win_probability = 1.0
            opponent_win_probability = 0.0
        elif predicted_outcome == 0:
            player_win_probability = 0.0
            opponent_win_probability = 1.0
        else:
            player_win_probability = (predicted_outcome + player_hp_ratio) / 2
            opponent_win_probability = 1 - player_win_probability

        return player_win_probability, opponent_win_probability

    def start_battle(self):
        print("A wild {} appeared!".format(self.opponent_pokemon.name))
        while self.player_pokemon.hp > 0 and self.opponent_pokemon.hp > 0:
            if self.player_pokemon.speed >= self.opponent_pokemon.speed:
                self.player_turn()
                if self.opponent_pokemon.hp <= 0:
                    break
                self.opponent_turn()
            else:
                self.opponent_turn()
                if self.player_pokemon.hp <= 0:
                    break
                self.player_turn()

    def player_turn(self):
        print("\nYour {}'s HP: {}/{}".format(self.player_pokemon.name, self.player_pokemon.hp, self.player_pokemon.max_hp))
        print("{}'s HP: {}/{}".format(self.opponent_pokemon.name, self.opponent_pokemon.hp, self.opponent_pokemon.max_hp))
        print("Your moves:")
        for idx, move in enumerate(self.player_pokemon.moves):
            print(f"{idx + 1}. {move['name']} ({move['power']} power)")
        player_choice = input("\nChoose your move (enter the move number): ")
        try:
            move_idx = int(player_choice) - 1
            damage = self.player_pokemon.attack_opponent(self.opponent_pokemon, move_idx)
            print("Your {} used {}! {} took {} damage.".format(self.player_pokemon.name, self.player_pokemon.moves[move_idx]['name'], self.opponent_pokemon.name, damage))
            if self.opponent_pokemon.hp <= 0:
                print("You defeated {}!".format(self.opponent_pokemon.name))
                return
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")

        player_win_probability, opponent_win_probability = self.calculate_win_probability()
        print("Player Win Probability: {:.2f}%".format(player_win_probability * 100))
        print("Opponent Win Probability: {:.2f}%".format(opponent_win_probability * 100))

    def opponent_turn(self):
        opponent_move_idx = random.randint(0, len(self.opponent_pokemon.moves) - 1)
        opponent_damage = self.opponent_pokemon.attack_opponent(self.player_pokemon, opponent_move_idx)
        print("{} used {}! Your {} took {} damage.".format(self.opponent_pokemon.name, self.opponent_pokemon.moves[opponent_move_idx]['name'], self.player_pokemon.name, opponent_damage))
        if self.player_pokemon.hp <= 0:
            print("{} defeated your {}!".format(self.opponent_pokemon.name, self.player_pokemon.name))


        player_win_probability, opponent_win_probability = self.calculate_win_probability()
        print("Player Win Probability: {:.2f}%".format(player_win_probability * 100))
        print("Opponent Win Probability: {:.2f}%".format(opponent_win_probability * 100))

X_train = pd.DataFrame({
    'player_level': [5] * 100,  
    'opponent_level': [3] * 100,
    'player_hp_ratio': [0.8] * 100,
    'opponent_hp_ratio': [0.6] * 100,
    'player_speed': [78] * 100,
    'opponent_speed': [120] * 100
})
y_train = pd.Series([1, 0, 1, 0] * 25) 

feraligatr_moves = [
    {'name': 'Water Gun', 'power': 40},
    {'name': 'Ice Beam', 'power': 90},
    {'name': 'Bite', 'power': 60},
    {'name': 'Hydro Pump', 'power': 110}
]

sceptile_moves = [
    {'name': 'Leaf Blade', 'power': 85},
    {'name': 'Dragon Claw', 'power': 80},
    {'name': 'Giga Drain', 'power': 75},
    {'name': 'Earthquake', 'power': 100}
]

player_pokemon = Pokemon("Feraligatr", "Water", 5, hp=85, attack=105, defense=100, speed=78, moves=feraligatr_moves)
opponent_pokemon = Pokemon("Sceptile", "Grass", 3, hp=70, attack=85, defense=65, speed=120, moves=sceptile_moves)

battle = Battle(player_pokemon, opponent_pokemon)
battle.train_model(X_train, y_train)
battle.start_battle()