import pygame as pg;
import sys;
import GuiBase;
import GuiTeam;

class GuiPauseMenu(GuiBase.GuiBase) :

    def __init__(self, player):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.image = pg.image.load("resources/gui/pause_menu.png");
        self.image.set_colorkey((255, 0, 255));
        self.livingTime = 0;
        self.player = player;

        #Image de la flèche
        self.arrow_image = pg.image.load("resources/gui/ge_arrow.png");
        self.arrowCoords = (200, 300);
        self.arrowSelected = 0;

        #Liste des options disponibles
        self.buttons = ["Pokemons", "Inventaire", "Joueur", "Sauvegarder", "Options", "Quitter"];
        self.buttons_images = [];

    def render(self, display, font):
        self.image.set_colorkey((255, 0, 255));
        display.blit(self.image, (600, 0));
        display.blit(self.arrow_image, self.arrowCoords);
        for button_img in self.buttons_images :
            display.blit(button_img, (630, 50 + self.buttons_images.index(button_img) * 60))


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
        if index == 3 :
            print("Sauvegarde ...");
            game.save_game();
        elif index == 5 :
            game.on_terminate();
        elif index == 0 :
            game.guiHandler.openGui(GuiTeam.GuiTeam(self.player, None));
        else :
            print("Menu indisponible");