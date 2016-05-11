import pygame as pg;

class GuiBase(pg.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self);
        self.x = x;
        self.y = y;
        self.width = width;
        self.height = height;
        self.image= pg.Surface([self.width, self.height]);
        self.image.fill((0xFFFFFF));
        self.rect = self.image.get_rect();
        self.rect.x = x;
        self.rect.y = y;


    def setImage(self, image) :
        self.image = image;

    def update(self, game, events) :
        pass;

