# -*- coding: utf-8 -*-


import sys;
import pygame as pg;
import json;

import World;
import Player;
import Camera;
import Tile;
import MathUtils;
import GuiHandler;
import GuiMainMenu;
import PokemonManager;

import cProfile;

from pygame.locals import *;


def simple_camera(camera, target_rect) :
    l, t, _, _ = target_rect;
    _, _, w, h = camera;
    return Rect(-l+400, -t+300, 800, 600);


class Game:

    #Defini l'UPS et le FPS ( Update par seconde, Frames par secondes )
    UPS = 20;
    FPS = 60;

    player = Player.Player(32, 32);
    camera = Camera.Camera(simple_camera, 800, 600);

    fadeImage = pg.Surface((800, 600));

    def __init__(self):
        self._running = True;
        self._displaySurface = None;
        self._clock = pg.time.Clock();
        self._flags = pg.HWSURFACE | pg.DOUBLEBUF;
        self.size = self._width, self._height = 800, 600;
        self.fadeProgress = 0;
        self.fadeTime = 0;
        self.fadeIn = False;
        self.state = 1;
        self.stateDict = {"pause" : 0, "world" : 1, "menu" : 2};
        self.guiHandler = GuiHandler.GuiHandler(self);
        self.pokemonManager = PokemonManager.PokemonManager(self);
        self.load_game();


    def on_init(self):
        pg.init();
        self._displaySurface = pg.display.set_mode(self.size, self._flags);
        self.world = World.World(self);
        self.world.entities.add(self.player);
        pg.display.set_caption("Projet ISN - Pykemon");
        pg.font.init();
        self._running = True;
        self.fadeImage.fill((0, 0, 0));
        self.fadeImage.set_alpha(0);
        self.guiHandler.openGui(GuiMainMenu.GuiMainMenu(self));


    def on_event(self, event):
        if event.type == QUIT or (event.type == K_ESCAPE) :
            self._running = False;

    def on_update(self, events, world, game):
        if self.state == self.stateDict["world"] :
            self.world.update(events, world, game);
        if self.state == self.stateDict["menu"] :
            self.guiHandler.update(game, events);


        if self.fadeTime > 0 and self.fadeIn == True:
            self.fadeScreenIn(self.fadeTime);
        elif self.fadeImage.get_alpha() > 0 :
            self.fadeScreenOut(8);


    def on_render(self) :
        self._displaySurface.fill(0x7AF0FF);

        self.world.render(self._displaySurface, self);
        self.camera.update(self.player);


        if self.player.zoomEnabled == True :
            #image = pg.transform.scale2x(self._displaySurface);
            image = pg.transform.scale(self._displaySurface, (1600, 1200));
            self._displaySurface.blit(image, (-self._width/2, -self._height/2));
        self._displaySurface.blit(self.fadeImage, (0, 0));
        self.guiHandler.render(self._displaySurface);
        #pg.display.update(image);
        pg.display.flip();
        #pg.display.set_caption("Pykemon - FPS : " + str(self._clock.get_fps()));

    def fadeScreenIn(self, fadeTime) :
        self.fadeIn = True;
        if self.fadeImage.get_alpha() < 255 :
            self.fadeTime = fadeTime;
            self.fadeImage.set_alpha(MathUtils.lerp(0, 255, self.fadeProgress/self.fadeTime))
            self.fadeProgress += 1;
            if self.fadeProgress > self.fadeTime :
                self.fadeProgress = 0;
                self.fadeTime = 0;


    def fadeScreenOut(self, fadeTime) :
        self.fadeIn = False;
        if self.fadeImage.get_alpha() > 0 :
            self.fadeTime = fadeTime;
            self.fadeImage.set_alpha(MathUtils.lerp(255, 0, self.fadeProgress/self.fadeTime))
            self.fadeProgress += 1;
            if self.fadeProgress > self.fadeTime :
                self.fadeTime = 0;
                self.fadeProgress = 0;


    def on_terminate(self):
        pg.quit();
        sys.exit();


    def save_game(self) :
        team = [];
        for pokemon in self.player.team :
            pokeData = {"name":pokemon.name,"level":pokemon.level};
            team.append(pokeData);

        data = {
            'playerX' : self.player.posX,
            'playerY' : self.player.posY,
            'team' : team,
            'quest_progress' : self.player.questProgress
        };

        data_as_json = json.dumps(data);
        save_file = open("resources/save_data/save.json", 'w');
        save_file.write(data_as_json);
        save_file.close();

    def load_game(self) :
        loaded_data = open("resources/save_data/save.json").read();
        jsonData = json.loads(loaded_data);
        self.player.posX = jsonData['playerX'];
        self.player.posY = jsonData['playerY'];
        self.player.questProgress = jsonData['quest_progress'];
        self.player.team = [];
        for pokemon in jsonData["team"] :
            new_poke = self.pokemonManager.getPokemon(pokemon["name"]);
            new_poke.level = pokemon["level"];
            new_poke.updateHealth();
            new_poke.updateStats();
            self.player.addPokemon(new_poke);

    def new_game(self) :
        self.player.posX = 432;
        self.player.posY = 58;
        self.player.team = [];
        self.player.questProgress = 0;
        new_poke = self.pokemonManager.getPokemon("Arcko");
        new_poke.level = 7;
        new_poke.updateHealth();
        new_poke.updateStats();
        self.player.addPokemon(new_poke);

    def run(self):
        if self.on_init() == False :
            self._running = False;

        while self._running :
            self._clock.tick(self.FPS);
            events = [];
            for event in pg.event.get() :
                self.on_event(event);
                if self._running :
                    events.append(event);
            self.on_update(events, self.world, self);
            self.on_render();
        self.on_terminate();

if __name__ == '__main__' :
    game = Game();
    game.run();
    #cProfile.run('game.run()');