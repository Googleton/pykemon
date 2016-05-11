import pygame as pg;

class Entity(pg.sprite.Sprite) :
    def __init__(self):
        pg.sprite.Sprite.__init__(self);

    #Update method.
    #Param 1 : events, all the events pygame recieves
    #Param 2 : world, the world in which the entity is in
    def update(self, events, world, game):
        pass;

    #Interact method. This method executes when the player press space while facing the entity.
    #Param 1 : entity, the entity that interacts with this one. ( Usually, the player )
    def interact(self, entity):
        pass;