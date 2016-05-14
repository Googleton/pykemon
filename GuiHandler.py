import pygame as pg;

class GuiHandler :



    def __init__(self, game) :
        self.game = game;
        self.currentGui = 0;
        pg.font.init();
        self.font = pg.font.Font("resources/gui/rusa.ttf", 19);
        self.font.set_bold(True);

    def openGui(self, gui) :
        self.currentGui = gui;
        self.game.state = self.game.stateDict["menu"];

    def closeGui(self) :
        self.game.state = self.game.stateDict["world"];
        self.currentGui = 0;


    def update(self, game, events) :
        if self.currentGui != 0 :
            self.currentGui.update(game, events, self.font);

    def render(self, display) :
        if self.currentGui != 0 :
            self.currentGui.render(display, self.font);
