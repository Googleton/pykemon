import pygame as pg;
import json;
import Entity;
import GuiNPCText;
import GuiBattle;
import PokemonManager;

class BasicNPC(Entity.Entity) :

    def __init__(self, x, y):
        Entity.Entity.__init__(self);
        self.texture = pg.image.load("resources/npc_3.png");
        self.image = self.texture.subsurface(pg.Rect(0, 0, 14, 20));
        self.image.set_colorkey((115, 197, 165));
        self.xOffset = 0;#-1
        self.yOffset = 0;#2

        self.rect = pg.Rect(x + self.xOffset, y + self.yOffset, 16, 22);
        self._layer = 2;

        self.dialog = "x";
        self.dialog_multi = [];

        self.hasMultiDialog = False;

        self.hasPath = False;
        self.path = [];
        self.waypoint = ();
        self.moving = False;
        #Required for collision
        self.occupied = True;
        self.type = "bystander";
        self.name = "NO_NAME";
        self.trainerTex = "trainer_3.png";
        self.team = [];
        self.beaten = False;


    def update(self, events, world, game):
        if self.moving :
            if ((self.rect.x-self.xOffset)/16, (self.rect.y-self.yOffset)/16) == self.waypoint:
                self.moving = False;
            self.moveToWaypoint();
        else :
            self.updateWaypoint()

    def moveToWaypoint(self):
        pass;

    def updateWaypoint(self):
        if self.hasPath :
            for waypoint in self.path:
                if (self.rect.x/16, self.rect.y/16) != waypoint:
                    self.waypoint = waypoint;
                    self.moving = True;

    def interact(self, entity, game, player):
        print(self.dialog);
        if self.type == "bystander" :
            game.guiHandler.openGui(GuiNPCText.GuiNPCText(self.dialog, self.name, self));
        elif self.type == "trainer" :
            print(self.beaten);
            if len(player.team) > 0 and self.beaten == False :
                game.guiHandler.openGui(GuiBattle.GuiBattle(self.dialog, self, player));
            elif self.beaten == True :
                game.guiHandler.openGui(GuiNPCText.GuiNPCText("Tu m'as deja vaincu ...", self.name, None));
            else :
                game.guiHandler.openGui(GuiNPCText.GuiNPCText("Vous n'avez pas de pokemons pour combattre !", "Jeu", None));

    def createTeam(self, team, game) :
        if self.type == "trainer" :
            for pokemon in team :
                new_poke = game.pokemonManager.getPokemon(pokemon["name"]);
                new_poke.level = pokemon["level"];
                new_poke.updateHealth();
                self.team.append(new_poke);

    def getPokemon(self, index) :
        if len(self.team) > 0 :
            return self.team[index];







