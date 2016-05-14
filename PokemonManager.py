import pygame as pg;
import json;

pokemon_sheet = pg.image.load("resources/pokemon_data/pokemon_sheet.png");
poke_image = pg.transform.scale2x(pokemon_sheet);

class PokemonManager() :

    ###
    #Cette classe sert a gerer tout les pokemons ( Les charger en memoire, en creer et en supprimer en jeu etc... )
    ###
    pokemon_list = [];
    attacks_list = [];


    def __init__(self, game) :
        self.loadPokemons();

    def loadPokemons(self) :
        print("Loading Pokemons ...")
        index_file = open("resources/pokemon_data/index.json").read();
        attacks_file = open("resources/pokemon_data/attacks.json").read();
        indexData = json.loads(index_file);
        attacksData = json.loads(attacks_file);

        attacks = attacksData["attacks"];
        for attack in attacks :
            new_attack = Attack(attack["name"], attack["base_damage"]);
            new_attack.type = attack["type"];
            new_attack.critical_chance = attack["critical_chance"];
            self.attacks_list.append(new_attack);

        pokemons = indexData["id"];
        for pokemon in pokemons :
            pokemon_file = open("resources/pokemon_data/pokemons/" + pokemon["filename"]).read();
            pokemonData = json.loads(pokemon_file);

            poke = Pokemon(pokemonData["name"], pokemon["index"], pokemonData["pos_front_x"], pokemonData["pos_front_y"],
                pokemonData["pos_inventory_x"], pokemonData["pos_inventory_y"]);
            poke.maxHealth = pokemonData["health"];
            poke.currentHealth = poke.maxHealth;
            poke.attacks = [];
            poke.base_health = pokemonData["base_health"];
            poke.base_attack = pokemonData["base_attack"];
            poke.base_defense = pokemonData["base_defense"];
            poke.type = pokemonData["type"];
            for attack in pokemonData["attacks"] :
                poke_attack = self.getAttack(attack["name"]);
                poke.attacks.append(poke_attack);
            while len(poke.attacks) < 4 :
                poke.attacks.append(None);
            self.pokemon_list.append(poke);


    def getEffectiveModifier(self, type1, type2):
        if type1 == "fire" and type2 == "water" :
            return 0.75;
        elif type1 == "fire" and type2 == "grass" :
            return 1.25;
        elif type1 == "water" and type2 == "fire" :
            return 1.25;
        elif type1 == "water" and type2 == "grass" :
            return 0.75;
        elif type1 == "grass" and type2 == "water" :
            return 1.25;
        elif type1 == "grass" and type2 == "fire" :
            return 0.75;
        else :
            return 1.0;


    def getPokemon(self, name) :
        for pokemon in self.pokemon_list :
            if pokemon.name == name :
                return pokemon;

    def getAttack(self, name) :
        for attack in self.attacks_list :
            if attack.name == name :
                return attack;


class Attack() :

    name = "Charge";
    damage = 5;
    type = "normal";
    critical_chance = 0;

    def __init__(self, name, damage) :
        self.name = name;
        self.damage = damage;

class Pokemon() :

    #Index de base = 0: Arcko
    index = 1;

    #Non-existant, donc ce nom est choisi
    name = "MISSINGNO";
    level = 1;
    experience = 0;
    attacks = [];

    maxHealth = 1;
    currentHealth = maxHealth;

    base_health = 10;
    base_defense = 10;
    base_attack = 10;

    currentAttack = 10;
    currentDefense = 10;

    type = "normal";

    frontX = 0;
    frontY = 0;
    inventoryX = 0;
    inventoryY = 0;

    size_front = 64 * 2; #Taille de l'image avant et arriere
    size_inventory = 32 * 2; #Taille de l'image dans l'inventaire
    front_to_back = 144 * 2; #Ecart entre l'image avant et arriere sur le spritesheet

    def __init__(self, name, index, frontX, frontY, inventoryX, inventoryY) :
        self.name = name;
        self.index = index;
        self.frontX = frontX * 2;
        self.frontY = frontY * 2;
        self.inventoryX = inventoryX * 2;
        self.inventoryY = inventoryY * 2;

    def draw_front(self, display, x, y):
        poke_image.set_colorkey((255, 200, 106));
        display.blit(poke_image, (x, y), pg.Rect(self.frontX, self.frontY, self.size_front, self.size_front));

    def draw_back(self, display, x, y):
        poke_image.set_colorkey((255, 200, 106));
        display.blit(poke_image, (x, y), pg.Rect(self.frontX + self.front_to_back, self.frontY, self.size_front, self.size_front));

    def draw_inventory(self, display, x, y):
        poke_image.set_colorkey((255, 200, 106));
        display.blit(poke_image, (x, y), pg.Rect(self.inventoryX, self.inventoryY, self.size_inventory, self.size_inventory));

    def dealDamage(self, ammount) :
        #Le pokemon meurt
        if (self.currentHealth - ammount) < 0 :
            self.currentHealth = 0;
            return True;
        #Degat negatif = soins. On evite de depasser la vie max.
        elif (self.currentHealth - ammount) > self.maxHealth :
            self.currentHealth = self.maxHealth;
            return False;
        #Ne meurt pas. On inflige juste les degats.
        else :
            self.currentHealth -= ammount;
            return False;

    def updateHealth(self) :
        self.maxHealth = int(((2 * self.base_health * self.level) / 50) + self.level + 10);
        self.currentHealth = self.maxHealth;

    def updateStats(self):
        self.currentAttack =  int(((2 * self.base_attack * self.level) / 50) + 5);
        self.currentDefense = int(((2 * self.base_defense * self.level) / 50) + 5);


