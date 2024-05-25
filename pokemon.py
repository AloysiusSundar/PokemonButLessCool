import random

class Pokemon:
    def __init__(self, name, type, level):
        self.name = name
        self.type = type
        self.level = level
        self.max_hp = level * 10
        self.hp = self.max_hp
        self.attack = level * 2
        self.defense = level * 1.5
        self.moves = []

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

    def start_battle(self):
        print("A wild {} appeared!".format(self.opponent_pokemon.name))
        while self.player_pokemon.hp > 0 and self.opponent_pokemon.hp > 0:
            print("\nYour {}'s HP: {}/{}".format(self.player_pokemon.name, self.player_pokemon.hp, self.player_pokemon.max_hp))
            print("{}'s HP: {}/{}".format(self.opponent_pokemon.name, self.opponent_pokemon.hp, self.opponent_pokemon.max_hp))
            print("Your {}'s Moves:".format(self.player_pokemon.name))
            for idx, move in enumerate(self.player_pokemon.moves):
                print("{}. {}: Power {}".format(idx + 1, move['name'], move['power']))
            player_choice = input("\nWhat will you do? (Choose move by index or type 'run'): ")
            if player_choice.lower() == 'run':
                print("You ran away successfully!")
                break
            try:
                move_idx = int(player_choice) - 1
                damage = self.player_pokemon.attack_opponent(self.opponent_pokemon, move_idx)
                print("Your {} used {}! {} took {} damage.".format(self.player_pokemon.name, self.player_pokemon.moves[move_idx]['name'], self.opponent_pokemon.name, damage))
                if self.opponent_pokemon.hp <= 0:
                    print("You defeated {}!".format(self.opponent_pokemon.name))
                    break
            except ValueError:
                print("Invalid choice. Try again.")

            opponent_move_idx = random.randint(0, len(self.opponent_pokemon.moves) - 1)
            opponent_damage = self.opponent_pokemon.attack_opponent(self.player_pokemon, opponent_move_idx)
            print("{} used {}! Your {} took {} damage.".format(self.opponent_pokemon.name, self.opponent_pokemon.moves[opponent_move_idx]['name'], self.player_pokemon.name, opponent_damage))
            if self.player_pokemon.hp <= 0:
                print("{} defeated your {}!".format(self.opponent_pokemon.name, self.player_pokemon.name))
                break


player_pokemon = Pokemon("Pikachu", "Electric", 5)
player_pokemon.moves = [
    {'name': 'Thunderbolt', 'power': 10},
    {'name': 'Quick Attack', 'power': 8},
    {'name': 'Iron Tail', 'power': 12},
    {'name': 'Thunder Wave', 'power': 5}
]

opponent_pokemon = Pokemon("Bulbasaur", "Grass", 3)
opponent_pokemon.moves = [
    {'name': 'Vine Whip', 'power': 9},
    {'name': 'Tackle', 'power': 7},
    {'name': 'Poison Powder', 'power': 5},
    {'name': 'Leech Seed', 'power': 6}
]

battle = Battle(player_pokemon, opponent_pokemon)
battle.start_battle()
