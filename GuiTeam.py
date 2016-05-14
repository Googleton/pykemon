import pygame as pg;
import GuiBase;

class GuiTeam(GuiBase.GuiBase) :

    def __init__(self, player, guiBattle):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.base_image = pg.image.load("resources/gui/team_gui.png").convert();
        self.image = pg.transform.scale(self.base_image.subsurface((8, 24, 240, 160)), (240*3, 160*3));
        self.background_color = pg.surface.Surface((800, 600));
        self.background_color.fill(0x889828);

        self.player = player;

        if guiBattle is not None :
            self.selectMode = True;
            self.guiBattle = guiBattle;
        else :
            self.selectMode = False;

        self.default_colorkey = (255, 223, 128)
        #All widgets
        self.widget_empty = pg.transform.scale(self.base_image.subsurface((256, 274, 142, 22)), (142*3, 22*3));
        self.widget_empty.set_colorkey(self.default_colorkey);

        self.widget_main = pg.transform.scale(self.base_image.subsurface((256, 26, 78, 49)), (78*3, 49*3));
        self.widget_main.set_colorkey(self.default_colorkey);

        self.widget_main_selected = pg.transform.scale(self.base_image.subsurface((336, 26, 78, 49)), (78*3, 49*3));
        self.widget_main_selected.set_colorkey(self.default_colorkey);

        self.widget_secondary = pg.transform.scale(self.base_image.subsurface((256, 178, 142, 22)), (142*3, 22*3));
        self.widget_secondary.set_colorkey(self.default_colorkey);

        self.widget_secondary_selected = pg.transform.scale(self.base_image.subsurface((256, 202, 142, 22)), (142*3, 22*3));
        self.widget_secondary_selected.set_colorkey(self.default_colorkey);

        self.widget_poke = pg.transform.scale(self.base_image.subsurface((18, 192, 20, 24)), (20*3, 24*3));
        self.widget_poke.set_colorkey(self.default_colorkey);

        self.widget_poke_selected = pg.transform.scale(self.base_image.subsurface((42, 192, 20, 24)), (20 * 3, 24 * 3));
        self.widget_poke_selected.set_colorkey(self.default_colorkey);

        self.selected = 0;

    def update(self, game, events, font):
        for event in events :
            if event.type == pg.KEYDOWN :
                if event.key == pg.K_ESCAPE :
                    game.guiHandler.closeGui();
                if event.key == pg.K_UP :
                    self.selected -= 1;
                    if self.selected < 0 :
                        self.selected = 0;
                if event.key == pg.K_DOWN:
                    self.selected += 1;
                    if self.selected > len(self.player.team) :
                        self.selected = len(self.player.team);
                if event.key == pg.K_SPACE :
                    if self.selected == len(self.player.team) and self.selectMode:
                        game.guiHandler.openGui(self.guiBattle);
                    elif self.selectMode :
                        if self.player.team[self.selected] == self.guiBattle.player_pokemon :
                            if self.player.team[self.selected].currentHealth > 0 :
                                game.guiHandler.openGui(self.guiBattle);
                        else :
                            self.guiBattle.player_pokemon = self.player.team[self.selected];
                            game.guiHandler.openGui(self.guiBattle);
                            self.guiBattle.updateStatus("player", self.guiBattle.player_pokemon, True, font);
                    elif self.selected == len(self.player.team) :
                        game.guiHandler.closeGui();

    def render(self, display, font):
        display.blit(self.background_color, (0, 0));
        display.blit(self.image, (20, 60));
        for i in range(0, 5) :
            display.blit(self.widget_empty, (310, 100+(70*i)));

        display.blit(font.render("Retour",0, (255, 255, 255)), (630, 480));


        #Pokemons
        if len(self.player.team) > 0 :
            if self.selected == 0 :
                img_outline = self.widget_main_selected;
                img_poke = self.widget_poke_selected;
            else:
                img_outline = self.widget_main;
                img_poke = self.widget_poke;

            display.blit(img_outline, (50, 150));
            display.blit(img_poke, (40, 140));
            self.player.getPokemon(0).draw_inventory(display, 50, 160);
            display.blit(font.render(self.player.getPokemon(0).name, 0, (255, 255, 255)), (110, 200));
            display.blit(font.render("Lv" + str(self.player.getPokemon(0).level), 0, (255, 255, 255)), (140, 220));
            pg.draw.rect(display, (112, 248, 168),(123, 249, (self.player.getPokemon(0).currentHealth / self.player.getPokemon(0).maxHealth) * 142, 9));
            display.blit(font.render(str(self.player.getPokemon(0).currentHealth) + "/" + str(self.player.getPokemon(0).maxHealth), 0, (255, 255, 255)), (200, 268));

            for i in range(0, len(self.player.team) - 1) :

                if i+1 == self.selected :
                    img_outline = self.widget_secondary_selected;
                    img_poke = self.widget_poke_selected;
                else :
                    img_outline = self.widget_secondary;
                    img_poke = self.widget_poke;

                display.blit(img_outline, (310, 100 + (70 * i)));
                display.blit(img_poke, (300, 90+(70*i)));
                self.player.getPokemon(i+1).draw_inventory(display, 310, 100 + (70*i));
                display.blit(font.render(self.player.getPokemon(i+1).name, 0, (255, 255, 255)), (410, 120 + (70*i )));
                display.blit(font.render("Lv" + str(self.player.getPokemon(i+1).level), 0, (255, 255, 255)), (425, 145 + (70*i)));
                pg.draw.rect(display, (112, 248, 168), (575, 124+(70*i), (self.player.getPokemon(i+1).currentHealth / self.player.getPokemon(i+1).maxHealth) * 142, 9));
                display.blit(font.render(str(self.player.getPokemon(i+1).currentHealth) + "/" + str(self.player.getPokemon(i+1).maxHealth), 0,(255, 255, 255)), (635, 139+(70*i)));
        #Fin Pokemons

        if self.selected == len(self.player.team):
            img = self.widget_poke_selected;
        else:
            img = self.widget_poke;
        display.blit(img, (565, 457));