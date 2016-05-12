import pygame as pg;
import sys;
import GuiBase;
import BasicNPC;

class GuiMainMenu(GuiBase.GuiBase) :

    def __init__(self, player):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.image = pg.image.load("resources/gui/pause_menu.png");
        self.image.set_colorkey((255, 0, 255));
        self.livingTime = 0;
        self.player = player;

        #Image de la flÃƒÆ’Ã‚Â¨che
        self.arrow_image = pg.image.load("resources/gui/ge_arrow.png");
        self.arrowCoords = (200, 300);
        self.arrowSelected = 0;

        #Liste des options disponibles
        self.buttons = ["Continuer", "Nouvelle partie", "Quitter"];
        self.buttons_images = [];

    def render(self, display, font):
        self.image.set_colorkey((255, 0, 255));
        display.blit(self.image, (600, 0));
        display.blit(self.arrow_image, self.arrowCoords);
        for button_img in self.buttons_images :
            display.blit(button_img, (630, 50 + self.buttons_images.index(button_img) * 60), button_img.get_rect());


    def update(self, game, events, font):
        self.livingTime += 1;

        if len(self.buttons_images) == 0 :
            for button in self.buttons :
                self.buttons_images.append(font.render(button, 0, (0, 0, 0)));

        self.arrowCoords = (610, 50 + (self.arrowSelected * 60))

        if self.livingTime >= 5 :
            for event in events :
                if event.type == pg.KEYDOWN :
                    if event.key == pg.K_DOWN :
                        self.arrowSelected += 1;
                        if(self.arrowSelected > len(self.buttons) - 1) :
                            self.arrowSelected = 0;
                    if event.key == pg.K_UP :
                        self.arrowSelected -= 1;
                        if(self.arrowSelected < 0) :
                            self.arrowSelected = len(self.buttons) - 1;
                    if event.key == pg.K_ESCAPE :
                        self.nextStep(game);
                    if event.key == pg.K_SPACE :
                        self.pressButton(self.arrowSelected, game);

    def nextStep(self, game) :
        game.guiHandler.closeGui();

    def pressButton(self, index, game) :
        if index == 0 :
            self.nextStep(game);
            game.load_game();
            if game.player.questProgress >= 5 :
                for entity in game.world.entities :
                    if type(entity) is BasicNPC.BasicNPC :
                        if "Magma" in entity.name :
                            game.world.destroyEntity(entity);
        elif index == 2 :
            game.on_terminate();
        else :
            self.nextStep(game);
            game.new_game();
