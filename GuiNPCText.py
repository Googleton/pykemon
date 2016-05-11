import pygame as pg;
import GuiBase;

class GuiNPCText(GuiBase.GuiBase) :

    def __init__(self, text, name):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.image = pg.image.load("resources/gui/npc_text.png");
        self.image.set_colorkey((255, 0, 255));
        self.text = text;
        self.name = name;
        self.textImg = 0;
        self.livingTime = 0;

    def render(self, display, font):
        if self.textImg == 0 :
            self.textImg = font.render(self.name + " : " + self.text, 0, (0, 0, 0));
        self.image.set_colorkey((255, 0, 255));
        display.blit(self.image, (100, 400));
        display.blit(self.textImg, (140, 440));

    def update(self, game, events, font):
        self.livingTime += 1;
        if self.livingTime >= 30 :
            for event in events :
                if event.type == pg.KEYDOWN :
                    if event.key == pg.K_SPACE :
                        self.nextStep(game);

    def nextStep(self, game) :
        game.guiHandler.closeGui();

