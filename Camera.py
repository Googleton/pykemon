import pygame as pg;

class Camera(object) :

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)
    def apply(self, target):
        return target.rect.move(self.state.topleft);
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect);