import pygame as pg;
import Entity;

class Tile(Entity.Entity) :

    def __init__(self, x, y, id, world) :
        Entity.Entity.__init__(self);
        self.image = world.all_tiles[id];
        self.image.set_alpha(0);
        #self.image.fill((255, 255, 255));
        self.rect = pg.Rect((x, y, 32, 32))
        self.ID = id;
        self.collider = False;
        self._layer = 1;
        self.occupied = False;

        #Gestion des teleporteurs
        self.teleporter = False;
        self.teleportX = 0;
        self.teleportY = 0;

    def onSteppedOn(self, entity, game):
        if self.teleporter :
            game.fadeScreenIn(10);
            entity.teleportAt(self.teleportX, self.teleportY);
            #game.fadeScreenOut(50);

    def update(self, events, world, game):
        pass;