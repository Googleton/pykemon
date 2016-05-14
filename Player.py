import pygame as pg;
import Entity;
import Tile;
import MathUtils;
import GuiPauseMenu;

class Player(Entity.Entity) :


    #tilePosX = posX / 16;
    #tilePosY = (posY+22)/16;

    velocity = [0, 0];

    def __init__(self, x, y):
        Entity.Entity.__init__(self);
        self.player_sheet = pg.image.load("resources/player.png");
        self.image = self.player_sheet.subsurface(pg.Rect(0, 0, 16, 22));
        self.image.set_colorkey((255, 0, 255));
        self.rect = pg.Rect(x, y, 14, 22);
        self._layer = 2;
        self.posX = 64;
        self.posY = 64-22;

        self.zoomEnabled = True;
        self.moving = False;
        #Nombre d'update entre chaque frame
        self.anim_frame_count = 8;
        self.anim_speed = self.anim_frame_count;
        #Nombre de frame par animation
        self.anim_max_frame = 3;
        #Direction : 0 = Bas, 1 = Haut, 2 = Gauche, 3 = Droite  Correspond au Y sur le sheet
        self.anim_direction = 0;
        #Numero de la frame. Correspond a la position X sur le sheet
        self.anim_pos = 0;

        #Gestion du mouvement sur plusieurs ticks
        self.movingTick = 0;
        self.oldX = 0;
        self.oldY = 0;
        self.newX = 0;
        self.newY = 0;
        self.keepMoving = False;
        self.heldTick = 0;

        #Gestion des interactions entre plusieurs entites
        self.interactCooldown = 0;
        self.canInteract = True;

        self.directionDict = {0: [0, 1], 1: [0, -1], 2: [-1, 0], 3: [1, 0]};

        #Pokemons
        self.team = [];


        self.questProgress = 0;

        print("Player Initialized !")

    def update(self, events, world, game):
        self.rect.x = self.posX;
        self.rect.y = self.posY;
        self.handleInput(events, world, game);
        self.updateAnimation(self.velocity);
        self.image = self.player_sheet.subsurface(pg.Rect(self.anim_pos * 16, self.anim_direction * 22, 16, 22));
        self.image.set_colorkey((255, 0, 255));


        for event in events :
            if event.type == pg.KEYDOWN :
                if event.key == pg.K_z :
                    self.zoomEnabled = not self.zoomEnabled;

        if self.interactCooldown > 0 :
            self.interactCooldown -= 1;
        else :
            self.canInteract = True;

        if self.moving :
            self.move(self.velocity, world, True, game);


    def interactWith(self, world, game, player):
        print(self.rect.x/16, (self.rect.y+6)/16);
        self.canInteract = False;
        interactX = self.posX + (self.directionDict[self.anim_direction][0] * 16);
        interactY = self.posY + (self.directionDict[self.anim_direction][1] * 16) + 6;
        if not world.interact(interactX, interactY, self, game, player):
            self.canInteract = True;
        else :
            self.interactCooldown = 30;

    #Incapable de verifier les coordonnees : Risque de teleportation dans une boite avec collider
    #Coordonnees en tiles; non en pixel
    def teleportAt(self, newX, newY) :
        self.oldX = self.posX;
        self.oldY = self.posY;
        self.posX = newX*16;
        self.posY = (newY*16) - 6;
        self.rect.x = self.posX;
        self.rect.y = self.posY;
        self.newX = self.posX;
        self.newY = self.posY;

    #Lance la sequence de deplacement du personnage
    def move(self, velocity, world, alreadyMoving, game):
        self.moving = True;

        if not alreadyMoving :
            self.movingTick = 0;
            self.oldX = self.posX;
            self.oldY = self.posY;
            self.newX = self.oldX + (self.velocity[0] * 16);
            self.newY = self.oldY + (self.velocity[1] * 16);
            tile = world.tileAt(self.newX, self.newY+6);
            if tile is not None and tile.occupied == True:
                self.posX = self.oldX;
                self.posY = self.oldY;
                self.moving = False;
            else :
                if tile is not None :
                    tile.onSteppedOn(self, game);
        else :
            if self.movingTick > 8 :
                self.movingTick = 0;
                self.moving = False;
                if self.keepMoving :
                    self.move(self.velocity, world, False);
            else :
                self.posX = MathUtils.lerp(self.oldX, self.newX, self.movingTick/8);
                self.posY = MathUtils.lerp(self.oldY, self.newY, self.movingTick/8);
                self.movingTick += 1;

    #Mets a jour l'animation du personnage
    def updateAnimation(self, velocity):
        if self.moving :
            if self.anim_pos + 1 == 4 :
                self.anim_pos = 0;
            else :
                if self.anim_speed == self.anim_frame_count :
                    self.anim_pos += 1;
                    self.anim_speed = 0;
                else :
                    self.anim_speed += 1;
        else :
            self.anim_pos = 0;

    #Plus utilise depuis l'ajout de camera;
    def render(self, display, game):
        display.blit(self.player_sheet.subsurface(pg.Rect(0, 0, 14, 22)), self.posX, self.posY-10);

    #Gere toutes les entrees utilisateur dont le joueur se sert ( fleches, barre d'espace )
    def handleInput(self, events, world, game) :
        keys = pg.key.get_pressed();
        if keys[pg.K_UP] and not self.moving:
            self.heldTick += 1;
            self.anim_direction = 1;
            if self.heldTick > 10 :
                self.velocity = self.directionDict[self.anim_direction];
                self.move(self.velocity, world, False, game);
        elif keys[pg.K_DOWN] and not self.moving:
            self.heldTick += 1;
            self.anim_direction = 0;
            if self.heldTick > 10 :
                self.velocity = self.directionDict[self.anim_direction];
                self.move(self.velocity, world, False, game);
        elif keys[pg.K_RIGHT] and not self.moving:
            self.heldTick += 1;
            self.anim_direction = 3;
            if self.heldTick > 10 :
                self.velocity = self.directionDict[self.anim_direction];
                self.move(self.velocity, world, False, game);
        elif keys[pg.K_LEFT] and not self.moving:
            self.heldTick += 1;
            self.anim_direction = 2;
            if self.heldTick > 10 :
                self.velocity = self.directionDict[self.anim_direction];
                self.move(self.velocity, world, False, game);

        if keys[pg.K_SPACE] and self.canInteract :
            self.interactWith(world, game, self);

        if keys[pg.K_ESCAPE] and self.interactCooldown <= 0 :
            game.guiHandler.openGui(GuiPauseMenu.GuiPauseMenu(self));
            self.interactCooldown = 30;


        if not keys[pg.K_UP] and not keys[pg.K_DOWN] and not keys[pg.K_RIGHT] and not keys[pg.K_LEFT] :
            self.keepMoving = False;
            self.velocity = [0, 0];
            self.heldTick = 0;

    def createTeam(self, team, game) :
        for pokemon in team :
            new_poke = game.pokemonManager.getPokemon(pokemon["name"]);
            new_poke.level = pokemon["level"];
            self.team.append(new_poke);

    def addPokemon(self, pokemon) :
        if len(self.team) < 6 :
            self.team.append(pokemon);

    def getPokemon(self, index) :
        if len(self.team) > 0 :
            return self.team[index];

    def stillHasPokemonAlive(self):
        for pokemon in self.team :
           if pokemon.currentHealth > 0 :
               return True;
        return False;

    def getFirstPokemonAlive(self):
        for pokemon in self.team :
            if pokemon.currentHealth > 0:
                return pokemon;
