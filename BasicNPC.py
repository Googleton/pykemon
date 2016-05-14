import pygame as pg;
import json;
import Entity;
import GuiNPCText;
import GuiBattle;
import PokemonManager;
import Tile;

class BasicNPC(Entity.Entity) :

    def __init__(self, x, y):
        Entity.Entity.__init__(self);
        self.texture = pg.image.load("resources/npc_3.png");
        self.image = self.texture.subsurface(pg.Rect(0, 0, 14, 20));
        self.image.set_colorkey((115, 197, 165));
        self.xOffset = 0;#-1
        self.yOffset = 0;#2
        self.coords = (x, y);

        self.rect = pg.Rect(x, y, 16, 22);
        self._layer = 2;
        self.direction = 0;
        self.mirror = False;

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

        self.defeat_text = "";
        self.defeat_action = "";

        self.quest_involved = -1;
        self.quest_action = "";
        self.quest_dialog = "";

        self.isActive = True;
        self.world = None;


    def update(self, events, world, game):
        if self.world is None :
            self.world = world;

        if self.moving :
            if ((self.rect.x-self.xOffset)/16, (self.rect.y-self.yOffset)/16) == self.waypoint:
                self.moving = False;
            self.moveToWaypoint();
        else :
            self.updateWaypoint()

        if self.isActive == False :
            world.destroyEntity(self);


    def moveToWaypoint(self):
        pass;

    def updateWaypoint(self):
        if self.hasPath :
            for waypoint in self.path:
                if (self.rect.x/16, self.rect.y/16) != waypoint:
                    self.waypoint = waypoint;
                    self.moving = True;

    def interact(self, entity, game, player):
        if self.isActive :
            if self.type == "bystander" :
                game.guiHandler.openGui(GuiNPCText.GuiNPCText(self.dialog, self.name, self));
            elif self.type == "trainer" :
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

    def onDefeated(self, player, game) :
        print("On defeated called")
        if self.quest_action == "disappear" :
            self.isActive = False;
        if self.quest_action == "disappear_all" :
            self.isActive = False;
            for entity in self.world.entities :
                if type(entity) is BasicNPC :
                    if "Magma" in entity.name :
                        self.world.destroyEntity(entity);
        if self.quest_action == "goto_lab" :
            tile = self.world.tileAt(self.rect.x,self.rect.y);
            if type(tile) is Tile.Tile :
                tile.collider = False;
                tile.occupied = False;
            game.fadeScreenIn(8);
            self.rect.x = 13*16;
            self.rect.y = 13*16;
            tile = self.world.tileAt(self.rect.x,self.rect.y);
            if type(tile) is Tile.Tile :
                tile.collider = True;
                tile.occupied = True;








